from __future__ import annotations

import argparse
import subprocess
import sys
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


def build_filter_args(args: argparse.Namespace, filter_args: list[str]) -> list[str]:
    cmd = [sys.executable, str(Path(__file__).with_name("gantt_timeline_v2.py"))]
    cmd += ["--xlsx", str(args.xlsx)]
    cmd += filter_args
    if args.expand:
        cmd.append("--expand")
    if args.debug:
        cmd.append("--debug")
    if args.output is not None:
        cmd += ["--output", str(args.output)]
    return cmd


def build_manim_args(args: argparse.Namespace) -> list[str]:
    cmd = ["manim"]
    if args.quality:
        qual = args.quality
        if not qual.startswith("-"):
            qual = f"-{qual}"
        cmd.append(qual)
    if args.preview:
        cmd.append("-p")
    cmd += [str(Path(__file__).with_name("gantt_timeline_v2.py")), args.scene]
    return cmd


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Genera filter_gantt.tasks desde XLSX y luego renderiza con Manim."
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

    filter_cmd = build_filter_args(args, filter_args)
    print("Ejecutando:", " ".join(filter_cmd))
    result = subprocess.run(filter_cmd)
    if result.returncode != 0:
        return result.returncode
    if args.only_debug:
        return 0

    manim_cmd = build_manim_args(args)
    print("Ejecutando:", " ".join(manim_cmd))
    result = subprocess.run(manim_cmd)
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
