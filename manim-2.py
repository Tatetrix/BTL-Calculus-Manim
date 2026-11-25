from manim import *
import numpy as np

# ==============================================================================
# 0. QUY ƯỚC KỸ THUẬT & BẢNG MÀU THỐNG NHẤT TOÀN VIDEO
# ==============================================================================
config.background_color = "#0F1117"

C_CURVE = BLUE      # Đường cong y = f(x), giá trị thực Δy
C_TAN = YELLOW      # Tiếp tuyến, vi phân ước tính dy
C_ERR = RED         # Khoảng hở, sai số, ngưỡng 5%, vùng Invalid
C_OK = GREEN        # Điểm hợp lệ, vùng tốt
C_SUB = GREY        # Trục, lưới, chữ phụ


# ==============================================================================
# 1. SCENE 1: ERRORS IN EVERYDAY LIFE (0:00 – 1:00)
# ==============================================================================
class S01_Intro(Scene):
    def construct(self):
        # 0:00–0:12: Tiêu đề mở đầu
        title = Text(
            "Differentials, Linearization and\nError Propagation in Measurement",
            font_size=36, color=WHITE, weight=BOLD
        )
        subtitle = Text(
            "Calculus 1 · Group 4 – CC01",
            font_size=22, color=C_SUB
        ).next_to(title, DOWN, buff=0.3)

        self.play(Write(title), FadeIn(subtitle, shift=UP * 0.2), run_time=2.0)
        self.wait(1.0)
        self.play(FadeOut(title, shift=UP * 0.6),
                  FadeOut(subtitle, shift=UP * 0.6))

        # Ba dụng cụ đo vẽ bằng VGroup: thước kẻ, đồng hồ bấm giây, cân đĩa
        ruler_body = Rectangle(width=3.6, height=0.65,
                               color=C_SUB, fill_opacity=0.2)
        ticks = VGroup(*[
            Line(
                UP * 0.325,
                UP * (0.14 if i % 5 != 0 else 0.02),
                color=WHITE, stroke_width=1.5
            ).move_to(ruler_body.get_top() + LEFT * 1.6 + RIGHT * i * 0.16, aligned_edge=UP)
            for i in range(21)
        ])
        ruler_lbl = Text("Ruler", font_size=20, color=C_SUB).next_to(
            ruler_body, UP, buff=0.2)
        ruler = VGroup(ruler_body, ticks, ruler_lbl).shift(
            LEFT * 4.3 + UP * 0.8)

        watch_circle = Circle(radius=0.65, color=C_SUB, fill_opacity=0.2)
        watch_btn = Rectangle(width=0.24, height=0.14, color=C_SUB,
                              fill_opacity=0.7).next_to(watch_circle, UP, buff=0)
        watch_hand = Line(
            watch_circle.get_center(),
            watch_circle.get_center() + UP * 0.45 + RIGHT * 0.22,
            color=C_TAN, stroke_width=3
        )
        watch_lbl = Text("Stopwatch", font_size=20, color=C_SUB).next_to(
            watch_btn, UP, buff=0.2)
        stopwatch = VGroup(watch_circle, watch_btn,
                           watch_hand, watch_lbl).shift(UP * 0.8)

        scale_base = Triangle(color=C_SUB, fill_opacity=0.4).scale(
            0.35).shift(RIGHT * 4.3 + UP * 0.35)
        scale_beam = Line(LEFT * 0.9, RIGHT * 0.9, color=WHITE,
                          stroke_width=3).next_to(scale_base, UP, buff=0)
        pan_l = Arc(radius=0.35, start_angle=PI, angle=PI, color=C_SUB).next_to(
            scale_beam.get_left(), DOWN, buff=0.15)
        pan_r = Arc(radius=0.35, start_angle=PI, angle=PI, color=C_SUB).next_to(
            scale_beam.get_right(), DOWN, buff=0.15)
        scale_lbl = Text("Scale", font_size=20, color=C_SUB).next_to(
            scale_beam, UP, buff=0.35)
        scale = VGroup(scale_base, scale_beam, pan_l, pan_r, scale_lbl)

        self.play(Create(ruler), Create(stopwatch),
                  Create(scale), run_time=2.0)

        # 0:12–0:25: Vùng mờ đỏ ±Δx quanh giá trị đọc trên cả 3 dụng cụ
        err_r = Rectangle(width=0.55, height=0.65, color=C_ERR, fill_opacity=0.3, stroke_width=1.5).move_to(
            ruler_body.get_center() + RIGHT * 0.25
        )
        lbl_dx = MathTex(r"\pm \Delta x", font_size=26,
                         color=C_ERR).next_to(err_r, DOWN, buff=0.2)
        err_w = Sector(radius=0.65, start_angle=PI / 5, angle=PI / 4, color=C_ERR, fill_opacity=0.3).move_arc_center_to(
            watch_circle.get_center()
        )
        err_s = Rectangle(width=0.7, height=0.35, color=C_ERR,
                          fill_opacity=0.3, stroke_width=0).move_to(pan_r.get_center())

        self.play(FadeIn(err_r), Write(lbl_dx), FadeIn(
            err_w), FadeIn(err_s), run_time=1.8)
        self.wait(1.5)
        self.play(FadeOut(ruler, stopwatch, scale,
                  err_r, lbl_dx, err_w, err_s))

        # 0:25–0:42: So sánh 1 cm trên bàn 60 cm vs sân bóng 100 m
        bar_table = Rectangle(width=3.8, height=0.45, color=C_CURVE,
                              fill_opacity=0.3).shift(UP * 1.4 + LEFT * 2.1)
        err_table = Rectangle(width=0.24, height=0.45, color=C_ERR,
                              fill_opacity=0.9, stroke_width=0).align_to(bar_table, RIGHT)
        txt_table = VGroup(
            Text("Tabletop (60 cm)", font_size=21, color=WHITE),
            MathTex(r"1\text{ cm} / 60\text{ cm} \approx 1.7\%",
                    font_size=26, color=C_TAN)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1).next_to(bar_table, RIGHT, buff=0.45)

        bar_field = Rectangle(width=6.4, height=0.45, color=C_CURVE,
                              fill_opacity=0.3).shift(DOWN * 0.1 + LEFT * 0.8)
        err_field = Rectangle(width=0.06, height=0.45, color=C_ERR,
                              fill_opacity=0.95, stroke_width=0).align_to(bar_field, RIGHT)
        txt_field = VGroup(
            Text("Football field (100 m)", font_size=21, color=WHITE),
            MathTex(r"1\text{ cm} / 100\text{ m} = 0.01\%",
                    font_size=26, color=C_OK)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1).next_to(bar_field, RIGHT, buff=0.45)

        notes = VGroup(
            Text("Absolute error = 1 cm (same unit size)",
                 font_size=21, color=C_ERR),
            Text("Relative error = percentage (very different meaning)",
                 font_size=21, color=C_TAN)
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=1.3)

        self.play(Create(bar_table), FadeIn(err_table),
                  Write(txt_table), run_time=1.5)
        self.play(Create(bar_field), FadeIn(err_field),
                  Write(txt_field), run_time=1.5)
        self.play(FadeIn(notes), run_time=1.0)
        self.wait(2.0)
        self.play(FadeOut(bar_table, err_table, txt_table,
                  bar_field, err_field, txt_field, notes))

        # 0:42–1:00: Sơ đồ 3 khối [x = a ± Δx] -> [y = f(x)] -> [y ± ?]
        b1 = VGroup(
            RoundedRectangle(
                width=3.2, height=1.1, corner_radius=0.15, color=C_CURVE, fill_opacity=0.12),
            MathTex(r"x = a \pm \Delta x", font_size=30, color=WHITE)
        )
        a1 = Arrow(LEFT, RIGHT, color=C_SUB).scale(0.7)
        b2 = VGroup(
            RoundedRectangle(width=2.8, height=1.1,
                             corner_radius=0.15, color=C_TAN, fill_opacity=0.12),
            MathTex(r"y = f(x)", font_size=30, color=WHITE)
        )
        a2 = Arrow(LEFT, RIGHT, color=C_SUB).scale(0.7)
        q_mark = MathTex(r"y \pm ?", font_size=32, color=C_ERR)
        b3 = VGroup(
            RoundedRectangle(width=2.8, height=1.1,
                             corner_radius=0.15, color=C_ERR, fill_opacity=0.12),
            q_mark
        )

        pipeline = VGroup(b1, a1, b2, a2, b3).arrange(RIGHT, buff=0.3)
        self.play(FadeIn(b1, shift=RIGHT * 0.25))
        self.play(GrowArrow(a1), FadeIn(b2, shift=RIGHT * 0.25))
        self.play(GrowArrow(a2), FadeIn(b3, shift=RIGHT * 0.25))
        self.play(Indicate(q_mark, color=C_ERR,
                  scale_factor=1.35), run_time=1.2)
        self.wait(1.0)


# ==============================================================================
# 1B. TABLE OF CONTENTS (NGAY SAU INTRODUCTION)
# ==============================================================================
class S01_TableOfContents(Scene):
    def construct(self):
        header = Text("Table of Contents", font_size=36,
                      color=WHITE, weight=BOLD).to_edge(UP, buff=0.65)
        underline = Line(LEFT * 2.5, RIGHT * 2.5, color=C_TAN,
                         stroke_width=3).next_to(header, DOWN, buff=0.15)

        sections = [
            ("01", "Theoretical Foundation",
             "Tangent approximation, Absolute & Relative Error Laws, 5% Limit", C_CURVE),
            ("02", "Case Study 1: Circular Tabletop",
             "Material trim estimation & validity bound (Δr ≤ 5.71 cm)", C_TAN),
            ("03", "Case Study 2: Tree Height Measurement",
             "Clinometer error analysis & optimal standing zone (15–20 m)", C_OK),
            ("04", "Conclusion & Further Work",
             "Key takeaways, model limits & multivariable extensions", C_SUB),
        ]

        cards = VGroup()
        for num, sec_title, desc, col in sections:
            badge = VGroup(
                RoundedRectangle(width=0.85, height=0.85,
                                 corner_radius=0.15, color=col, fill_opacity=0.2),
                Text(num, font_size=26, color=col, weight=BOLD)
            )
            txt_grp = VGroup(
                Text(sec_title, font_size=25, color=WHITE, weight=BOLD),
                Text(desc, font_size=18, color=C_SUB)
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.08)

            row_box = RoundedRectangle(
                width=10.8, height=1.05, corner_radius=0.15, color=C_SUB, stroke_opacity=0.35, fill_opacity=0.06)
            row_content = VGroup(badge, txt_grp).arrange(RIGHT, buff=0.4).move_to(
                row_box.get_left() + RIGHT * 0.3, aligned_edge=LEFT)
            cards.add(VGroup(row_box, row_content))

        cards.arrange(DOWN, buff=0.25).next_to(underline, DOWN, buff=0.45)

        self.play(Write(header), Create(underline), run_time=1.0)
        for card in cards:
            self.play(FadeIn(card, shift=RIGHT * 0.3), run_time=0.65)
        self.wait(2.2)
        self.play(FadeOut(header, underline, cards))


# ==============================================================================
# 2. SCENE 2: REPLACE THE CURVE BY ITS TANGENT (1:00 – 1:50)
# ==============================================================================
class S02_Idea(MovingCameraScene):
    def construct(self):
        # 1:00–1:12: Đồ thị f(x) mượt và điểm x = a
        axes = Axes(
            x_range=[0, 5, 1], y_range=[0, 4.5, 1],
            x_length=6.6, y_length=4.6,
            axis_config={"color": C_SUB}
        ).to_edge(LEFT, buff=0.55)

        def f(x): return 0.1 * x**3 - 0.45 * x**2 + 0.8 * x + 0.8
        def df(x): return 0.3 * x**2 - 0.9 * x + 0.8
        a = 2.8

        curve = axes.plot(f, x_range=[0.2, 4.5],
                          color=C_CURVE, stroke_width=3.5)
        dot_a = Dot(axes.c2p(a, f(a)), color=WHITE)
        drop_a = DashedLine(axes.c2p(a, 0), axes.c2p(a, f(a)), color=C_SUB)
        lbl_a = MathTex("a", font_size=24).next_to(
            axes.c2p(a, 0), DOWN, buff=0.15)

        self.play(Create(axes), Create(curve), FadeIn(
            dot_a, drop_a, lbl_a), run_time=2.0)

        # 1:12–1:22: MovingCameraScene zoom cận cảnh + tiếp tuyến vàng
        tangent = axes.plot(
            lambda x: f(a) + df(a) * (x - a),
            x_range=[0.8, 4.5], color=C_TAN, stroke_width=2.5
        )
        self.camera.frame.save_state()
        self.play(self.camera.frame.animate.scale(
            0.12).move_to(dot_a.get_center()), run_time=2.0)
        self.play(Create(tangent), run_time=1.2)
        self.wait(0.8)
        self.play(Restore(self.camera.frame), run_time=1.8)

        # 1:22–1:36: Đánh dấu a + Δx, đoạn đứng Δy (BLUE), dy (YELLOW), khoảng hở (RED)
        dx = 1.2
        x2 = a + dx
        p_base = axes.c2p(x2, f(a))
        p_tan = axes.c2p(x2, f(a) + df(a) * dx)
        p_cur = axes.c2p(x2, f(x2))

        h_dash = DashedLine(axes.c2p(a, f(a)), p_base, color=C_SUB)
        lbl_x2 = MathTex(
            r"a+\Delta x", font_size=22).next_to(axes.c2p(x2, 0), DOWN, buff=0.15)
        bar_dy = Line(p_base, p_tan, color=C_TAN, stroke_width=5)
        bar_gap = Line(p_tan, p_cur, color=C_ERR, stroke_width=5)

        lbl_inc = MathTex(r"\Delta y = f(a+\Delta x) - f(a)",
                          font_size=24, color=C_CURVE)
        lbl_dif = MathTex(
            r"\mathrm{d}y = f'(a)\Delta x", font_size=24, color=C_TAN)
        lbl_lin = MathTex(r"L(x) = f(a) + f'(a)(x-a)",
                          font_size=24, color=C_OK)

        # 1:36–1:50: Linearization + 3 thẻ giả thiết (RoundedRectangle)
        h_cards = VGroup(*[
            VGroup(
                RoundedRectangle(
                    width=5.3, height=0.6, corner_radius=0.12, color=C_SUB, fill_opacity=0.15),
                Text(txt, font_size=19, color=WHITE)
            )
            for txt in [
                "(H1) f is differentiable near a",
                "(H2) Δx is small compared to |a|",
                "(H3) f(a) ≠ 0 (for relative errors)"
            ]
        ]).arrange(DOWN, buff=0.18)

        right_col = VGroup(lbl_inc, lbl_dif, lbl_lin, h_cards).arrange(
            DOWN, aligned_edge=LEFT, buff=0.28
        ).to_edge(RIGHT, buff=0.4)

        self.play(Create(h_dash), Write(lbl_x2), Create(
            bar_dy), Create(bar_gap), run_time=1.8)
        self.play(Write(lbl_inc), Write(lbl_dif), run_time=1.5)
        self.play(TransformMatchingTex(lbl_dif.copy(), lbl_lin), run_time=1.2)
        for card in h_cards:
            self.play(FadeIn(card, shift=LEFT * 0.35), run_time=0.55)
        self.wait(1.5)


# ==============================================================================
# 3. SCENE 3: ABSOLUTE-ERROR LAW (1:50 – 2:30)
# ==============================================================================
class S03_AbsError(Scene):
    def construct(self):
        # 1:50–2:02: Mô phỏng 2 biến L = x1 - x2 (tại sao cần trị tuyệt đối)
        header_2v = Text("Why Absolute Value? Example: L = x₁ − x₂",
                         font_size=28, color=C_TAN).to_edge(UP, buff=0.45)
        sub_2v = Text("Two variables: beyond this video",
                      font_size=20, color=C_SUB).to_edge(DOWN, buff=0.45)
        self.play(Write(header_2v), FadeIn(sub_2v))

        s1 = ValueTracker(0.0)
        s2 = ValueTracker(0.0)

        bars_2v = always_redraw(lambda: VGroup(
            Line([-4.2, 1.3, 0], [0.6 + s1.get_value(), 1.3, 0],
                 color=C_CURVE, stroke_width=10),
            MathTex(r"x_1", font_size=26, color=C_CURVE).move_to(
                [-4.6, 1.3, 0]),
            Line([-4.2, 0.3, 0], [-1.4 + s2.get_value(), 0.3, 0],
                 color=C_OK, stroke_width=10),
            MathTex(r"x_2", font_size=26, color=C_OK).move_to([-4.6, 0.3, 0]),
            Line([-1.4 + s2.get_value(), -0.9, 0], [0.6 +
                 s1.get_value(), -0.9, 0], color=C_TAN, stroke_width=12),
            MathTex(r"L = x_1 - x_2", font_size=26,
                    color=C_TAN).move_to([-4.2, -0.9, 0])
        ))
        self.add(bars_2v)
        self.wait(0.6)

        # x1 lùi trái (-0.65), x2 tiến phải (+0.65) -> L co lại đoạn đỏ Δx1 + Δx2
        self.play(s1.animate.set_value(-0.65),
                  s2.animate.set_value(0.65), run_time=2.0)
        shrink_red = Line([-0.05, -0.9, 0], [1.25, -0.9, 0],
                          color=C_ERR, stroke_width=12)
        wrong_eq = MathTex(r"\Delta x_1 - \Delta x_2 = 0",
                           font_size=26, color=C_SUB).shift(RIGHT * 3.5 + UP * 0.8)
        cross = Cross(wrong_eq, stroke_color=C_ERR, stroke_width=3)
        right_eq = MathTex(r"|\Delta L|_{\max} = \Delta x_1 + \Delta x_2",
                           font_size=28, color=C_ERR).next_to(wrong_eq, DOWN, buff=0.4)

        self.play(Create(shrink_red), Write(wrong_eq))
        self.play(Create(cross), Write(right_eq))
        self.wait(1.8)
        self.play(FadeOut(header_2v, sub_2v, bars_2v,
                  shrink_red, wrong_eq, cross, right_eq))

        # 2:02–2:30: Đồ thị 1 biến, ValueTracker Δx chạy từ -1 đến +1 và ngược lại
        axes = Axes(
            x_range=[0, 4.5, 1], y_range=[0, 5, 1],
            x_length=6.5, y_length=4.5,
            axis_config={"color": C_SUB}
        ).to_edge(LEFT, buff=0.55)
        def f(x): return 0.25 * x**2 + 0.6
        def df(x): return 0.5 * x
        a = 2.2
        dx_tr = ValueTracker(0.85)

        curve = axes.plot(f, x_range=[0.3, 4.1], color=C_CURVE, stroke_width=3)
        tangent = axes.plot(lambda x: f(a) + df(a) * (x - a),
                            x_range=[0.3, 4.1], color=C_TAN, stroke_width=2.5)
        dot_a = Dot(axes.c2p(a, f(a)), color=WHITE)

        def dyn_abs():
            dx = dx_tr.get_value()
            x_cur = a + dx
            y_tan = f(a) + df(a) * dx
            v_bar = Line(axes.c2p(x_cur, f(a)), axes.c2p(
                x_cur, y_tan), color=C_TAN, stroke_width=6)
            h_dash = DashedLine(axes.c2p(a, f(a)),
                                axes.c2p(x_cur, f(a)), color=C_SUB)
            sign_lbl = MathTex(r"(+)" if dx >= 0 else r"(-)", font_size=24, color=C_TAN).next_to(
                v_bar, RIGHT if dx >= 0 else LEFT, buff=0.12
            )
            return VGroup(h_dash, v_bar, sign_lbl)

        anim_grp = always_redraw(dyn_abs)
        self.play(Create(axes), Create(curve), Create(tangent), FadeIn(dot_a))
        self.add(anim_grp)
        self.play(dx_tr.animate.set_value(-0.85), run_time=1.8)
        self.play(dx_tr.animate.set_value(0.85), run_time=1.8)

        # Khóa hai dải vàng đối xứng quanh f(a) & đóng khung Theorem 1
        band_up = Line(axes.c2p(0, f(a)), axes.c2p(
            0, f(a) + df(a) * 0.85), color=C_TAN, stroke_width=8)
        band_dn = Line(axes.c2p(0, f(a)), axes.c2p(
            0, f(a) - df(a) * 0.85), color=C_TAN, stroke_width=8)

        thm1_box = VGroup(
            RoundedRectangle(width=5.4, height=1.35,
                             corner_radius=0.15, color=C_TAN, fill_opacity=0.12),
            MathTex(r"|\Delta y| \approx |f'(a)|\,\Delta x",
                    font_size=34, color=C_TAN)
        )
        thm1_title = Text("Theorem 1: Absolute-Error Law",
                          font_size=26, color=WHITE, weight=BOLD)
        amp_lbl = MathTex(
            r"|f'(a)| = \text{error amplifier}", font_size=25, color=C_ERR)

        right_panel = VGroup(thm1_title, thm1_box, amp_lbl).arrange(
            DOWN, aligned_edge=LEFT, buff=0.35
        ).to_edge(RIGHT, buff=0.45)

        self.play(Create(band_up), Create(band_dn), FadeIn(
            right_panel, shift=LEFT * 0.3), run_time=1.5)
        self.wait(1.8)


# ==============================================================================
# 4. SCENE 4: RELATIVE-ERROR LAW (2:30 – 3:05)
# ==============================================================================
class S04_RelError(Scene):
    def construct(self):
        title = Text("Theorem 2: Relative-Error Law", font_size=32,
                     color=C_TAN, weight=BOLD).to_edge(UP, buff=0.55)
        eq_start = MathTex(r"|\Delta y|", r"\approx", r"|f'(a)|\,\Delta x",
                           font_size=36, color=C_TAN).shift(UP * 1.4)
        eq_div = MathTex(r"\frac{|\Delta y|}{|f(a)|}", r"\approx",
                         r"\left|\frac{f'(a)}{f(a)}\right|\Delta x", font_size=36, color=WHITE).shift(UP * 1.4)
        eq_thm2 = MathTex(
            r"\delta y \approx \left|\frac{f'(a)}{f(a)}\right|\Delta x = |\mathrm{d}(\ln|f(a)|)|",
            font_size=34, color=C_OK
        ).next_to(eq_div, DOWN, buff=0.45)

        self.play(Write(title), Write(eq_start))
        self.wait(0.8)
        self.play(TransformMatchingTex(eq_start, eq_div), run_time=1.2)
        self.play(Write(eq_thm2), run_time=1.3)
        self.wait(1.0)

        # 2:45–3:05: Ví dụ y = 5x^3 tại x = 4.00, δx = 1.5%
        ex_card = RoundedRectangle(width=11.0, height=2.5, corner_radius=0.18,
                                   color=C_CURVE, fill_opacity=0.1).to_edge(DOWN, buff=0.7)
        line1 = MathTex(
            r"\text{Example: } y = 5x^3 \implies \ln y = \ln 5 + 3\ln x \implies \mathrm{d}(\ln y) = 3\frac{\mathrm{d}x}{x}", font_size=26, color=WHITE)
        dx_tex = MathTex(r"\delta x = 1.5\%", font_size=30, color=C_CURVE)
        dy_tex = MathTex(r"\delta y = 4.5\%", font_size=32, color=C_TAN)
        row2 = VGroup(dx_tex, dy_tex).arrange(RIGHT, buff=2.2)

        ex_content = VGroup(line1, row2).arrange(
            DOWN, buff=0.55).move_to(ex_card)
        curved_arrow = CurvedArrow(
            dx_tex.get_right() + RIGHT * 0.15,
            dy_tex.get_left() + LEFT * 0.15,
            angle=-0.45,
            color=C_TAN
        )
        mult_lbl = MathTex(r"\times 3", font_size=28, color=C_TAN).next_to(
            curved_arrow, UP, buff=0.1)

        self.play(Create(ex_card), Write(line1), FadeIn(dx_tex), run_time=1.4)
        self.play(Create(curved_arrow), Write(
            mult_lbl), FadeIn(dy_tex), run_time=1.4)
        self.wait(2.0)


# ==============================================================================
# 5. SCENE 5: WHY IT WORKS, AND WHEN IT FAILS (3:05 – 3:55)
# ==============================================================================
class S05_Limits(Scene):
    def construct(self):
        # 3:05–3:30: Cát tuyến trắng xoay dần về trùng tiếp tuyến vàng khi Δx -> 0
        axes = Axes(
            x_range=[0, 5, 1], y_range=[0, 4.5, 1],
            x_length=6.5, y_length=4.5,
            axis_config={"color": C_SUB}
        ).to_edge(LEFT, buff=0.55)
        def f(x): return 0.1 * x**3 - 0.45 * x**2 + 0.8 * x + 0.8
        def df(x): return 0.3 * x**2 - 0.9 * x + 0.8
        a = 2.8
        dx_tr = ValueTracker(1.3)

        curve = axes.plot(f, x_range=[0.2, 4.5],
                          color=C_CURVE, stroke_width=3.5)
        tangent = axes.plot(lambda x: f(a) + df(a) * (x - a),
                            x_range=[0.8, 4.5], color=C_TAN, stroke_width=2.5)

        def get_secant():
            dx = dx_tr.get_value()
            x2 = a + dx
            slope = (f(x2) - f(a)) / dx
            sec = axes.plot(lambda x: f(a) + slope * (x - a),
                            x_range=[0.8, 4.5], color=WHITE, stroke_width=2.5)
            gap = Line(axes.c2p(x2, f(a) + df(a) * dx),
                       axes.c2p(x2, f(x2)), color=C_ERR, stroke_width=6)
            d1 = Dot(axes.c2p(a, f(a)), color=WHITE)
            d2 = Dot(axes.c2p(x2, f(x2)), color=WHITE)
            return VGroup(sec, gap, d1, d2)

        sec_anim = always_redraw(get_secant)
        proof_box = VGroup(
            Text("Why does it work?", font_size=28, color=WHITE, weight=BOLD),
            Text("Secant rotates into tangent", font_size=21, color=C_SUB),
            MathTex(
                r"\Delta y = \mathrm{d}y + \varepsilon \cdot \Delta x", font_size=30, color=C_TAN),
            MathTex(r"\lim_{\Delta x \to 0} \varepsilon = 0",
                    font_size=28, color=C_OK),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.55)

        self.play(Create(axes), Create(curve),
                  Create(tangent), FadeIn(proof_box))
        self.add(sec_anim)
        self.play(dx_tr.animate.set_value(0.1), run_time=3.5)
        self.wait(1.0)
        self.play(FadeOut(axes, curve, tangent, sec_anim, proof_box))

        # 3:30–3:55: Phản ví dụ y = sin(x) tại x = 0, Δx = 1 rad -> Chốt ngưỡng 5%
        axes2 = Axes(
            x_range=[-0.2, 1.5, 0.5], y_range=[-0.1, 1.3, 0.5],
            x_length=6.2, y_length=4.4,
            axis_config={"color": C_SUB}
        ).to_edge(LEFT, buff=0.55)
        sin_c = axes2.plot(
            np.sin, x_range=[0, 1.4], color=C_CURVE, stroke_width=3.5)
        tan_c = axes2.plot(lambda x: x, x_range=[
                           0, 1.2], color=C_TAN, stroke_width=2.5)

        bar_true = Line(axes2.c2p(1.0, 0), axes2.c2p(
            1.0, np.sin(1.0)), color=C_CURVE, stroke_width=8)
        bar_err = Line(axes2.c2p(1.0, np.sin(1.0)), axes2.c2p(
            1.0, 1.0), color=C_ERR, stroke_width=8)
        lbl_err = Text("Discrepancy ≈ 18.8%", font_size=22, color=C_ERR,
                       weight=BOLD).next_to(bar_err, RIGHT, buff=0.15)

        rule_rect = RoundedRectangle(
            width=5.4, height=1.35, corner_radius=0.15, color=C_OK, fill_opacity=0.15)
        rule_tex = MathTex(r"\frac{|\Delta y - \mathrm{d}y|}{|\Delta y|} < 5\% \implies \text{Accept}",
                           font_size=26, color=C_OK).move_to(rule_rect)
        rule_card = VGroup(rule_rect, rule_tex)

        right_fail = VGroup(
            Text("When does it fail?", font_size=28, color=C_ERR, weight=BOLD),
            MathTex(
                r"y = \sin x,\ a = 0,\ \Delta x = 1\text{ rad}", font_size=25),
            MathTex(
                r"\mathrm{d}y = 1.000 \quad \text{vs} \quad \Delta y \approx 0.8415", font_size=24, color=C_TAN),
            rule_card
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).to_edge(RIGHT, buff=0.45)

        self.play(Create(axes2), Create(sin_c), Create(tan_c))
        self.play(Create(bar_true), Create(bar_err),
                  Write(lbl_err), FadeIn(right_fail))
        self.wait(2.5)


# ==============================================================================
# 6. SCENE 6: CASE 1 — CIRCULAR TABLETOP (3:55 – 5:20)
# ==============================================================================
class S06_Tabletop(MovingCameraScene):
    def construct(self):
        # 3:55–4:10: Hình tròn bán kính r0 = 60 cm + thông số
        outer = Circle(radius=1.9, color=C_CURVE, fill_opacity=0.25,
                       stroke_width=2.5).shift(LEFT * 3.5 + UP * 0.2)
        rad_line = Line(outer.get_center(), outer.get_right(),
                        color=WHITE, stroke_width=2.5)
        brace_r = Brace(rad_line, DOWN, buff=0.1)
        lbl_r = MathTex(r"r_0 = 60\text{ cm}", font_size=24).next_to(
            brace_r, DOWN, buff=0.1)

        info_top = VGroup(
            Text("Case Study 1: Circular Tabletop",
                 font_size=27, color=C_CURVE, weight=BOLD),
            MathTex(
                r"p = 50\text{ VND/cm}^2, \quad \text{Paid} = 565{,}200\text{ VND}", font_size=24),
            Text("Artisan trims Δr = 1 cm",
                 font_size=23, color=C_ERR, weight=BOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(RIGHT, buff=0.55).to_edge(UP, buff=0.55)

        self.play(Create(outer), Create(rad_line), GrowFromCenter(
            brace_r), Write(lbl_r), FadeIn(info_top))
        self.wait(1.0)

        # 4:10–4:30: Tô vành ngoài Δr = 1 cm bằng Annulus đỏ + Zoom camera vào cung vành khăn
        ring = Annulus(inner_radius=1.65, outer_radius=1.9,
                       color=C_ERR, fill_opacity=0.55).move_to(outer.get_center())
        da_eq = MathTex(r"\mathrm{d}A = 2\pi r\,\Delta r", font_size=28, color=C_TAN).next_to(
            outer, DOWN, buff=0.35)

        self.play(FadeIn(ring), Write(da_eq))
        self.camera.frame.save_state()
        self.play(self.camera.frame.animate.scale(
            0.35).move_to(outer.get_top()), run_time=1.8)
        self.wait(0.8)
        self.play(Restore(self.camera.frame), run_time=1.5)

        # 4:30–4:50: Bảng so sánh hai cột Estimate vs Exact
        col_est = VGroup(
            Text("Linear Estimate", font_size=21, color=C_TAN, weight=BOLD),
            MathTex(r"\mathrm{d}A = 376.80\text{ cm}^2",
                    font_size=23, color=C_TAN),
            MathTex(r"\mathrm{d}T = 18{,}840\text{ VND}",
                    font_size=23, color=C_TAN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)

        col_act = VGroup(
            Text("Exact Value", font_size=21, color=C_CURVE, weight=BOLD),
            MathTex(r"\Delta A = 373.66\text{ cm}^2",
                    font_size=23, color=C_CURVE),
            MathTex(r"\Delta T = 18{,}683\text{ VND}",
                    font_size=23, color=C_CURVE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)

        table_grp = VGroup(col_est, col_act).arrange(RIGHT, buff=0.55).next_to(
            info_top, DOWN, aligned_edge=LEFT, buff=0.45)
        diff_res = VGroup(
            MathTex(
                r"\text{Difference: } 157\text{ VND } (0.84\% < 5\%)", font_size=24, color=C_OK),
            MathTex(
                r"\text{Red sliver: } \pi(\Delta r)^2 = 3.14\text{ cm}^2", font_size=22, color=C_ERR)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(table_grp, DOWN, aligned_edge=LEFT, buff=0.35)

        self.play(FadeIn(table_grp, shift=UP * 0.2))
        self.play(Write(diff_res))
        self.wait(2.0)
        self.play(FadeOut(outer, rad_line, brace_r, lbl_r,
                  ring, da_eq, info_top, table_grp, diff_res))

        # 4:50–5:20: Đồ thị Relative discrepancy vs Δr (0–8 cm), ngưỡng 5% tại Δr = 5.71 cm
        axes = Axes(
            x_range=[0, 8, 1], y_range=[0, 7.5, 1],
            x_length=8.2, y_length=4.6,
            axis_config={"color": C_SUB, "include_numbers": True}
        ).shift(DOWN * 0.2)
        x_lbl = MathTex(r"\Delta r\text{ (cm)}", font_size=24).next_to(
            axes.x_axis, DOWN, buff=0.35)
        y_lbl = Text("Relative Discrepancy (%)", font_size=20).rotate(
            PI / 2).next_to(axes.y_axis, LEFT, buff=0.35)

        def disc_fn(dr): return 100.0 * dr / (120.0 - dr)
        dr_tr = ValueTracker(0.01)

        dyn_curve = always_redraw(lambda: axes.plot(
            disc_fn, x_range=[0.01, dr_tr.get_value()], color=C_CURVE, stroke_width=3.5
        ))
        dyn_dot = always_redraw(lambda: Dot(
            axes.c2p(dr_tr.get_value(), disc_fn(dr_tr.get_value())), color=C_CURVE
        ))

        limit_line = DashedLine(axes.c2p(0, 5), axes.c2p(
            8, 5), color=C_ERR, stroke_width=2.5)
        limit_txt = Text("5% Acceptance Limit", font_size=19,
                         color=C_ERR).next_to(axes.c2p(1.5, 5), UP, buff=0.12)

        invalid_zone = Polygon(
            axes.c2p(5.71, 0), axes.c2p(8, 0), axes.c2p(
                8, 7.5), axes.c2p(5.71, 7.5),
            color=C_ERR, fill_opacity=0.14, stroke_width=0
        )
        dot_lim = Dot(axes.c2p(5.71, 5.0), color=C_ERR)
        lbl_lim = MathTex(r"\Delta r \approx 5.71\text{ cm}", font_size=22, color=C_ERR).next_to(
            dot_lim, DR, buff=0.12)

        dot_1 = Dot(axes.c2p(1.0, disc_fn(1.0)), color=C_OK)
        lbl_1 = MathTex(r"\Delta r = 1\text{ cm } (0.84\%)", font_size=21, color=C_OK).next_to(
            dot_1, UL, buff=0.12)

        self.play(Create(axes), Write(x_lbl), Write(y_lbl))
        self.add(dyn_curve, dyn_dot)
        self.play(dr_tr.animate.set_value(8.0), run_time=3.2)
        self.play(Create(limit_line), Write(limit_txt),
                  FadeIn(invalid_zone), FadeIn(dot_lim, lbl_lim))
        self.play(FadeIn(dot_1, lbl_1))
        self.wait(2.2)


# ==============================================================================
# 7. SCENE 7: CASE 2 — TREE HEIGHT (5:20 – 7:00)
# ==============================================================================
class S07_TreeHeight(Scene):
    def construct(self):
        # 5:20–6:15: Cảnh hiện trường đo cây tại d = 20 m, θ0 = 40°
        ground = Line([-6.2, -2.0, 0], [-0.5, -2.0, 0],
                      color=C_SUB, stroke_width=3)
        trunk = Rectangle(width=0.35, height=2.6, color="#8B5A2B",
                          fill_opacity=0.8).move_to([-1.4, -0.7, 0])
        crown = Circle(radius=0.95, color=C_OK,
                       fill_opacity=0.45).move_to([-1.4, 0.8, 0])
        tree_top = [-1.4, 1.75, 0]

        obs_body = Line([-5.2, -2.0, 0], [-5.2, -1.25, 0],
                        color=WHITE, stroke_width=4)
        obs_head = Dot([-5.2, -1.15, 0], color=WHITE, radius=0.12)
        eye_pt = [-5.2, -1.15, 0]

        horiz_sight = DashedLine(eye_pt, [-1.4, -1.15, 0], color=C_SUB)
        sight_line = Line(eye_pt, tree_top, color=C_TAN, stroke_width=2.5)
        ang = Angle(Line(eye_pt, [-1.4, -1.15, 0]),
                    sight_line, radius=0.95, color=C_TAN)
        ang_lbl = MathTex(r"\theta_0 = 40^\circ", font_size=22,
                          color=C_TAN).next_to(ang, RIGHT, buff=0.12)
        d_lbl = MathTex(r"d = 20\text{ m}", font_size=22).next_to(
            ground, DOWN, buff=0.15)

        # Nêm góc ±1° + thanh khoảng chiều cao [17.79; 18.98] m
        wedge_up = DashedLine(eye_pt, [-1.4, 2.05, 0], color=C_ERR)
        wedge_dn = DashedLine(eye_pt, [-1.4, 1.45, 0], color=C_ERR)
        range_bar = Line([-0.9, 1.45, 0], [-0.9, 2.05, 0],
                         color=C_TAN, stroke_width=6)

        right_calc = VGroup(
            Text("Case Study 2: Tree Height",
                 font_size=27, color=C_OK, weight=BOLD),
            MathTex(
                r"H(\theta) = h_e + d\tan\theta = 18.382\text{ m}", font_size=24),
            MathTex(
                r"\Delta\theta = \pm 1^\circ \implies \mathrm{d}H = 0.595\text{ m}", font_size=24, color=C_TAN),
            MathTex(
                r"H \in [17.79;\ 18.98]\text{ m}", font_size=24, color=C_TAN),
            MathTex(
                r"\Delta H = 0.604\text{ m} \implies \text{Discrepancy } 1.47\% < 5\%", font_size=23, color=C_OK),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.45)

        self.play(Create(ground), Create(trunk), Create(crown),
                  Create(obs_body), FadeIn(obs_head), Write(d_lbl))
        self.play(Create(horiz_sight), Create(sight_line), Create(
            ang), Write(ang_lbl), FadeIn(right_calc[:2]))
        self.play(Create(wedge_up), Create(wedge_dn),
                  Create(range_bar), FadeIn(right_calc[2:]))
        self.wait(2.2)
        self.play(FadeOut(
            ground, trunk, crown, obs_body, obs_head, horiz_sight, sight_line,
            ang, ang_lbl, d_lbl, wedge_up, wedge_dn, range_bar, right_calc
        ))

        # 6:15–7:00: Chia màn hình: Trái người đi bộ d: 50 -> 4 m | Phải đồ thị δH & Linearization discrepancy
        H0, he, dth = 18.382, 1.60, np.radians(1.0)
        d_tr = ValueTracker(50.0)

        # Bên trái: mô hình thu nhỏ người đi bộ
        g_left = Line([-6.3, -1.8, 0], [-1.3, -1.8, 0],
                      color=C_SUB, stroke_width=2.5)
        t_left = Rectangle(width=0.25, height=2.2, color="#8B5A2B",
                           fill_opacity=0.8).move_to([-1.7, -0.7, 0])
        c_left = Circle(radius=0.7, color=C_OK,
                        fill_opacity=0.45).move_to([-1.7, 0.6, 0])
        top_left = [-1.7, 1.3, 0]

        def walker_group():
            d_val = d_tr.get_value()
            # Map d in [4, 50] -> x in [-2.1, -6.0]
            x_obs = -1.7 - (d_val / 50.0) * 4.3
            body = Line([x_obs, -1.8, 0], [x_obs, -1.15, 0],
                        color=WHITE, stroke_width=4)
            head = Dot([x_obs, -1.05, 0], color=WHITE, radius=0.1)
            ray = Line([x_obs, -1.05, 0], top_left,
                       color=C_TAN, stroke_width=2)
            txt_d = MathTex(f"d = {d_val:.1f}\\text{{ m}}",
                            font_size=22, color=WHITE).move_to([-3.8, -2.35, 0])
            return VGroup(body, head, ray, txt_d)

        walker_dyn = always_redraw(walker_group)

        # Bên phải: Axes (x: d từ 4 đến 50 m, y: Error %)
        axes = Axes(
            x_range=[4, 50, 10], y_range=[0, 8, 2],
            x_length=6.4, y_length=4.5,
            axis_config={"color": C_SUB, "include_numbers": True}
        ).to_edge(RIGHT, buff=0.45).shift(DOWN * 0.1)
        ax_xlbl = MathTex(r"d\text{ (m)}", font_size=22).next_to(
            axes.x_axis, DOWN, buff=0.3)
        ax_ylbl = Text("Error (%)", font_size=18).rotate(
            PI / 2).next_to(axes.y_axis, LEFT, buff=0.25)

        def meas_err(d):
            th = np.arctan((H0 - he) / d)
            dh = (d / (np.cos(th)**2)) * dth
            return 100.0 * dh / H0

        def lin_disc(d):
            th = np.arctan((H0 - he) / d)
            dh = (d / (np.cos(th)**2)) * dth
            exact = d * (np.tan(th + dth) - np.tan(th))
            return 100.0 * abs(exact - dh) / abs(exact)

        # Vẽ trước từ d=50 xuống d_tr
        plot_blue = always_redraw(lambda: axes.plot(
            meas_err, x_range=[d_tr.get_value(), 50.0], color=C_CURVE, stroke_width=3
        ))
        plot_orange = always_redraw(lambda: axes.plot(
            lin_disc, x_range=[d_tr.get_value(), 50.0], color=ORANGE, stroke_width=3
        ))

        lim_5 = DashedLine(axes.c2p(4, 5), axes.c2p(
            50, 5), color=C_ERR, stroke_width=2)
        inv_rect = Polygon(
            axes.c2p(4, 0), axes.c2p(5.87, 0), axes.c2p(
                5.87, 8), axes.c2p(4, 8),
            color=C_ERR, fill_opacity=0.18, stroke_width=0
        )
        inv_lbl = Text("Invalid\n(<5.87m)", font_size=15,
                       color=C_ERR).move_to(axes.c2p(8.2, 6.8))

        opt_rect = Polygon(
            axes.c2p(15, 0), axes.c2p(20, 0), axes.c2p(20, 8), axes.c2p(15, 8),
            color=C_OK, fill_opacity=0.15, stroke_width=0
        )
        min_dot = Dot(axes.c2p(16.78, meas_err(16.78)), color=C_OK)
        min_lbl = Text("min δH ≈ 3.19% at 16.8 m\nStand at 15–20 m",
                       font_size=16, color=C_OK).next_to(min_dot, UP, buff=0.45)

        self.play(Create(g_left), Create(t_left), Create(c_left),
                  Create(axes), Write(ax_xlbl), Write(ax_ylbl))
        self.add(walker_dyn, plot_blue, plot_orange)
        self.play(d_tr.animate.set_value(4.0), run_time=4.5)
        self.play(Create(lim_5), FadeIn(inv_rect), Write(inv_lbl))
        self.play(FadeIn(opt_rect), FadeIn(min_dot), Write(min_lbl))
        self.wait(2.5)


# ==============================================================================
# 8. SCENE 8: CONCLUSION (7:00 – 7:40)
# ==============================================================================
class S08_Conclusion(Scene):
    def construct(self):
        title = Text("Conclusion", font_size=36, color=WHITE,
                     weight=BOLD).to_edge(UP, buff=0.6)

        f1 = MathTex(r"|\Delta y| \approx |f'(a)|\,\Delta x",
                     font_size=34, color=C_TAN)
        box1 = SurroundingRectangle(
            f1, color=C_TAN, buff=0.25, corner_radius=0.12)
        g1 = VGroup(box1, f1)

        f2 = MathTex(
            r"\delta y \approx |\mathrm{d}(\ln|f(a)|)|", font_size=34, color=C_OK)
        box2 = SurroundingRectangle(
            f2, color=C_OK, buff=0.25, corner_radius=0.12)
        g2 = VGroup(box2, f2)

        pillars = VGroup(g1, g2).arrange(RIGHT, buff=0.8).shift(UP * 1.1)

        bullets = VGroup(
            Text("• Absolute values guarantee worst-case error bounds.",
                 font_size=21, color=WHITE),
            Text("• Linearization stays reliable within the 5% discrepancy limit.",
                 font_size=21, color=WHITE),
            Text("• Further work: multivariable total differential & 2nd-order Taylor.",
                 font_size=21, color=WHITE),
            Text("Note: The report also includes Case 3 (measuring a cliff by dropping a rock).",
                 font_size=18, color=C_SUB),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(pillars, DOWN, buff=0.65)

        self.play(Write(title), FadeIn(pillars, shift=UP * 0.2))
        for b in bullets:
            self.play(FadeIn(b, shift=UP * 0.15), run_time=0.65)
        self.wait(2.5)
        self.play(FadeOut(title, pillars, bullets))

        thanks = Text("Thank you for watching!", font_size=40,
                      color=C_CURVE, weight=BOLD)
        team = Text(
            "Trần Nhật Duy · Phạm Lâm Nhật Khoa · Trần Việt Quốc Toàn · Nguyễn Minh Trang",
            font_size=20, color=C_SUB
        ).next_to(thanks, DOWN, buff=0.45)

        self.play(Write(thanks), FadeIn(team, shift=UP * 0.2))
        self.wait(3.0)
