from manim import *

class CalypsoLandscape(Scene):
    def construct(self):
        # Título
        title = Text("Calypso Integration Landscape", font_size=42, weight=BOLD)
        title.to_edge(UP, buff=0.5)

        # === CALYPSO (Centro) ===
        calypso_box = RoundedRectangle(
            width=3, height=1.5,
            corner_radius=0.2,
            fill_color=BLUE_D,
            fill_opacity=0.8,
            stroke_color=WHITE
        )
        calypso_text = Text("CALYPSO", font_size=28, weight=BOLD)
        calypso = VGroup(calypso_box, calypso_text)
        calypso.move_to(ORIGIN)

        # === INFRAESTRUCTURA CLIENTE (Izquierda) ===
        infra_items = [
            "Active Directory",
            "API Management",
            "Monitoreo",
            "Respaldo"
        ]
        infra_title = Text("INFRAESTRUCTURA", font_size=18, weight=BOLD, color=YELLOW)
        infra_subtitle = Text("CLIENTE", font_size=14, color=YELLOW)
        infra_header = VGroup(infra_title, infra_subtitle).arrange(DOWN, buff=0.1)

        infra_list = VGroup(*[
            Text(f"• {item}", font_size=14) for item in infra_items
        ]).arrange(DOWN, aligned_edge=LEFT, buff=0.15)

        infra_content = VGroup(infra_header, infra_list).arrange(DOWN, buff=0.3)
        infra_box = RoundedRectangle(
            width=3.5, height=3,
            corner_radius=0.2,
            fill_color=GRAY,
            fill_opacity=0.3,
            stroke_color=YELLOW
        )
        infra_box.surround(infra_content, buff=0.3)
        infra = VGroup(infra_box, infra_content)
        infra.to_edge(LEFT, buff=0.5)

        # === SISTEMAS APLICATIVOS INTERNOS (Derecha Arriba) ===
        apps_items = [
            "Motor de pagos",
            "Servicios on-prem",
            "Consultas locales"
        ]
        apps_title = Text("SISTEMAS APLICATIVOS", font_size=16, weight=BOLD, color=GREEN)
        apps_subtitle = Text("INTERNOS", font_size=12, color=GREEN)
        apps_header = VGroup(apps_title, apps_subtitle).arrange(DOWN, buff=0.1)

        apps_list = VGroup(*[
            Text(f"• {item}", font_size=12) for item in apps_items
        ]).arrange(DOWN, aligned_edge=LEFT, buff=0.12)

        apps_content = VGroup(apps_header, apps_list).arrange(DOWN, buff=0.25)
        apps_box = RoundedRectangle(
            width=3.5, height=2.2,
            corner_radius=0.2,
            fill_color=GRAY,
            fill_opacity=0.3,
            stroke_color=GREEN
        )
        apps_box.surround(apps_content, buff=0.25)
        apps = VGroup(apps_box, apps_content)
        apps.to_edge(RIGHT, buff=0.5).shift(UP * 1.5)

        # === PROVEEDORES EXTERNOS (Derecha Abajo) ===
        ext_items = [
            "Bloomberg",
            "NASDAQ",
            "Reuters / SWIFT",
            "Exchanges",
            "Clearing houses"
        ]
        ext_title = Text("PROVEEDORES EXTERNOS", font_size=16, weight=BOLD, color=RED)
        ext_subtitle = Text("PUBLICOS", font_size=12, color=RED)
        ext_header = VGroup(ext_title, ext_subtitle).arrange(DOWN, buff=0.1)

        ext_list = VGroup(*[
            Text(f"• {item}", font_size=12) for item in ext_items
        ]).arrange(DOWN, aligned_edge=LEFT, buff=0.12)

        ext_content = VGroup(ext_header, ext_list).arrange(DOWN, buff=0.25)
        ext_box = RoundedRectangle(
            width=3.5, height=2.8,
            corner_radius=0.2,
            fill_color=GRAY,
            fill_opacity=0.3,
            stroke_color=RED
        )
        ext_box.surround(ext_content, buff=0.25)
        ext = VGroup(ext_box, ext_content)
        ext.to_edge(RIGHT, buff=0.5).shift(DOWN * 1.5)

        # === CONEXIONES ===
        # Línea Calypso <-> Infraestructura
        line_infra = DoubleArrow(
            start=infra_box.get_right(),
            end=calypso_box.get_left(),
            buff=0.1,
            stroke_color=YELLOW,
            tip_length=0.2
        )

        # Línea Calypso <-> Sistemas Aplicativos
        line_apps = DoubleArrow(
            start=calypso_box.get_right() + UP * 0.3,
            end=apps_box.get_left(),
            buff=0.1,
            stroke_color=GREEN,
            tip_length=0.2
        )

        # Línea Calypso <-> Proveedores Externos
        line_ext = DoubleArrow(
            start=calypso_box.get_right() + DOWN * 0.3,
            end=ext_box.get_left(),
            buff=0.1,
            stroke_color=RED,
            tip_length=0.2
        )

        # === ANIMACIONES ===
        # Aparecer título
        self.play(Write(title), run_time=1)
        self.wait(0.5)

        # Aparecer Calypso (el centro)
        self.play(
            FadeIn(calypso_box, scale=0.8),
            Write(calypso_text),
            run_time=1
        )
        self.wait(0.3)

        # Aparecer cajas satélites
        self.play(
            FadeIn(infra, shift=RIGHT),
            FadeIn(apps, shift=LEFT),
            FadeIn(ext, shift=LEFT),
            run_time=1.5
        )
        self.wait(0.3)

        # Aparecer conexiones
        self.play(
            GrowArrow(line_infra),
            GrowArrow(line_apps),
            GrowArrow(line_ext),
            run_time=1
        )

        self.wait(2)


if __name__ == "__main__":
    # Para ejecutar: manim -pql calypso_landscape.py CalypsoLandscape
    pass
