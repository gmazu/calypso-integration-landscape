from __future__ import annotations

import argparse
import subprocess
import sys
import shutil
from datetime import datetime
from pathlib import Path


def extract_filter_args(argv: list[str]) -> tuple[list[str], list[str]]:
    """Extrae --nivel/--id en el orden recibido y retorna (filtros, resto)."""
    filters: list[str] = []
    rest: list[str] = []
    i = 0
    while i < len(argv):
        arg = argv[i]
        if arg in ("--nivel", "--id"):
            if i + 1 >= len(argv):
                raise SystemExit(f"Error: {arg} requiere un valor.")
            filters.extend([arg, argv[i + 1]])
            i += 2
            continue
        rest.append(arg)
        i += 1
    return filters, rest


def build_filter_args(args: argparse.Namespace, filter_args: list[str], script_path: Path) -> list[str]:
    cmd = [sys.executable, str(script_path)]
    cmd += ["--xlsx", str(args.xlsx)]
    cmd += filter_args
    if args.expand:
        cmd.append("--expand")
    if args.debug:
        cmd.append("--debug")
    if args.output is not None:
        cmd += ["--output", str(args.output)]
    return cmd


def build_manim_args(args: argparse.Namespace, script_path: Path) -> list[str]:
    cmd = ["manim"]
    if args.quality:
        qual = args.quality
        if not qual.startswith("-"):
            qual = f"-{qual}"
        cmd.append(qual)
    if args.resolution:
        cmd += ["-r", args.resolution]
    if args.fps:
        cmd += ["--fps", str(args.fps)]
    if args.preview:
        cmd.append("-p")
    cmd += [str(script_path), args.scene]
    return cmd


def find_latest_mp4(root: Path) -> Path | None:
    mp4s = list(root.rglob("*.mp4"))
    if not mp4s:
        return None
    return max(mp4s, key=lambda p: p.stat().st_mtime)


def prune_other_mp4s(latest: Path) -> None:
    for p in latest.parent.glob("*.mp4"):
        if p != latest:
            try:
                p.unlink()
            except OSError:
                pass


def resolve_script_path() -> Path:
    """Lee run_gantt_pipeline.parametros y retorna el script Manim a usar."""
    cfg_path = Path(__file__).with_name("run_gantt_pipeline.parametros")
    if not cfg_path.exists():
        return Path(__file__).with_name("gantt_timeline_v3.0.0.py")
    try:
        raw = cfg_path.read_text(encoding="utf-8")
    except OSError:
        return Path(__file__).with_name("gantt_timeline_v3.0.0.py")
    script_name = None
    for line in raw.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("script:"):
            _, value = line.split(":", 1)
            script_name = value.strip()
            break
    if not script_name:
        return Path(__file__).with_name("gantt_timeline_v3.0.0.py")
    return Path(__file__).with_name(script_name)


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Genera filter_gantt.tasks desde XLSX y luego renderiza con Manim. "
            "El script activo se toma de run_gantt_pipeline.parametros."
        )
    )
    parser.add_argument("--xlsx", required=True, type=Path, help="Ruta al archivo XLSX.")
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=Path(__file__).with_name("filter_gantt.tasks"),
        help="Archivo de salida (default: filter_gantt.tasks).",
    )
    parser.add_argument(
        "--scene",
        default="GanttTimelineLevel2",
        help="Nombre de la escena Manim.",
    )
    parser.add_argument(
        "--quality",
        default="ql",
        help="Preset de calidad Manim sin guion (ej: ql, qm, qh, pql).",
    )
    parser.add_argument(
        "--resolution",
        help="Resolución Manim en formato W,H (ej: 3840,2160).",
    )
    parser.add_argument(
        "--fps",
        type=int,
        help="FPS para render (ej: 60).",
    )
    parser.add_argument(
        "--preview",
        action="store_true",
        help="Abrir preview después del render.",
    )
    parser.add_argument(
        "-debug",
        "--debug",
        action="store_true",
        help="Imprime un informe breve del filtro antes de renderizar.",
    )
    parser.add_argument(
        "--expand",
        action="store_true",
        help="Al usar --id, expande solo el siguiente nivel del ID desde el XLSX completo.",
    )
    parser.add_argument(
        "--keep-scene",
        type=Path,
        help=(
            "Ruta donde se guarda una copia del último video renderizado. "
            "El último MP4 se busca en media/videos/<script_activo> y se limpian los demás."
        ),
    )
    parser.add_argument(
        "--only-debug",
        action="store_true",
        help="Solo genera el filtro y muestra el informe; no renderiza.",
    )
    filter_args, rest = extract_filter_args(sys.argv[1:])
    args = parser.parse_args(rest)

    if args.only_debug:
        args.debug = True

    if not args.xlsx.exists():
        print(f"Error: no existe el archivo {args.xlsx}", file=sys.stderr)
        return 1

    script_path = resolve_script_path()
    filter_cmd = build_filter_args(args, filter_args, script_path)
    print("Ejecutando:", " ".join(filter_cmd))
    result = subprocess.run(filter_cmd)
    if result.returncode != 0:
        return result.returncode
    if args.only_debug:
        return 0

    manim_cmd = build_manim_args(args, script_path)
    print("Ejecutando:", " ".join(manim_cmd))
    result = subprocess.run(manim_cmd)
    if result.returncode != 0:
        return result.returncode

    media_root = Path(__file__).with_name("media") / "videos" / script_path.stem
    latest = find_latest_mp4(media_root)
    if latest:
        prune_other_mp4s(latest)
        if args.keep_scene:
            args.keep_scene.mkdir(parents=True, exist_ok=True)
            stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            dest = args.keep_scene / f"{args.scene}_{stamp}.mp4"
            try:
                shutil.copy2(latest, dest)
                print(f"Guardado: {dest}")
            except OSError as exc:
                print(f"Error al guardar copia: {exc}", file=sys.stderr)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
