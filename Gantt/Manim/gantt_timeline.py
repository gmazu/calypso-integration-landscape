from __future__ import annotations

from datetime import datetime
import ast
from pathlib import Path
from collections import OrderedDict
import textwrap

from manim import *


def load_tasks(path: str) -> list[list]:
    text = Path(path).read_text(encoding="utf-8")
    module = ast.parse(text)
    for node in module.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "tasks":
                    return ast.literal_eval(node.value)
    raise ValueError("tasks list not found")


class GanttTimelineLevel2(Scene):
    def construct(self):
        tasks = load_tasks("../Backup/smartsheet_PRE_v1.txt")
        level2 = [row for row in tasks if row[1] == 2]

        dated = []
        undated = []
        for row in level2:
            task_id, _, name, *_rest, start, end, _pct, _dur, _pred = row
            if start and end:
                dated.append(
                    {
                        "id": task_id,
                        "name": name,
                        "start": datetime.strptime(start, "%d/%m/%y"),
                        "end": datetime.strptime(end, "%d/%m/%y"),
                        "start_str": start,
                        "end_str": end,
                    }
                )
            else:
                undated.append({"id": task_id, "name": name})

        dated.sort(key=lambda t: t["start"])

        title = Text("Hablitación Plataforma Calypso Banco BCI", font_size=34, weight=BOLD)
        subtitle = Text("Ambiente Pre Productivo", font_size=18, color=GRAY_B)
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

        points = VGroup()
        stems = VGroup()
        labels = VGroup()
        dates = VGroup()

        grouped = OrderedDict()
        for task in dated:
            key = task["start"].date()
            grouped.setdefault(key, []).append(task)

        above_idx = 0
        below_idx = 0

        above_idx = 0
        below_idx = 0

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

            stem_end_y = y + (stem_len if above else -stem_len)
            stem = Line([x, y, 0], [x, stem_end_y, 0], color=GRAY_B, stroke_width=1)

            date_text = tasks_for_date[0]["start"].strftime("%d/%m")
            date_label = Text(date_text, font_size=12, color=BLUE_D)
            date_label.next_to(point, DOWN if above else UP, buff=0.1)

            offsets = [1.0, 1.5, 2.0] if len(tasks_for_date) > 1 else [stem_len + 0.2]
            for t_idx, task in enumerate(tasks_for_date):
                offset = offsets[t_idx] if t_idx < len(offsets) else offsets[-1]
                target_y = y + (offset if above else -offset)

                title = Text(f"ID {task['id']}", font_size=12, weight=BOLD)
                wrapped_name = textwrap.fill(task["name"], width=28)
                body = Text(wrapped_name, font_size=12, color=GRAY_B, line_spacing=0.9)
                text_block = VGroup(title, body).arrange(DOWN, buff=0.08, aligned_edge=LEFT)

                text_block.move_to([x, target_y, 0])
                labels.add(text_block)

            points.add(point)
            stems.add(stem)
            dates.add(date_label)

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
        self.play(LaggedStartMap(FadeIn, points, lag_ratio=0.05), run_time=0.9)
        self.play(LaggedStartMap(Create, stems, lag_ratio=0.05), run_time=1.0)
        self.play(LaggedStartMap(FadeIn, dates, lag_ratio=0.05), run_time=0.8)
        self.play(LaggedStartMap(FadeIn, labels, lag_ratio=0.05), run_time=1.2)

        if undated_block:
            self.play(FadeIn(undated_block), run_time=0.6)

        self.wait(2)


class GanttTimelineCircular(ThreeDScene):
    def construct(self):
        tasks = load_tasks("Gantt/smartsheet_PRE_v1.txt")
        level2 = [row for row in tasks if row[1] == 2]

        dated = []
        for row in level2:
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

        title = Text("Hablitación Plataforma Calypso Banco BCI", font_size=32, weight=BOLD)
        subtitle = Text("Ambiente Pre Productivo", font_size=18, color=GRAY_B)
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
    # manim -pql Gantt/Manim/gantt_timeline.py GanttTimelineLevel2
    # manim -pql Gantt/Manim/gantt_timeline.py GanttTimelineCircular
    pass
