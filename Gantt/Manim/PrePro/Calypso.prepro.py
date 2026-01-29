from manim import *

class Preproduccion(Scene):
    def construct(self):
        self.camera.background_color = WHITE

        # Estilos
        stroke = BLACK
        fill = "#F2F2F2"
        text_color = BLACK

        def box(label, w=2.6, h=0.9, fs=28):
            r = RoundedRectangle(
                width=w, height=h, corner_radius=0.12,
                stroke_color=stroke, stroke_width=2,
                fill_color=fill, fill_opacity=1
            )
            t = Text(label, font_size=fs, color=text_color)
            t.move_to(r.get_center())
            return VGroup(r, t)

        def cylinder(label, w=1.4, h=1.6, fs=28):
            c = Cylinder(radius=w/2, height=h, direction=OUT)
            c.set_stroke(stroke, 2)
            c.set_fill("#E8E8E8", 1)
            t = Text(label, font_size=fs, color=text_color)
            t.next_to(c, DOWN, buff=0.15)
            return VGroup(c, t)

        # Título
        title = Text("Preproducción", font_size=44, color=text_color).to_edge(UP)
        self.play(Write(title))

        # Arriba: Usuario, VIPs, FS, API
        usuario = box("Usuario", w=3.2, h=0.95, fs=30).next_to(title, DOWN, buff=0.5)
        vip1 = box("VIP1", w=1.6, h=0.75, fs=26).next_to(usuario, DOWN, buff=0.35).shift(LEFT*1.3)
        vip2 = box("VIP2", w=1.6, h=0.75, fs=26).next_to(usuario, DOWN, buff=0.35).shift(RIGHT*1.3)
        fs_box = box("FS", w=2.0, h=0.8, fs=28).next_to(VGroup(vip1, vip2), DOWN, buff=0.25)

        api = Circle(radius=0.45, color=stroke)
        api.set_fill("#E8E8E8", 1)
        api_t = Text("API", font_size=26, color=text_color).move_to(api.get_center())
        api_g = VGroup(api, api_t).next_to(fs_box, LEFT, buff=1.2).shift(UP*0.7)

        self.play(FadeIn(usuario), FadeIn(vip1), FadeIn(vip2), FadeIn(fs_box), FadeIn(api_g))

        a_usuario_vip1 = Arrow(usuario.get_bottom(), vip1.get_top(), buff=0.05, color=stroke)
        a_usuario_vip2 = Arrow(usuario.get_bottom(), vip2.get_top(), buff=0.05, color=stroke)
        a_vips_fs1 = Arrow(vip1.get_bottom(), fs_box.get_top(), buff=0.05, color=stroke)
        a_vips_fs2 = Arrow(vip2.get_bottom(), fs_box.get_top(), buff=0.05, color=stroke)
        a_api_vip1 = Arrow(api_g.get_right(), vip1.get_left(), buff=0.05, color=stroke)

        self.play(Create(a_usuario_vip1), Create(a_usuario_vip2), Create(a_vips_fs1), Create(a_vips_fs2), Create(a_api_vip1))

        # Bloque OpenShift
        openshift = box("OpenShift", w=6.4, h=1.05, fs=30).next_to(fs_box, DOWN, buff=0.6)
        self.play(FadeIn(openshift))

        # Nodos OCP
        ocp1 = box("ocp1", w=1.7, h=0.75, fs=26).next_to(openshift, DOWN, buff=0.35).shift(LEFT*2.2)
        ocp2 = box("ocp2", w=1.7, h=0.75, fs=26).next_to(openshift, DOWN, buff=0.35)
        ocp3 = box("ocp3", w=1.7, h=0.75, fs=26).next_to(openshift, DOWN, buff=0.35).shift(RIGHT*2.2)

        # etcd debajo de cada nodo
        etcd1 = cylinder("etcd", w=1.0, h=1.0, fs=22).scale(0.75).next_to(ocp1, DOWN, buff=0.2)
        etcd2 = cylinder("etcd", w=1.0, h=1.0, fs=22).scale(0.75).next_to(ocp2, DOWN, buff=0.2)
        etcd3 = cylinder("etcd", w=1.0, h=1.0, fs=22).scale(0.75).next_to(ocp3, DOWN, buff=0.2)

        self.play(FadeIn(ocp1), FadeIn(ocp2), FadeIn(ocp3), FadeIn(etcd1), FadeIn(etcd2), FadeIn(etcd3))

        a_fs_openshift = Arrow(fs_box.get_bottom(), openshift.get_top(), buff=0.05, color=stroke)
        self.play(Create(a_fs_openshift))

        # Entornos: DEV, UAT, (opcional INT/TEST como etiqueta)
        env_label = Text("Entornos", font_size=24, color=text_color).next_to(etcd2, DOWN, buff=0.25)
        uat = box("UAT", w=1.9, h=0.75, fs=28).next_to(env_label, DOWN, buff=0.2).shift(LEFT*1.3)
        dev = box("DEV", w=1.9, h=0.75, fs=28).next_to(env_label, DOWN, buff=0.2).shift(RIGHT*1.3)
        it = Text("INT / TEST", font_size=22, color=text_color).next_to(env_label, RIGHT, buff=0.6)

        self.play(Write(env_label), FadeIn(uat), FadeIn(dev), FadeIn(it))

        # Infra / Hypervisor
        infra = box("Infra / Hypervisor", w=6.2, h=1.0, fs=26).next_to(VGroup(uat, dev), DOWN, buff=0.55)
        self.play(FadeIn(infra))

        a_env_infra1 = Arrow(uat.get_bottom(), infra.get_top(), buff=0.05, color=stroke)
        a_env_infra2 = Arrow(dev.get_bottom(), infra.get_top(), buff=0.05, color=stroke)
        self.play(Create(a_env_infra1), Create(a_env_infra2))

        # Storage: 3par y secundario
        storage_3par = cylinder("3par", w=1.6, h=1.9, fs=28).scale(0.9).next_to(infra, DOWN, buff=0.7).shift(LEFT*2.0)
        storage_sec = cylinder("sec", w=1.6, h=1.9, fs=28).scale(0.9).next_to(infra, DOWN, buff=0.7).shift(RIGHT*2.0)
        self.play(FadeIn(storage_3par), FadeIn(storage_sec))

        # Conexiones a storage
        a_infra_3par = Arrow(infra.get_bottom(), storage_3par[0].get_top(), buff=0.1, color=stroke)
        a_infra_sec = Arrow(infra.get_bottom(), storage_sec[0].get_top(), buff=0.1, color=stroke)
        self.play(Create(a_infra_3par), Create(a_infra_sec))

        self.wait(1)

