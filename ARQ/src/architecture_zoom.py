from manim import *
import numpy as np

class ArchitectureZoom(Scene):
    def construct(self):
        # Título
        title = Text("Calypso - Arquitectura de Integración", font_size=36, weight=BOLD)
        title.to_edge(UP, buff=0.4)
        self.play(Write(title), run_time=1)

        # === CALYPSO (Centro) ===
        calypso = self.create_calypso_component()
        calypso.scale(0.9).move_to(ORIGIN).shift(RIGHT * 2 + UP * 0.5)

        # === ACTIVE DIRECTORY (Izquierda arriba - Usuarios) ===
        ad_box = self.create_ad_component()
        ad_box.scale(0.75).move_to(LEFT * 4 + UP * 1.5)

        # === APIM (Izquierda abajo - Aplicaciones) ===
        apim_box = self.create_apim_component()
        apim_box.scale(0.75).move_to(LEFT * 4 + DOWN * 1.2)

        # === MONITOREO (Abajo centro - Apoyo técnico) ===
        monitor_box = self.create_monitor_component()
        monitor_box.scale(0.75).move_to(RIGHT * 2 + DOWN * 2.5)

        # === ANIMACIONES ===
        # Aparece Calypso primero (el centro)
        self.play(FadeIn(calypso, scale=0.8), run_time=1)
        self.wait(0.3)

        # Aparecen AD y APIM (entradas)
        self.play(
            FadeIn(ad_box, shift=RIGHT),
            FadeIn(apim_box, shift=RIGHT),
            run_time=1
        )
        self.wait(0.3)

        # Aparece Monitoreo (apoyo)
        self.play(FadeIn(monitor_box, shift=UP), run_time=1)
        self.wait(0.3)

        # Conexiones
        line_ad = Arrow(
            ad_box.get_right(),
            calypso.get_left() + UP * 0.5,
            buff=0.15, stroke_color=YELLOW, tip_length=0.2
        )
        line_apim = Arrow(
            apim_box.get_right(),
            calypso.get_left() + DOWN * 0.3,
            buff=0.15, stroke_color=BLUE, tip_length=0.2
        )
        line_monitor = DashedLine(
            monitor_box.get_top(),
            calypso.get_bottom(),
            stroke_color=GREEN, dash_length=0.1
        )

        # Labels en conexiones
        label_usuarios = Text("Usuarios", font_size=12, color=YELLOW)
        label_usuarios.next_to(line_ad, UP, buff=0.1)

        label_apps = Text("Aplicaciones", font_size=12, color=BLUE)
        label_apps.next_to(line_apim, DOWN, buff=0.1)

        label_soporte = Text("Soporte técnico", font_size=11, color=GREEN)
        label_soporte.next_to(line_monitor, RIGHT, buff=0.1)

        self.play(
            GrowArrow(line_ad),
            GrowArrow(line_apim),
            run_time=0.8
        )
        self.play(
            Write(label_usuarios),
            Write(label_apps),
            run_time=0.5
        )

        self.play(Create(line_monitor), run_time=0.6)
        self.play(Write(label_soporte), run_time=0.4)

        self.wait(2)

    def create_ad_component(self):
        """Active Directory - Usuarios"""
        box = RoundedRectangle(
            width=3, height=2.2,
            corner_radius=0.15,
            fill_color=BLUE_E,
            fill_opacity=0.3,
            stroke_color=YELLOW
        )

        title = Text("Active Directory", font_size=14, weight=BOLD, color=YELLOW)
        title.next_to(box.get_top(), DOWN, buff=0.15)

        # Iconos de usuarios
        users = VGroup()
        for i in range(3):
            head = Circle(radius=0.15, fill_color=WHITE, fill_opacity=0.8, stroke_width=1)
            body = Arc(radius=0.25, start_angle=PI, angle=PI, stroke_color=WHITE, stroke_width=2)
            body.next_to(head, DOWN, buff=0.02)
            user = VGroup(head, body)
            users.add(user)

        users.arrange(RIGHT, buff=0.3)
        users.move_to(box.get_center()).shift(DOWN * 0.15)

        label = Text("Usuarios", font_size=11, color=GRAY_B)
        label.next_to(users, DOWN, buff=0.2)

        return VGroup(box, title, users, label)

    def create_apim_component(self):
        """APIM - Autenticación de aplicaciones"""
        box = RoundedRectangle(
            width=3, height=2.2,
            corner_radius=0.15,
            fill_color=BLUE_E,
            fill_opacity=0.3,
            stroke_color=BLUE
        )

        title = Text("API Management", font_size=14, weight=BOLD, color=BLUE)
        title.next_to(box.get_top(), DOWN, buff=0.15)

        # Icono de llave/candado
        lock_body = Rectangle(width=0.5, height=0.4, fill_color=GOLD, fill_opacity=0.8, stroke_color=GOLD_E)
        lock_arc = Arc(radius=0.2, start_angle=0, angle=PI, stroke_color=GOLD_E, stroke_width=3)
        lock_arc.next_to(lock_body, UP, buff=0)
        lock = VGroup(lock_body, lock_arc)

        # Iconos de apps (cuadrados)
        apps = VGroup()
        for i in range(3):
            app = Square(side_length=0.35, fill_color=BLUE_B, fill_opacity=0.6, stroke_color=BLUE, stroke_width=1)
            apps.add(app)
        apps.arrange(RIGHT, buff=0.2)

        content = VGroup(lock, apps).arrange(DOWN, buff=0.25)
        content.move_to(box.get_center()).shift(DOWN * 0.1)

        label = Text("Aplicaciones", font_size=11, color=GRAY_B)
        label.next_to(apps, DOWN, buff=0.15)

        return VGroup(box, title, content, label)

    def create_monitor_component(self):
        """Monitoreo - Apoyo técnico"""
        box = RoundedRectangle(
            width=4, height=2,
            corner_radius=0.15,
            fill_color=BLUE_E,
            fill_opacity=0.3,
            stroke_color=GREEN
        )

        title = Text("Monitoreo", font_size=14, weight=BOLD, color=GREEN)
        title.next_to(box.get_top(), DOWN, buff=0.12)

        # Panel con curva de métricas
        panel = Rectangle(width=1.8, height=0.8, fill_color=BLACK, fill_opacity=0.5, stroke_color=GREEN_B)

        # Curva de métricas
        x_vals = np.linspace(0, 2 * PI, 50)
        y_vals = 0.2 * np.sin(x_vals) + 0.08 * np.sin(3 * x_vals)
        points = [panel.get_left() + RIGHT * (i / 50) * 1.6 + UP * y + RIGHT * 0.1 for i, y in enumerate(y_vals)]
        curve = VMobject(stroke_color=GREEN, stroke_width=2)
        curve.set_points_smoothly(points)

        # Barras pequeñas
        bars = VGroup()
        for i in range(5):
            h = 0.15 + 0.25 * np.random.random()
            bar = Rectangle(width=0.12, height=h, fill_color=GREEN_B, fill_opacity=0.7, stroke_width=0)
            bars.add(bar)
        bars.arrange(RIGHT, buff=0.08, aligned_edge=DOWN)

        panel_group = VGroup(panel, curve)
        visuals = VGroup(panel_group, bars).arrange(RIGHT, buff=0.3)
        visuals.move_to(box.get_center()).shift(DOWN * 0.1)

        label = Text("Apoyo técnico", font_size=10, color=GRAY_B)
        label.next_to(visuals, DOWN, buff=0.12)

        return VGroup(box, title, visuals, label)

    def create_calypso_component(self):
        """Calypso - Plataforma central"""
        box = RoundedRectangle(
            width=3, height=3.5,
            corner_radius=0.2,
            fill_color=BLUE_D,
            fill_opacity=0.8,
            stroke_color=WHITE,
            stroke_width=2
        )

        title = Text("CALYPSO", font_size=22, weight=BOLD)
        title.move_to(box.get_center()).shift(UP * 1)

        subtitle = Text("Front-to-Back", font_size=13, color=GRAY_B)
        subtitle.next_to(title, DOWN, buff=0.15)

        # Icono (cuadrados conectados vertical)
        squares = VGroup()
        for i in range(3):
            sq = Square(side_length=0.4, fill_color=WHITE, fill_opacity=0.3, stroke_color=WHITE, stroke_width=1)
            squares.add(sq)
        squares.arrange(DOWN, buff=0.2)
        squares.next_to(subtitle, DOWN, buff=0.3)

        lines = VGroup(
            Line(squares[0].get_bottom(), squares[1].get_top(), stroke_color=WHITE, stroke_width=1),
            Line(squares[1].get_bottom(), squares[2].get_top(), stroke_color=WHITE, stroke_width=1)
        )

        return VGroup(box, title, subtitle, squares, lines)


class UserAuthFlow(Scene):
    """Flujo: Usuario → Calypso → AD (consulta/respuesta) - con APIM y Monitoreo visibles"""

    def construct(self):
        # Título
        title = Text("Flujo de Autenticación de Usuario", font_size=32, weight=BOLD)
        title.to_edge(UP, buff=0.4)
        self.play(Write(title), run_time=0.8)

        # === LAYOUT COMPLETO ===

        # USUARIO (Extremo izquierda)
        users_box = self.create_users_box()
        users_box.scale(0.65).move_to(LEFT * 6)

        # AD (Izquierda arriba)
        ad_box = self.create_ad_box()
        ad_box.scale(0.6).move_to(LEFT * 2.5 + UP * 1.8)

        # APIM (Izquierda abajo)
        apim_box = self.create_apim_box()
        apim_box.scale(0.6).move_to(LEFT * 2.5 + DOWN * 1.5)

        # CALYPSO (Centro)
        calypso = self.create_calypso_box()
        calypso.scale(0.7).move_to(RIGHT * 1.5)

        # MONITOREO (Abajo)
        monitor_box = self.create_monitor_box()
        monitor_box.scale(0.55).move_to(RIGHT * 1.5 + DOWN * 2.8)

        # Mostrar todos los componentes
        self.play(
            FadeIn(calypso, scale=0.9),
            run_time=0.6
        )
        self.play(
            FadeIn(ad_box, shift=RIGHT),
            FadeIn(apim_box, shift=RIGHT),
            FadeIn(monitor_box, shift=UP),
            run_time=0.8
        )
        self.play(
            FadeIn(users_box, shift=RIGHT),
            run_time=0.5
        )

        # Conexiones estáticas (login y soporte)
        line_user = Line(
            users_box.get_right(), calypso.get_left(),
            stroke_color=GRAY, stroke_width=2, stroke_opacity=0.6
        )
        line_ad = Line(
            calypso.get_left(), ad_box.get_right(),
            stroke_color=GRAY, stroke_width=2, stroke_opacity=0.6
        )
        line_apim = Arrow(
            apim_box.get_right(), calypso.get_left() + DOWN * 0.4,
            buff=0.1, stroke_color=GRAY, tip_length=0.15, stroke_opacity=0.4
        )
        line_monitor = DashedLine(
            monitor_box.get_top(), calypso.get_bottom(),
            stroke_color=GRAY, dash_length=0.1, stroke_opacity=0.4
        )
        self.play(
            Create(line_user),
            Create(line_ad),
            Create(line_apim),
            Create(line_monitor),
            run_time=0.5
        )

        self.wait(0.3)

        # === FLUJO ANIMADO DE USUARIOS ===

        # 1. Usuario solicita acceso a Calypso
        self.play_flow_step(
            "1. Usuario solicita acceso",
            users_box, calypso,
            color=YELLOW,
            label="Login",
            path=line_user
        )

        # 2. Calypso consulta a AD
        self.emphasize_component(ad_box, color=BLUE)
        self.play_flow_step(
            "2. Calypso consulta AD",
            calypso, ad_box,
            color=BLUE,
            label="¿Válido?",
            path=Line(calypso.get_left(), ad_box.get_right())
        )

        # 3. AD responde a Calypso
        self.emphasize_component(ad_box, color=GREEN)
        self.play_flow_step(
            "3. AD responde",
            ad_box, calypso,
            color=GREEN,
            label="OK ✓",
            path=Line(ad_box.get_right(), calypso.get_left())
        )

        # 4. Calypso responde al usuario
        self.play_flow_step(
            "4. Acceso concedido",
            calypso, users_box,
            color=GREEN,
            label="Bienvenido",
            path=Line(calypso.get_left(), users_box.get_right())
        )

        # Estado autenticado visible
        auth_label = Text("Autenticado ✓", font_size=16, color=GREEN)
        auth_label.next_to(users_box, DOWN, buff=0.25)
        self.play(Write(auth_label), run_time=0.4)

        self.wait(2)

    def play_flow_step(self, step_text, from_obj, to_obj, color, label, path=None):
        """Anima un paso del flujo"""
        # Texto del paso
        step = Text(step_text, font_size=18, color=color)
        step.to_edge(DOWN, buff=0.5)
        self.play(Write(step), run_time=0.4)

        # Crear punto que viaja
        dot = Dot(color=color, radius=0.15)
        dot.move_to(from_obj.get_right() if from_obj.get_center()[0] < to_obj.get_center()[0] else from_obj.get_left())

        # Label del mensaje
        msg_label = Text(label, font_size=14, color=color)
        msg_label.next_to(dot, UP, buff=0.1)
        msg = VGroup(dot, msg_label)

        # Calcular destino
        if path is None:
            if from_obj.get_center()[0] < to_obj.get_center()[0]:
                start = from_obj.get_right()
                end = to_obj.get_left()
            else:
                start = from_obj.get_left()
                end = to_obj.get_right()
        else:
            start = path.get_start()
            end = path.get_end()

        msg.move_to(start)

        self.play(FadeIn(msg, scale=0.5), run_time=0.2)
        if path is None:
            self.play(msg.animate.move_to(end), run_time=0.8)
        else:
            self.play(MoveAlongPath(msg, path), run_time=0.8)
        self.play(FadeOut(msg), FadeOut(step), run_time=0.3)

    def emphasize_component(self, component, color):
        """Resalta un componente para enfatizar su participación en el flujo"""
        highlight = SurroundingRectangle(component, color=color, buff=0.1, stroke_width=3)
        self.play(FadeIn(highlight), run_time=0.2)
        self.play(FadeOut(highlight), run_time=0.3)

    def create_users_box(self):
        """Caja de usuario"""
        box = RoundedRectangle(
            width=2.5, height=3,
            corner_radius=0.15,
            fill_color=GRAY_E,
            fill_opacity=0.4,
            stroke_color=YELLOW
        )

        title = Text("Usuario", font_size=16, weight=BOLD, color=YELLOW)
        title.next_to(box.get_top(), DOWN, buff=0.2)

        # Icono de usuario
        users = VGroup()
        head = Circle(radius=0.2, fill_color=YELLOW, fill_opacity=0.7, stroke_width=1)
        body = Arc(radius=0.3, start_angle=PI, angle=PI, stroke_color=YELLOW, stroke_width=2)
        body.next_to(head, DOWN, buff=0.02)
        user = VGroup(head, body)
        users.add(user)

        users.move_to(box.get_center()).shift(DOWN * 0.2)

        return VGroup(box, title, users)

    def create_calypso_box(self):
        """Caja de Calypso"""
        box = RoundedRectangle(
            width=3, height=3,
            corner_radius=0.2,
            fill_color=BLUE_D,
            fill_opacity=0.8,
            stroke_color=WHITE,
            stroke_width=2
        )

        title = Text("CALYPSO", font_size=20, weight=BOLD)
        title.move_to(box.get_center())

        return VGroup(box, title)

    def create_ad_box(self):
        """Caja de Active Directory"""
        box = RoundedRectangle(
            width=2.5, height=3,
            corner_radius=0.15,
            fill_color=GRAY_E,
            fill_opacity=0.4,
            stroke_color=BLUE
        )

        title = Text("Active", font_size=14, weight=BOLD, color=BLUE)
        title2 = Text("Directory", font_size=14, weight=BOLD, color=BLUE)
        titles = VGroup(title, title2).arrange(DOWN, buff=0.1)
        titles.next_to(box.get_top(), DOWN, buff=0.2)

        # Icono de base de datos
        db = VGroup(
            Ellipse(width=1.2, height=0.4, fill_color=BLUE_B, fill_opacity=0.5, stroke_color=BLUE),
            Rectangle(width=1.2, height=0.8, fill_color=BLUE_B, fill_opacity=0.3, stroke_color=BLUE),
            Ellipse(width=1.2, height=0.4, fill_color=BLUE_B, fill_opacity=0.5, stroke_color=BLUE),
        )
        db[1].next_to(db[0], DOWN, buff=-0.05)
        db[2].next_to(db[1], DOWN, buff=-0.05)
        db.move_to(box.get_center()).shift(DOWN * 0.3)

        return VGroup(box, titles, db)

    def create_apim_box(self):
        """Caja de APIM"""
        box = RoundedRectangle(
            width=2.5, height=2.2,
            corner_radius=0.15,
            fill_color=GRAY_E,
            fill_opacity=0.4,
            stroke_color=BLUE
        )

        title = Text("APIM", font_size=14, weight=BOLD, color=BLUE)
        title.next_to(box.get_top(), DOWN, buff=0.15)

        # Icono candado
        lock_body = Rectangle(width=0.4, height=0.3, fill_color=GOLD, fill_opacity=0.7, stroke_color=GOLD_E)
        lock_arc = Arc(radius=0.15, start_angle=0, angle=PI, stroke_color=GOLD_E, stroke_width=2)
        lock_arc.next_to(lock_body, UP, buff=0)
        lock = VGroup(lock_body, lock_arc)
        lock.move_to(box.get_center()).shift(DOWN * 0.1)

        label = Text("Aplicaciones", font_size=10, color=GRAY_B)
        label.next_to(lock, DOWN, buff=0.2)

        return VGroup(box, title, lock, label)

    def create_monitor_box(self):
        """Caja de Monitoreo"""
        box = RoundedRectangle(
            width=3.5, height=1.8,
            corner_radius=0.15,
            fill_color=GRAY_E,
            fill_opacity=0.4,
            stroke_color=GREEN
        )

        title = Text("Monitoreo", font_size=12, weight=BOLD, color=GREEN)
        title.next_to(box.get_top(), DOWN, buff=0.1)

        # Barras simples
        bars = VGroup()
        for i in range(4):
            h = 0.2 + 0.3 * (i % 3) / 2
            bar = Rectangle(width=0.2, height=h, fill_color=GREEN_B, fill_opacity=0.6, stroke_width=0)
            bars.add(bar)
        bars.arrange(RIGHT, buff=0.15, aligned_edge=DOWN)
        bars.move_to(box.get_center()).shift(DOWN * 0.15)

        return VGroup(box, title, bars)


if __name__ == "__main__":
    # Para ejecutar:
    # manim -pql architecture_zoom.py ArchitectureZoom
    # manim -pql architecture_zoom.py UserAuthFlow
    pass
