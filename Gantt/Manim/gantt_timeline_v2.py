from __future__ import annotations

import argparse
import ast
import sys
import textwrap
from collections import OrderedDict
from datetime import datetime
from pathlib import Path
import uuid
import os

from manim import *
from openpyxl import load_workbook


# =============================================================================
# Funciones auxiliares
# =============================================================================
def format_date(value) -> str:
    if isinstance(value, datetime):
        return value.strftime("%d/%m/%y")
    if value is None:
        return ""
    text = str(value).strip()
    if not text:
        return ""
    for fmt in ("%d/%m/%y", "%d/%m/%Y", "%Y-%m-%d"):
        try:
            return datetime.strptime(text, fmt).strftime("%d/%m/%y")
        except ValueError:
            continue
    return text


def format_percent(value) -> str:
    if value is None:
        return ""
    if isinstance(value, (int, float)):
        pct = value * 100 if 0 <= value <= 1 else value
        return f"{int(round(pct))}%"
    text = str(value).strip()
    if not text:
        return ""
    return text if "%" in text else f"{text}%"


def load_tasks_from_xlsx(path: Path) -> list[list]:
    wb = load_workbook(path, read_only=False, data_only=True)
    ws = wb[wb.sheetnames[0]]

    header_row = next(ws.iter_rows(min_row=1, max_row=1))
    headers = [cell.value for cell in header_row]
    header_map = {str(val).strip().lower(): idx for idx, val in enumerate(headers, start=1) if val}

    def col_index(*names: str) -> int | None:
        for name in names:
            key = name.strip().lower()
            if key in header_map:
                return header_map[key]
        return None

    col_id = col_index("id", "uid", "uid ")
    col_name = col_index("nombre de la tarea", "nombre", "task name", "name")
    col_status = col_index("estado", "status")
    col_assigned = col_index("asignado a", "asignado", "assigned")
    col_start = col_index("fecha de inicio", "inicio", "start", "start date")
    col_end = col_index("fecha de finalización", "fecha de finalizacion", "fin", "finish", "end", "end date")
    col_pct = col_index("porcentaje completo", "% completo", "avance", "percent complete", "percentcomplete")
    col_duration = col_index("duración", "duracion", "duration")
    col_pred = col_index("predecesores", "predecessors", "pred")

    if not col_name:
        raise ValueError("No se encontro la columna 'Nombre de la tarea' en el XLSX.")

    tasks = []
    for row_idx in range(2, ws.max_row + 1):
        name_cell = ws.cell(row=row_idx, column=col_name)
        name_val = name_cell.value
        if name_val is None or str(name_val).strip() == "":
            continue

        indent = name_cell.alignment.indent or 0
        level = int(indent)

        task_id = ws.cell(row=row_idx, column=col_id).value if col_id else row_idx - 1
        status = ws.cell(row=row_idx, column=col_status).value if col_status else ""
        assigned = ws.cell(row=row_idx, column=col_assigned).value if col_assigned else ""
        start = ws.cell(row=row_idx, column=col_start).value if col_start else ""
        end = ws.cell(row=row_idx, column=col_end).value if col_end else ""
        pct = ws.cell(row=row_idx, column=col_pct).value if col_pct else ""
        duration = ws.cell(row=row_idx, column=col_duration).value if col_duration else ""
        pred = ws.cell(row=row_idx, column=col_pred).value if col_pred else ""

        if isinstance(task_id, float) and task_id.is_integer():
            task_id = int(task_id)

        tasks.append(
            [
                task_id,
                level,
                str(name_val).strip(),
                str(status).strip() if status is not None else "",
                str(assigned).strip() if assigned is not None else "",
                format_date(start),
                format_date(end),
                format_percent(pct),
                str(duration).strip() if duration is not None else "",
                str(pred).strip() if pred is not None else "",
            ]
        )

    return tasks


def _parse_levels(values: list[str] | None) -> list[int]:
    if not values:
        return []
    levels: list[int] = []
    for raw in values:
        parts = [p.strip() for p in raw.split(",") if p.strip()]
        for part in parts:
            levels.append(int(part))
    return levels


def filter_by_levels(tasks: list[list], levels: list[int]) -> list[list]:
    """Filtra por niveles e incluye ancestros para dar contexto visual."""
    if not levels:
        return tasks
    level_set = set(levels)
    result: list[list] = []
    seen: set[tuple] = set()
    stack: list[list] = []

    for row in tasks:
        level = row[1]
        while stack and stack[-1][1] >= level:
            stack.pop()
        stack.append(row)

        if level in level_set:
            # Incluir ancestros y la fila actual sin duplicados.
            for parent in stack:
                key = tuple(parent)
                if key not in seen:
                    result.append(parent)
                    seen.add(key)

    return result


def parse_filter_sequence(argv: list[str]) -> list[tuple[str, list[int] | int]]:
    """Parsea --nivel/--id en el orden recibido para aplicar filtros anidados."""
    seq: list[tuple[str, list[int] | int]] = []
    i = 0
    while i < len(argv):
        arg = argv[i]
        if arg == "--nivel":
            if i + 1 >= len(argv):
                raise SystemExit("Error: --nivel requiere un valor.")
            levels = _parse_levels([argv[i + 1]])
            seq.append(("nivel", levels))
            i += 2
            continue
        if arg == "--id":
            if i + 1 >= len(argv):
                raise SystemExit("Error: --id requiere un valor.")
            try:
                task_id = int(argv[i + 1])
            except ValueError as exc:
                raise SystemExit("Error: --id requiere un entero.") from exc
            seq.append(("id", task_id))
            i += 2
            continue
        i += 1
    return seq


def split_by_pipe(argv: list[str]) -> list[list[str]]:
    """Divide argumentos en segmentos separados por '|'."""
    segments: list[list[str]] = []
    current: list[str] = []
    for arg in argv:
        if arg == "|":
            segments.append(current)
            current = []
        else:
            current.append(arg)
    segments.append(current)
    return segments


def filter_by_id_with_context(tasks: list[list], task_id: int, max_depth: int | None = None) -> list[list]:
    """
    Filtra la tarea con el ID dado más sus hijos directos.
    Retorna la tarea padre y todas las tareas con nivel mayor hasta encontrar
    otra tarea del mismo nivel o menor.
    """
    result: list[list] = []
    seen: set[tuple] = set()
    stack: list[list] = []

    found_idx = None
    parent_level = None

    for idx, row in enumerate(tasks):
        level = row[1]
        while stack and stack[-1][1] >= level:
            stack.pop()
        stack.append(row)
        if row[0] == task_id:
            found_idx = idx
            parent_level = level
            for parent in stack:
                key = tuple(parent)
                if key not in seen:
                    result.append(parent)
                    seen.add(key)
            break

    if found_idx is None or parent_level is None:
        return []

    # Agregar hijos (nivel > parent_level) hasta encontrar mismo nivel o menor
    for row in tasks[found_idx + 1:]:
        if row[1] <= parent_level:
            break
        if max_depth is not None and row[1] > parent_level + max_depth:
            continue
        key = tuple(row)
        if key not in seen:
            result.append(row)
            seen.add(key)

    return result


def get_tasks_for_render() -> list[list]:
    """Lee tareas desde filter_gantt.tasks (generado por el CLI)."""
    tasks_file = Path(__file__).with_name("filter_gantt.tasks")
    if not tasks_file.exists():
        raise FileNotFoundError(
            f"No se encontró {tasks_file}. "
            "Ejecuta primero el CLI para generar filter_gantt.tasks."
        )
    return load_tasks_from_file(tasks_file)


def load_tasks_from_file(path: Path) -> list[list]:
    text = path.read_text(encoding="utf-8").lstrip()
    module = ast.parse(text)
    for node in module.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "tasks":
                    return ast.literal_eval(node.value)
    raise ValueError("tasks list not found in file")


def write_tasks_file(tasks: list[list], output_path: Path) -> None:
    with output_path.open("w", encoding="utf-8") as f:
        f.write("tasks = [\n")
        for row in tasks:
            f.write(f"    {row},\n")
        f.write("]\n")


# =============================================================================
# CLI standalone (python gantt_timeline_v2.py -xlsx ... --nivel ...)
# =============================================================================
def run_filter_cli() -> int:
    """CLI para generar filter_gantt.tasks desde XLSX."""
    parser = argparse.ArgumentParser(
        description="Genera filter_gantt.tasks desde XLSX o renderiza con Manim."
    )
    parser.add_argument("-xlsx", "--xlsx", required=True, type=Path, help="Ruta al archivo XLSX.")
    parser.add_argument(
        "--expand",
        action="store_true",
        help="Al usar --id, expande solo el siguiente nivel del ID desde el XLSX completo.",
    )
    parser.add_argument(
        "-debug",
        "--debug",
        action="store_true",
        help="Imprime un informe breve del filtro (IDs/niveles/títulos).",
    )
    parser.add_argument(
        "-o", "--output",
        type=Path,
        default=Path(__file__).with_name("filter_gantt.tasks"),
        help="Archivo de salida (default: filter_gantt.tasks).",
    )
    args, _unknown = parser.parse_known_args()
    segments = split_by_pipe(sys.argv[1:])

    if not args.xlsx.exists():
        print(f"Error: no existe el archivo {args.xlsx}", file=sys.stderr)
        return 1

    filtered = load_tasks_from_xlsx(args.xlsx)
    temp_files: list[Path] = []

    for seg_idx, seg in enumerate(segments):
        filter_seq = parse_filter_sequence(seg)
        if filter_seq:
            for kind, value in filter_seq:
                if kind == "nivel":
                    filtered = filter_by_levels(
                        filtered, value if isinstance(value, list) else [value]
                    )
                    print(f"Filtrado por nivel {value}: {len(filtered)} tareas")
                elif kind == "id":
                    base = load_tasks_from_xlsx(args.xlsx) if args.expand else filtered
                    depth = 1 if args.expand else None
                    filtered = filter_by_id_with_context(base, int(value), max_depth=depth)
                    print(f"Filtrado por ID {value}: {len(filtered)} tareas")
        else:
            if seg_idx == 0:
                print(f"Sin filtro: {len(filtered)} tareas")

        if seg_idx < len(segments) - 1:
            tmp = Path("/tmp") / f"gantt_filter_{uuid.uuid4().hex}_{seg_idx}.tasks"
            write_tasks_file(filtered, tmp)
            temp_files.append(tmp)
            filtered = load_tasks_from_file(tmp)

    if args.debug:
        levels = sorted({row[1] for row in filtered})
        print(f"Niveles presentes: {levels}")
        print("Tareas filtradas (id | nivel | título):")
        for task_id, level, name, *_rest in filtered:
            print(f"- {task_id} | {level} | {name}")

    write_tasks_file(filtered, args.output)
    print(f"Escrito: {args.output}")

    for tmp in temp_files:
        try:
            os.remove(tmp)
        except OSError:
            pass
    return 0


# =============================================================================
# Escenas Manim
# =============================================================================

# Uso:
#   manim -pql gantt_timeline_v2.py GanttTimelineLevel2 --xlsx archivo.xlsx --nivel 1
#   manim -pql gantt_timeline_v2.py GanttTimelineLevel2 --xlsx archivo.xlsx --id 42


class GanttTimelineLevel2(Scene):
    def construct(self):
        tasks = get_tasks_for_render()

        title_text = "Hablitación Plataforma Calypso Banco BCI"
        subtitle_text = "Ambiente Pre Productivo"
        level0 = next((row for row in tasks if row[1] == 0), None)
        level1 = next((row for row in tasks if row[1] == 1), None)
        if level0:
            title_text = level0[2]
        if level1:
            subtitle_text = level1[2]

        tasks = [row for row in tasks if row[1] >= 2]

        dated = []
        undated = []
        for row in tasks:
            task_id, _, name, *_rest, start, end, pct, _dur, _pred = row
            if start and end:
                dated.append(
                    {
                        "id": task_id,
                        "name": name,
                        "start": datetime.strptime(start, "%d/%m/%y"),
                        "end": datetime.strptime(end, "%d/%m/%y"),
                        "start_str": start,
                        "end_str": end,
                        "pct": pct,
                    }
                )
            else:
                undated.append({"id": task_id, "name": name})

        dated.sort(key=lambda t: t["start"])

        title = Text(title_text, font_size=28, weight=BOLD)
        subtitle = Text(subtitle_text, font_size=16, color=GRAY_B)
        header = VGroup(title, subtitle).arrange(DOWN, buff=0.2).to_edge(UP, buff=0.4)

        timeline_left = LEFT * 5.5 + DOWN * 0.2
        timeline_right = RIGHT * 5.5 + DOWN * 0.2
        timeline = Line(timeline_left, timeline_right, color=GRAY_B, stroke_width=4)

        if dated:
            start_min = min(t["start"] for t in dated)
            end_max = max(t["end"] for t in dated)
        else:
            start_min = datetime.now()
            end_max = datetime.now()

        def date_to_x(value: datetime) -> float:
            total = (end_max - start_min).days or 1
            offset = (value - start_min).days
            ratio = offset / total
            return interpolate(timeline_left[0], timeline_right[0], ratio)

        # Promedio global de avance para etiqueta en "hoy"
        pct_all = []
        for t in dated:
            if t.get("pct"):
                try:
                    pct_all.append(float(str(t["pct"]).replace("%", "").strip()))
                except ValueError:
                    pass
        avg_all = round(sum(pct_all) / len(pct_all)) if pct_all else None

        # Línea de "hoy"
        today = datetime.now()
        if start_min <= today <= end_max:
            x_today = date_to_x(today)
            today_line = Line(
                [x_today, timeline_left[1] - 3.2, 0],
                [x_today, timeline_left[1] - 2.6, 0],
                color=RED,
                stroke_width=1,
            )
            today_label = Text(f"Hoy {today.strftime('%d/%m')}", font_size=11, color=RED)
            today_label.next_to(today_line, UP, buff=0.05)
            if avg_all is not None:
                today_pct = Text(f"Prom {avg_all}%", font_size=10, color=RED_E)
                today_pct.next_to(today_line, DOWN, buff=0.04)
            else:
                today_pct = None
        else:
            today_line = None
            today_label = None
            today_pct = None

        points = VGroup()
        stems = VGroup()
        labels = VGroup()
        dates = VGroup()
        deltas = VGroup()
        pct_by_date: dict = {}

        grouped = OrderedDict()
        for task in dated:
            key = task["start"].date()
            grouped.setdefault(key, []).append(task)

        above_idx = 0
        below_idx = 0

        date_keys = list(grouped.keys())
        for idx, (key, tasks_for_date) in enumerate(grouped.items()):
            x = date_to_x(tasks_for_date[0]["start"])
            y = timeline_left[1]

            point = Dot([x, y, 0], radius=0.065, color=BLUE_D)

            above = idx % 2 == 0
            if above:
                stem_len = [1.0, 1.5, 2.0][above_idx % 3]
                above_idx += 1
            else:
                stem_len = [1.0, 1.5, 2.0][below_idx % 3]
                below_idx += 1

            date_text = tasks_for_date[0]["start"].strftime("%d/%m")
            date_label = Text(date_text, font_size=12, color=BLUE_D)
            date_label.next_to(point, DOWN if above else UP, buff=0.1)

            offsets = [1.0, 1.5, 2.0] if len(tasks_for_date) > 1 else [stem_len + 0.2]
            for t_idx, task in enumerate(tasks_for_date):
                offset = offsets[t_idx] if t_idx < len(offsets) else offsets[-1]
                target_y = y + (offset if above else -offset)

                title_text = Text(f"ID {task['id']}", font_size=12, weight=BOLD)
                wrapped_name = textwrap.fill(task["name"], width=28)
                body = Text(wrapped_name, font_size=12, color=GRAY_B, line_spacing=0.9)
                end_line = f"Fin: {task['end_str']}"
                if task.get("pct"):
                    end_line = f"{end_line}  {task['pct']}"
                end_text = Text(end_line, font_size=11, color=GRAY_C)
                text_block = VGroup(title_text, body, end_text).arrange(DOWN, buff=0.08, aligned_edge=LEFT)

                text_block.move_to([x, target_y, 0])
                if target_y >= y:
                    text_block.shift(UP * 0.35)
                else:
                    text_block.shift(DOWN * 0.35)
                labels.add(text_block)

                # Barra vertical hueca con relleno segun % por ID
                bar_width = 0.1
                bar_height = abs(target_y - y)
                bar_center = (y + target_y) / 2
                outline = Rectangle(
                    width=bar_width,
                    height=bar_height,
                    stroke_color=GRAY_B,
                    stroke_width=1.3,
                    fill_opacity=0,
                ).move_to([x, bar_center, 0])

                pct_val = None
                if task.get("pct"):
                    try:
                        pct_val = float(str(task["pct"]).replace("%", "").strip())
                    except ValueError:
                        pct_val = None
                if pct_val is None:
                    fill = None
                else:
                    pct_norm = max(0.0, min(1.0, pct_val / 100.0))
                    fill_h = bar_height * pct_norm
                    fill = Rectangle(
                        width=bar_width * 0.75,
                        height=fill_h,
                        stroke_width=0,
                        fill_color=GREEN_C,
                        fill_opacity=0.9,
                    )
                    if target_y >= y:
                        fill.move_to([x, y + fill_h / 2, 0])
                    else:
                        fill.move_to([x, y - fill_h / 2, 0])

                stems.add(outline)
                if fill:
                    stems.add(fill)

            points.add(point)
            dates.add(date_label)

            pcts = []
            for t in tasks_for_date:
                if t.get("pct"):
                    try:
                        pcts.append(float(str(t["pct"]).replace("%", "").strip()))
                    except ValueError:
                        pass
            if pcts:
                pct_by_date[key] = round(sum(pcts) / len(pcts))

        # Escala inferior estilo "mapa": barra segmentada con dias por tramo
        scale_y = timeline_left[1] - 3.2
        bar_height = 0.15
        bar = VGroup()
        for i in range(1, len(date_keys)):
            d0 = date_keys[i - 1]
            d1 = date_keys[i]
            delta_days = (d1 - d0).days
            x0 = date_to_x(datetime.combine(d0, datetime.min.time()))
            x1 = date_to_x(datetime.combine(d1, datetime.min.time()))
            mid_x = (x0 + x1) / 2

            seg_width = max(0.01, x1 - x0)
            seg_color = BLUE_E if i % 2 == 0 else GRAY_E
            seg = Rectangle(
                width=seg_width,
                height=bar_height,
                stroke_width=0,
                fill_color=seg_color,
                fill_opacity=1,
            ).move_to([mid_x, scale_y, 0])
            bar.add(seg)

            tick = Line([x0, scale_y + 0.08, 0], [x0, scale_y - 0.08, 0], color=GRAY_B, stroke_width=1)
            txt = Text(f"{delta_days}d", font_size=10, color=GRAY_B)
            txt.next_to(seg, DOWN, buff=0.06)
            if d1 in pct_by_date:
                avg_txt = Text(f"Prom {pct_by_date[d1]}%", font_size=9, color=GREEN_C)
                avg_txt.next_to(txt, DOWN, buff=0.04)
                deltas.add(VGroup(tick, txt, avg_txt))
            else:
                deltas.add(VGroup(tick, txt))

        if date_keys:
            x_start = date_to_x(datetime.combine(date_keys[0], datetime.min.time()))
            x_end = date_to_x(datetime.combine(date_keys[-1], datetime.min.time()))
            deltas.add(Line([x_end, scale_y + 0.08, 0], [x_end, scale_y - 0.08, 0], color=GRAY_B, stroke_width=1))

        if undated:
            undated_title = Text("Sin fechas", font_size=16, color=GRAY_B)
            undated_lines = VGroup(
                *[Text(f"{t['id']} - {t['name']}", font_size=14) for t in undated]
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
            undated_block = VGroup(undated_title, undated_lines).arrange(DOWN, buff=0.2)
            undated_block.to_edge(RIGHT, buff=0.6).shift(DOWN * 2.2)
        else:
            undated_block = VGroup()

        self.play(Write(header), run_time=1)
        self.play(Create(timeline), run_time=0.8)
        if today_line:
            anims = [FadeIn(today_line), FadeIn(today_label)]
            if today_pct:
                anims.append(FadeIn(today_pct))
            self.play(*anims, run_time=0.4)
        self.play(LaggedStartMap(FadeIn, points, lag_ratio=0.05), run_time=0.9)
        self.play(LaggedStartMap(Create, stems, lag_ratio=0.05), run_time=1.0)
        self.play(LaggedStartMap(FadeIn, dates, lag_ratio=0.05), run_time=0.8)
        self.play(LaggedStartMap(FadeIn, labels, lag_ratio=0.05), run_time=1.2)
        if deltas:
            self.play(FadeIn(bar), run_time=0.4)
            self.play(LaggedStartMap(FadeIn, deltas, lag_ratio=0.03), run_time=0.6)

        if undated_block:
            self.play(FadeIn(undated_block), run_time=0.6)

        self.wait(2)


class GanttTimelineCircular(ThreeDScene):
    def construct(self):
        tasks = get_tasks_for_render()

        title_text = "Hablitación Plataforma Calypso Banco BCI"
        subtitle_text = "Ambiente Pre Productivo"
        level0 = next((row for row in tasks if row[1] == 0), None)
        level1 = next((row for row in tasks if row[1] == 1), None)
        if level0:
            title_text = level0[2]
        if level1:
            subtitle_text = level1[2]

        tasks = [row for row in tasks if row[1] >= 2]

        dated = []
        for row in tasks:
            task_id, _, name, *_rest, start, end, _pct, _dur, _pred = row
            if start and end:
                dated.append(
                    {
                        "id": task_id,
                        "name": name,
                        "start": datetime.strptime(start, "%d/%m/%y"),
                    }
                )

        dated.sort(key=lambda t: t["start"])

        title = Text(title_text, font_size=26, weight=BOLD)
        subtitle = Text(subtitle_text, font_size=16, color=GRAY_B)
        header = VGroup(title, subtitle).arrange(DOWN, buff=0.2).to_edge(UP, buff=0.4)

        outer = Arc(
            radius=3.2,
            start_angle=PI * 0.2,
            angle=PI * 1.6,
            color=GRAY_B,
            stroke_width=2,
        )
        inner = Arc(
            radius=2.6,
            start_angle=PI * 0.2,
            angle=PI * 1.6,
            color=GRAY_C,
            stroke_width=1,
        )

        ticks = VGroup()
        for i in range(70):
            ang = outer.start_angle + (outer.angle * i / 69)
            p1 = 3.25 * np.array([np.cos(ang), np.sin(ang), 0])
            p2 = 3.4 * np.array([np.cos(ang), np.sin(ang), 0])
            ticks.add(Line(p1, p2, stroke_width=1, color=GRAY_B))

        points = VGroup()
        labels = VGroup()
        if dated:
            start_min = min(t["start"] for t in dated)
            end_max = max(t["start"] for t in dated)
        else:
            start_min = datetime.now()
            end_max = datetime.now()

        def date_to_angle(value: datetime) -> float:
            total = (end_max - start_min).days or 1
            offset = (value - start_min).days
            ratio = offset / total
            return outer.start_angle + outer.angle * ratio

        for idx, task in enumerate(dated):
            ang = date_to_angle(task["start"])
            radius = 2.9
            pos = radius * np.array([np.cos(ang), np.sin(ang), 0])
            points.add(Dot(pos, radius=0.05, color=BLUE_D))

            label = Text(f"ID {task['id']}", font_size=12, color=GRAY_B)
            label.move_to((radius + 0.45) * np.array([np.cos(ang), np.sin(ang), 0]))
            label.rotate(ang + PI / 2)
            labels.add(label)

        group = VGroup(outer, inner, ticks, points, labels)
        group.move_to(DOWN * 0.2)
        group.rotate(PI / 5, axis=RIGHT)
        group.rotate(-PI / 10, axis=UP)

        self.set_camera_orientation(phi=70 * DEGREES, theta=-35 * DEGREES)

        self.play(Write(header), run_time=1)
        self.play(Create(outer), Create(inner), run_time=1.2)
        self.play(LaggedStartMap(Create, ticks, lag_ratio=0.02), run_time=1.5)
        self.play(LaggedStartMap(FadeIn, points, lag_ratio=0.05), run_time=1.0)
        self.play(LaggedStartMap(FadeIn, labels, lag_ratio=0.05), run_time=1.0)
        self.play(Rotate(group, angle=PI / 2, axis=UP), run_time=4, rate_func=linear)
        self.wait(1)


if __name__ == "__main__":
    raise SystemExit(run_filter_cli())
