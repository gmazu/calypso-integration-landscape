from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/youtube"]


def get_service(client_secret: Path, token_path: Path, use_console: bool):
    flow = InstalledAppFlow.from_client_secrets_file(str(client_secret), SCOPES)
    if use_console:
        creds = flow.run_console()
    else:
        creds = flow.run_local_server(port=0)
    token_path.write_text(creds.to_json(), encoding="utf-8")
    return build("youtube", "v3", credentials=creds)


def load_service(client_secret: Path, token_path: Path, use_console: bool):
    if token_path.exists():
        return build("youtube", "v3", credentials=json.loads(token_path.read_text(encoding="utf-8")))
    return get_service(client_secret, token_path, use_console)


def main() -> int:
    parser = argparse.ArgumentParser(description="Crea un live broadcast + live stream en YouTube.")
    parser.add_argument("--client-secret", required=True, type=Path, help="Ruta al client_secret.json")
    parser.add_argument(
        "--token",
        type=Path,
        default=Path(__file__).with_name(".youtube_token.json"),
        help="Ruta para guardar el token OAuth",
    )
    parser.add_argument("--title", required=True, help="Título del live")
    parser.add_argument("--description", default="", help="Descripción del live")
    parser.add_argument("--privacy", default="private", choices=["private", "unlisted", "public"])
    parser.add_argument(
        "--latency",
        default="normal",
        choices=["normal", "low", "ultraLow"],
        help="Latencia del live",
    )
    parser.add_argument(
        "--save",
        type=Path,
        default=Path(__file__).with_name(".live_stream.json"),
        help="Archivo donde se guardan los datos del stream",
    )
    parser.add_argument(
        "--no-browser",
        action="store_true",
        help="Muestra la URL de autorización en consola en vez de abrir navegador.",
    )
    args = parser.parse_args()

    service = load_service(args.client_secret, args.token, args.no_browser)

    now = datetime.now(timezone.utc).isoformat()
    broadcast_body = {
        "snippet": {"title": args.title, "description": args.description, "scheduledStartTime": now},
        "status": {"privacyStatus": args.privacy},
        "contentDetails": {"latencyPreference": args.latency},
    }
    broadcast = (
        service.liveBroadcasts()
        .insert(part="snippet,status,contentDetails", body=broadcast_body)
        .execute()
    )

    stream_body = {
        "snippet": {"title": f"{args.title} (stream)"},
        "cdn": {"frameRate": "30fps", "resolution": "1080p", "ingestionType": "rtmp"},
    }
    stream = service.liveStreams().insert(part="snippet,cdn", body=stream_body).execute()

    service.liveBroadcasts().bind(
        part="id,contentDetails",
        id=broadcast["id"],
        streamId=stream["id"],
    ).execute()

    ingest = stream["cdn"]["ingestionInfo"]
    data = {
        "broadcast_id": broadcast["id"],
        "stream_id": stream["id"],
        "ingest_address": ingest["ingestionAddress"],
        "stream_name": ingest["streamName"],
        "watch_url": f"https://www.youtube.com/watch?v={broadcast['id']}",
    }

    args.save.write_text(json.dumps(data, indent=2), encoding="utf-8")
    print(json.dumps(data, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
