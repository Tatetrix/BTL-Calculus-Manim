from manim import *
import numpy as np


class Scene05(Scene):
    def construct(self):
        # Bảng màu tối giản đồng bộ toàn bộ dự án
        self.camera.background_color = "#0F172A"
        SLATE = "#64748B"

        # Tự động ghép file tiếng khi render nháp (thêm dấu # khi render final không tiếng)
        self.add_sound("Recordings/Scene5.wav")

        # Bộ đếm thời gian khóa cứng từng mốc giây (audio 69.58s + 1.6s giữ hình cuối = 71.20s)
        t = 0.0

        def play(*anims, run_time=1.0, **kwargs):
            nonlocal t
            self.play(*anims, run_time=run_time, **kwargs)
            t += run_time

        def wait_until(target_t):
            nonlocal t
            dt = target_t - t
            if dt > 0.01:
                self.wait(dt)
                t += dt

        # Header cố định tối giản góc trái trên
        header_badge = VGroup(
            Text("Group 4 (CC01)", font_size=16, color=TEAL_C, weight=BOLD),
            Text("Topic 9: Error Propagation", font_size=18, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.06)
        header_badge.to_corner(UL, buff=0.35)

        header_line = Line(
            LEFT * 6.8, RIGHT * 6.8, color=SLATE, stroke_width=1, stroke_opacity=0.35
        ).next_to(header_badge, DOWN, buff=0.15, aligned_edge=LEFT)

        self.add(header_badge, header_line)

        sec_title = Text(
            "Accuracy, Breakdown & The 5% Rule",
            font_size=25,
            color=YELLOW_C,
            weight=BOLD,
        ).to_edge(UP, buff=0.38).shift(RIGHT * 1.2)

        # =====================================================================
        # BEAT 1A (0.00s – 4.10s): CÂU HỎI MỞ ĐẦU — TẠI SAO THAY Δy BẰNG dy LẠI TỐT?
        # "So why does replacing delta y with dy work so well?"
        # =====================================================================
        open_dy_true = MathTex(r"\Delta y", font_size=76,
                               color=TEAL_C).move_to([-2.1, 0.35, 0])
        open_dy_diff = MathTex(r"dy", font_size=76,
                               color=YELLOW_C).move_to([2.1, 0.35, 0])
        open_arrow = CurvedArrow(
            [-1.1, 0.55, 0], [1.1, 0.55, 0],
            angle=-0.45, color=WHITE, stroke_width=3.5, tip_length=0.22
        )
        open_replace = Text("replace with", font_size=20, color=GREY_A).next_to(
            open_arrow, UP, buff=0.14
        )
        open_q = Text(
            "Why does this linear shortcut work so well?",
            font_size=28, color=WHITE, weight=BOLD
        ).move_to([0, -1.15, 0])
        open_line = Line(LEFT * 3.1, RIGHT * 3.1, color=TEAL_C, stroke_width=2.2, stroke_opacity=0.75).next_to(
            open_q, DOWN, buff=0.18
        )

        play(
            FadeIn(sec_title, shift=DOWN * 0.15),
            FadeIn(open_dy_true, scale=0.88),
            run_time=0.9,
        )
        play(
            Create(open_arrow),
            FadeIn(open_replace, shift=UP * 0.08),
            FadeIn(open_dy_diff, shift=RIGHT * 0.25),
            FadeIn(open_q, shift=UP * 0.15),
            Create(open_line),
            run_time=1.8,
            rate_func=smooth,
        )
        play(
            Indicate(open_dy_diff, color=YELLOW_A, scale_factor=1.14),
            run_time=0.8,
        )
        wait_until(3.65)
        play(
            FadeOut(VGroup(open_dy_true, open_dy_diff,
                    open_arrow, open_replace, open_q, open_line)),
            run_time=0.45,
        )

        # =====================================================================
        # BEAT 1B (4.10s – 17.85s): CÁT TUYẾN XOAY THÀNH TIẾP TUYẾN & KHE ĐỎ TẮT NHANH
        # "Watch what happens as delta x shrinks towards zero:
        #  the secant line rotates smoothly into the tangent line,
        #  and that red gap between them vanishes even faster than delta x itself."
        # =====================================================================
        wait_until(4.10)

        ax1 = Axes(
            x_range=[0, 3.8, 1],
            y_range=[0, 4.5, 1],
            x_length=5.8,
            y_length=4.35,
            axis_config={
                "color": GREY_B,
                "stroke_width": 1.8,
                "include_tip": True,
                "tip_width": 0.13,
                "tip_height": 0.13,
            },
        ).move_to([-2.65, -0.45, 0])

        a1 = 1.0

        def f1(x):
            return 0.26 * (x**2) + 0.22 * x + 0.55

        fa1 = f1(a1)
        fp1 = 0.52 * a1 + 0.22

        def L1(x):
            return fa1 + fp1 * (x - a1)

        curve1 = ax1.plot(f1, x_range=[0.15, 3.45],
                          color=BLUE_C, stroke_width=3.6)
        tan1 = DashedLine(
            ax1.c2p(0.3, L1(0.3)),
            ax1.c2p(3.55, L1(3.55)),
            color=YELLOW_C,
            stroke_width=2.8,
            dash_length=0.14,
        )
        dot_a1 = Dot(ax1.c2p(a1, fa1), color=WHITE, radius=0.075)
        lbl_a1 = MathTex(r"a", font_size=22, color=GREY_A).next_to(
            ax1.c2p(a1, 0), DOWN, buff=0.14
        )
        tan_lbl = Text("Tangent", font_size=17, color=YELLOW_C).next_to(
            ax1.c2p(3.25, L1(3.25)), DOWN, buff=0.16
        )

        dx_t = ValueTracker(2.15)

        def get_secant():
            dx = dx_t.get_value()
            m_sec = (f1(a1 + dx) - fa1) / dx
            x_l = 0.35
            x_r = min(3.45, a1 + dx + 0.25)
            return Line(
                ax1.c2p(x_l, fa1 + m_sec * (x_l - a1)),
                ax1.c2p(x_r, fa1 + m_sec * (x_r - a1)),
                color=PURPLE_B,
                stroke_width=3.0,
            )

        def get_moving_parts():
            dx = dx_t.get_value()
            b = a1 + dx
            p_a = ax1.c2p(a1, fa1)
            p_base = ax1.c2p(b, fa1)
            p_tan = ax1.c2p(b, L1(b))
            p_cur = ax1.c2p(b, f1(b))

            dx_seg = Line(p_a, p_base, color=BLUE_B, stroke_width=4.0)
            dy_seg = Line(p_base, p_tan, color=YELLOW_C,
                          stroke_width=3.2, stroke_opacity=0.85)
            gap_seg = Line(p_tan, p_cur, color=RED_C, stroke_width=7.0)
            dot_b = Dot(p_cur, color=PURPLE_B, radius=0.075)
            grp = VGroup(dx_seg, dy_seg, gap_seg, dot_b)
            # Ẩn nhãn Secant khi điểm chạy tiến quá sát a để không bị đè chữ
            if dx > 0.38:
                sec_tag = Text("Secant", font_size=17, color=PURPLE_B).next_to(
                    dot_b, UL, buff=0.14
                )
                grp.add(sec_tag)
            return grp

        dyn_secant = always_redraw(get_secant)
        dyn_parts = always_redraw(get_moving_parts)

        play(
            Create(ax1),
            Create(curve1),
            Create(tan1),
            FadeIn(tan_lbl),
            FadeIn(dot_a1),
            FadeIn(lbl_a1),
            Create(dyn_secant),
            FadeIn(dyn_parts),
            run_time=1.7,
        )

        # Thanh đo tối giản bên phải (tách xa đồ thị, không bao giờ chồng chữ)
        bar_max_w = 4.0
        bar_x_left = 2.05

        hdr_shrink = MathTex(r"\Delta x \longrightarrow 0", font_size=34, color=WHITE).move_to(
            [bar_x_left + bar_max_w / 2.0, 1.35, 0]
        )

        lbl_bar_dx = MathTex(r"\text{Step } \Delta x", font_size=22, color=BLUE_B).move_to(
            [bar_x_left, 0.35, 0], aligned_edge=LEFT
        )
        track_dx = Line(
            [bar_x_left, -0.05, 0], [bar_x_left + bar_max_w, -0.05, 0],
            color=SLATE, stroke_width=8, stroke_opacity=0.3
        )
        dyn_bar_dx = always_redraw(
            lambda: Line(
                [bar_x_left, -0.05, 0],
                [bar_x_left +
                    max(bar_max_w * (dx_t.get_value() / 2.15), 0.04), -0.05, 0],
                color=BLUE_B, stroke_width=8,
            )
        )
        dyn_num_dx = always_redraw(
            lambda: MathTex(
                rf"{dx_t.get_value():.2f}", font_size=23, color=BLUE_B
            ).move_to([bar_x_left + bar_max_w, 0.35, 0], aligned_edge=RIGHT)
        )

        lbl_bar_gap = MathTex(
            r"\text{Red Gap } |\Delta y - dy|", font_size=22, color=RED_B
        ).move_to([bar_x_left, -1.05, 0], aligned_edge=LEFT)
        track_gap = Line(
            [bar_x_left, -1.45, 0], [bar_x_left + bar_max_w, -1.45, 0],
            color=SLATE, stroke_width=8, stroke_opacity=0.3
        )
        dyn_bar_gap = always_redraw(
            lambda: Line(
                [bar_x_left, -1.45, 0],
                [
                    bar_x_left
                    + max(bar_max_w * ((0.26 * (dx_t.get_value() ** 2)) /
                          (0.26 * (2.15**2))), 0.02),
                    -1.45,
                    0,
                ],
                color=RED_C, stroke_width=8,
            )
        )
        dyn_num_gap = always_redraw(
            lambda: MathTex(
                rf"{0.26 * (dx_t.get_value() ** 2):.2f}", font_size=23, color=RED_B
            ).move_to([bar_x_left + bar_max_w, -1.05, 0], aligned_edge=RIGHT)
        )

        play(
            Write(hdr_shrink),
            FadeIn(VGroup(lbl_bar_dx, track_dx, dyn_bar_dx, dyn_num_dx)),
            FadeIn(VGroup(lbl_bar_gap, track_gap, dyn_bar_gap, dyn_num_gap)),
            run_time=1.3,
        )

        # 7.70s: "the secant line rotates smoothly into the tangent line,"
        wait_until(7.70)
        play(dx_t.animate.set_value(0.72), run_time=3.1, rate_func=smooth)

        # 11.15s: "and that red gap between them vanishes even faster than delta x itself."
        wait_until(11.15)
        play(dx_t.animate.set_value(0.06), run_time=4.6, rate_func=smooth)

        gap_zero_ring = SurroundingRectangle(
            dyn_num_gap, color=GREEN_C, buff=0.1, corner_radius=0.08
        )
        play(Create(gap_zero_ring), FadeOut(gap_zero_ring), run_time=0.8)

        wait_until(17.10)
        beat1_all = VGroup(
            ax1, curve1, tan1, tan_lbl, dot_a1, lbl_a1, dyn_secant, dyn_parts,
            hdr_shrink, lbl_bar_dx, track_dx, dyn_bar_dx, dyn_num_dx,
            lbl_bar_gap, track_gap, dyn_bar_gap, dyn_num_gap,
        )
        play(FadeOut(beat1_all), run_time=0.75)

        # =====================================================================
        # BEAT 2 (18.05s – 32.30s): KÝ HIỆU SAI SỐ BẬC CAO Δy = dy + ε·Δx
        # "In symbols, delta y equals dy plus epsilon delta x, where epsilon goes
        #  to zero, meaning the leftover error is a higher-order term that we
        #  can safely ignore when delta x is small."
        # =====================================================================
        wait_until(18.05)

        sym_tag = Text(
            "IN SYMBOLS", font_size=18, color=GREY_B, weight=BOLD
        ).move_to([0, 1.55, 0])
        play(FadeIn(sym_tag, shift=DOWN * 0.1), run_time=0.7)

        # 19.05s: "delta y equals dy plus epsilon delta x,"
        wait_until(19.05)
        eq_sym = MathTex(
            r"\Delta y", r"=", r"dy", r"+", r"\varepsilon\,\Delta x",
            font_size=62, color=WHITE
        ).move_to([0, 0.35, 0])
        eq_sym[0].set_color(TEAL_C)
        eq_sym[2].set_color(YELLOW_C)
        eq_sym[4].set_color(RED_B)

        play(Write(eq_sym), run_time=2.3)

        # 22.35s: "where epsilon goes to zero,"
        wait_until(22.35)
        eps_cond = MathTex(
            r"\text{where }\; \varepsilon \longrightarrow 0 \;\text{ as }\; \Delta x \longrightarrow 0",
            font_size=28, color=GREY_A
        ).move_to([0, -2.0, 0])
        play(FadeIn(eps_cond, shift=UP * 0.12), run_time=1.6)

        # 24.15s: "meaning the leftover error is a higher-order term..."
        wait_until(24.15)
        ho_brace = Brace(eq_sym[4], direction=DOWN, buff=0.18, color=RED_C)
        ho_lbl = Text(
            "Higher-order leftover error", font_size=20, color=RED_B, weight=BOLD
        ).next_to(ho_brace, DOWN, buff=0.12)
        play(GrowFromCenter(ho_brace), FadeIn(
            ho_lbl, shift=UP * 0.1), run_time=1.7)

        # 27.30s: "...that we can safely ignore when delta x is small."
        # Gạch bỏ số hạng dư rồi thu gọn trực tiếp phương trình thành Δy ≈ dy ở giữa!
        wait_until(27.30)
        strike_eps = Line(
            eq_sym[4].get_corner(DL) + LEFT * 0.08,
            eq_sym[4].get_corner(UR) + RIGHT * 0.08,
            color=RED_C, stroke_width=3.5
        )
        play(Create(strike_eps), run_time=0.7)

        collapsed_eq = MathTex(
            r"\Delta y", r"\approx", r"dy", font_size=68, color=WHITE
        ).move_to([0, 0.25, 0])
        collapsed_eq[0].set_color(TEAL_C)
        collapsed_eq[1].set_color(GREEN_C)
        collapsed_eq[2].set_color(YELLOW_C)

        small_note = Text(
            "Safe to ignore leftover error when Δx is small",
            font_size=21, color=GREEN_C, weight=BOLD
        ).move_to([0, -1.25, 0])

        play(
            FadeOut(VGroup(eq_sym[3], eq_sym[4], ho_brace,
                    ho_lbl, strike_eps, eps_cond)),
            Transform(eq_sym[0], collapsed_eq[0]),
            Transform(eq_sym[1], collapsed_eq[1]),
            Transform(eq_sym[2], collapsed_eq[2]),
            FadeIn(small_note, shift=UP * 0.12),
            run_time=2.0,
            rate_func=smooth,
        )

        res_flash = Line(
            collapsed_eq.get_left(), collapsed_eq.get_right(),
            color=YELLOW_C, stroke_width=4.2
        ).next_to(collapsed_eq, DOWN, buff=0.22)
        play(ShowPassingFlash(res_flash, time_width=0.55), run_time=0.8)

        wait_until(31.50)
        play(
            FadeOut(VGroup(sym_tag, eq_sym[0],
                    eq_sym[1], eq_sym[2], small_note)),
            run_time=0.8,
        )

        # =====================================================================
        # BEAT 3 (33.30s – 55.10s): ĐIỂM GÃY — y = sin(x) TẠI Δx = 1 RADIAN
        # "Still, every linear model has its breaking point.
        #  Take y = sin(x) at zero, and suppose we take a huge step of 1 radian.
        #  The differential predicts a change of 1, while the true change is sin(1),
        #  about 0.84. That's nearly 19% off — way too rough."
        # =====================================================================
        wait_until(33.30)

        bp_text = Text(
            "Every linear model has its breaking point.",
            font_size=34, color=WHITE, weight=BOLD
        ).move_to([0, 0.2, 0])
        # Đường gạch đỏ gồm 2 nửa liền nhau, rồi tách & gãy gập ngay chữ "breaking point"!
        bp_half_l = Line([-3.2, -0.32, 0], [0.0, -0.32, 0],
                         color=RED_C, stroke_width=3.5)
        bp_half_r = Line([0.0, -0.32, 0], [3.2, -0.32, 0],
                         color=RED_C, stroke_width=3.5)

        play(
            FadeIn(bp_text, shift=UP * 0.12),
            Create(bp_half_l),
            Create(bp_half_r),
            run_time=1.3,
        )
        play(
            bp_half_l.animate.rotate(-0.08,
                                     about_point=[-3.2, -0.32, 0]).shift(LEFT * 0.08),
            bp_half_r.animate.rotate(
                0.08, about_point=[3.2, -0.32, 0]).shift(RIGHT * 0.08),
            run_time=0.9,
            rate_func=smooth,
        )

        # 36.35s: "Take y equals sin x"
        wait_until(36.35)

        ax3 = Axes(
            x_range=[0, 1.45, 0.5],
            y_range=[0, 1.35, 0.5],
            x_length=5.8,
            y_length=4.3,
            axis_config={
                "color": GREY_B,
                "stroke_width": 1.8,
                "include_tip": True,
                "tip_width": 0.13,
                "tip_height": 0.13,
            },
        ).move_to([-2.65, -0.45, 0])

        sin_curve = ax3.plot(
            np.sin, x_range=[0, 1.38], color=BLUE_C, stroke_width=3.8)
        # Đặt nhãn gọn dưới đường cong để không lấn sang cột số liệu bên phải
        sin_lbl = MathTex(r"y = \sin x", font_size=26, color=BLUE_B).next_to(
            ax3.c2p(1.30, np.sin(1.30)), DOWN, buff=0.22
        )

        play(
            FadeOut(VGroup(bp_text, bp_half_l, bp_half_r)),
            Create(ax3),
            Create(sin_curve),
            Write(sin_lbl),
            run_time=1.7,
        )

        # 38.30s: "at zero," -> Neo điểm gốc (0, 0) & vẽ tiếp tuyến y = x
        wait_until(38.30)
        origin_dot = Dot(ax3.c2p(0, 0), color=WHITE, radius=0.08)
        origin_lbl = MathTex(r"0", font_size=22, color=GREY_A).next_to(
            origin_dot, DL, buff=0.12)
        tan_sin = ax3.plot(lambda x: x, x_range=[
                           0, 1.22], color=YELLOW_C, stroke_width=3.0)
        tan_sin_lbl = MathTex(r"y = x", font_size=25, color=YELLOW_C).next_to(
            ax3.c2p(0.85, 0.85), UL, buff=0.18
        )

        play(
            FadeIn(origin_dot), FadeIn(origin_lbl),
            Create(tan_sin), Write(tan_sin_lbl),
            run_time=0.95,
        )

        # 39.35s: "and suppose we take a huge step of 1 radian."
        # Quét bước nhảy 0 -> 1 rad đồng thời vẽ khe tách đỏ trực tiếp giữa đường cong & tiếp tuyến!
        wait_until(39.35)
        step_t = ValueTracker(0.02)

        dyn_step_arrow = always_redraw(
            lambda: Arrow(
                ax3.c2p(0, 0),
                ax3.c2p(step_t.get_value(), 0),
                buff=0,
                color=ORANGE,
                stroke_width=5,
                max_tip_length_to_length_ratio=0.12,
            )
        )
        dyn_step_lbl = always_redraw(
            lambda: MathTex(
                rf"\Delta x = {step_t.get_value():.2f}\text{{ rad}}",
                font_size=24, color=ORANGE
            ).next_to(ax3.c2p(step_t.get_value() * 0.52, 0), DOWN, buff=0.22)
        )
        dyn_sweep_div = always_redraw(
            lambda: VGroup(
                DashedLine(
                    ax3.c2p(step_t.get_value(), 0),
                    ax3.c2p(step_t.get_value(), step_t.get_value()),
                    color=GREY_B, stroke_width=1.6, stroke_opacity=0.6
                ),
                Line(
                    ax3.c2p(step_t.get_value(), np.sin(step_t.get_value())),
                    ax3.c2p(step_t.get_value(), step_t.get_value()),
                    color=RED_C, stroke_width=6.5, stroke_opacity=0.85
                ),
                Dot(ax3.c2p(step_t.get_value(), step_t.get_value()),
                    color=YELLOW_C, radius=0.065),
                Dot(ax3.c2p(step_t.get_value(), np.sin(step_t.get_value())),
                    color=TEAL_C, radius=0.065),
            )
        )

        self.add(dyn_step_arrow, dyn_step_lbl, dyn_sweep_div)
        play(step_t.animate.set_value(1.0), run_time=2.5, rate_func=smooth)

        # Cố định trạng thái tại x = 1.0 rad
        self.remove(dyn_step_arrow, dyn_step_lbl, dyn_sweep_div)
        fixed_step_arrow = Arrow(
            ax3.c2p(0, 0), ax3.c2p(1.0, 0), buff=0,
            color=ORANGE, stroke_width=5, max_tip_length_to_length_ratio=0.12
        )
        fixed_step_lbl = MathTex(r"\Delta x = 1\text{ rad}", font_size=24, color=ORANGE).next_to(
            fixed_step_arrow, DOWN, buff=0.2
        )
        p_x1_base = ax3.c2p(1.0, 0)
        p_x1_tan = ax3.c2p(1.0, 1.0)
        p_x1_sin = ax3.c2p(1.0, np.sin(1.0))

        dot_tan1 = Dot(p_x1_tan, color=YELLOW_C, radius=0.075)
        dot_sin1 = Dot(p_x1_sin, color=TEAL_C, radius=0.075)
        crimson_gap = Line(p_x1_sin, p_x1_tan, color=RED_C, stroke_width=8.5)
        self.add(fixed_step_arrow, fixed_step_lbl,
                 dot_tan1, dot_sin1, crimson_gap)

        # 42.55s: "The differential predicts a change of 1,"
        wait_until(42.55)
        beam_dy = Line(p_x1_base + RIGHT * 0.08, p_x1_tan +
                       RIGHT * 0.08, color=YELLOW_C, stroke_width=4.2)
        guide_y1 = DashedLine(ax3.c2p(
            0, 1.0), p_x1_tan, color=YELLOW_C, stroke_width=1.4, stroke_opacity=0.55)
        y1_tick = MathTex(r"1", font_size=21, color=YELLOW_C).next_to(
            ax3.c2p(0, 1.0), LEFT, buff=0.14)

        col_x = 3.55
        readout_dy = MathTex(r"dy = 1.00", font_size=34,
                             color=YELLOW_C).move_to([col_x, 1.35, 0])
        lbl_pred = Text("Differential prediction", font_size=17, color=GREY_B).next_to(
            readout_dy, UP, buff=0.1
        )

        play(
            GrowFromEdge(beam_dy, DOWN),
            Create(guide_y1),
            FadeIn(y1_tick),
            FadeIn(lbl_pred),
            Write(readout_dy),
            run_time=2.1,
        )

        # 45.20s: "while the true change is sin of 1,"
        wait_until(45.20)
        beam_true = Line(p_x1_base + LEFT * 0.08, p_x1_sin +
                         LEFT * 0.08, color=TEAL_C, stroke_width=4.2)
        readout_true = MathTex(
            r"\Delta y = \sin(1)", font_size=34, color=TEAL_C).move_to([col_x, 0.05, 0])
        lbl_true = Text("True change", font_size=17, color=GREY_B).next_to(
            readout_true, UP, buff=0.1
        )

        play(
            GrowFromEdge(beam_true, DOWN),
            FadeIn(lbl_true),
            Write(readout_true),
            run_time=1.9,
        )

        # 47.80s: "about 0.84."
        wait_until(47.80)
        guide_sin1 = DashedLine(ax3.c2p(
            0, np.sin(1.0)), p_x1_sin, color=TEAL_C, stroke_width=1.4, stroke_opacity=0.55)
        ysin_tick = MathTex(r"0.84", font_size=20, color=TEAL_C).next_to(
            ax3.c2p(0, np.sin(1.0)), LEFT, buff=0.14)
        readout_approx = MathTex(r"\approx 0.84", font_size=34, color=TEAL_B).next_to(
            readout_true, DOWN, buff=0.12
        )

        play(
            Create(guide_sin1),
            FadeIn(ysin_tick),
            Write(readout_approx),
            run_time=1.8,
        )

        # 50.85s: "That's nearly 19% off — way too rough."
        wait_until(50.85)
        gap_brace = Brace(crimson_gap, direction=RIGHT, buff=0.14, color=RED_C)
        gap_val = MathTex(r"0.16", font_size=21, color=RED_B).next_to(
            gap_brace, RIGHT, buff=0.08)

        off_big = MathTex(r"\approx 19\%\text{ OFF}", font_size=40, color=RED_C).move_to(
            [col_x, -1.6, 0])
        off_sub = Text("Way too rough!", font_size=19, color=RED_B, weight=BOLD).next_to(
            off_big, DOWN, buff=0.12
        )

        play(
            Indicate(crimson_gap, color=RED_B, scale_factor=1.18),
            GrowFromCenter(gap_brace),
            FadeIn(gap_val),
            Write(off_big),
            FadeIn(off_sub, shift=UP * 0.1),
            run_time=1.7,
        )
        play(Indicate(off_big, color=YELLOW_C, scale_factor=1.12), run_time=0.8)

        wait_until(54.25)
        beat3_all = VGroup(
            ax3, sin_curve, sin_lbl, origin_dot, origin_lbl, tan_sin, tan_sin_lbl,
            fixed_step_arrow, fixed_step_lbl, beam_dy, dot_tan1, guide_y1, y1_tick,
            lbl_pred, readout_dy, beam_true, dot_sin1, lbl_true, readout_true,
            guide_sin1, ysin_tick, readout_approx, crimson_gap, gap_brace, gap_val,
            off_big, off_sub,
        )
        play(FadeOut(beat3_all), run_time=0.85)

        # =====================================================================
        # BEAT 4 (55.40s – 71.20s): QUY TẮC KIỂM DUYỆT NGHIÊM NGẶT 5% (THÊM ĐẤT DIỄN)
        # "That's why in all of our case studies, we enforce a strict quality check:
        #  we only accept the linear approximation when its relative discrepancy —
        #  the gap divided by the true change — stays below 5%."
        # =====================================================================
        wait_until(55.40)

        qc_title = Text(
            "STRICT QUALITY CHECK  ·  THE 5% RULE",
            font_size=24, color=YELLOW_C, weight=BOLD
        ).move_to([0, 1.8, 0])
        qc_rule = Line(LEFT * 3.5, RIGHT * 3.5, color=YELLOW_C, stroke_width=2.0, stroke_opacity=0.7).next_to(
            qc_title, DOWN, buff=0.16
        )

        # Đưa thanh đo dung sai lên sớm (đang neo tại mốc 18.8% REJECT từ ví dụ sin 1!)
        g_w = 8.6
        g_y = -1.85
        g_left = -g_w / 2.0
        green_w = g_w * (5.0 / 20.0)
        red_w = g_w * (15.0 / 20.0)
        x_5pct = g_left + green_w

        green_zone = RoundedRectangle(
            width=green_w, height=0.24, corner_radius=0.06,
            fill_color=GREEN_C, fill_opacity=0.88, stroke_width=0
        ).move_to([g_left + green_w / 2.0, g_y, 0])

        red_zone = RoundedRectangle(
            width=red_w, height=0.24, corner_radius=0.06,
            fill_color=RED_C, fill_opacity=0.32, stroke_width=0
        ).move_to([x_5pct + red_w / 2.0, g_y, 0])

        thresh_line = Line(
            [x_5pct, g_y - 0.36, 0], [x_5pct, g_y + 0.4, 0],
            color=YELLOW_C, stroke_width=3.2
        )
        thresh_lbl = MathTex(r"5\%", font_size=24, color=YELLOW_C).next_to(
            thresh_line, UP, buff=0.08)
        acc_lbl = Text("ACCEPT", font_size=17, color=GREEN_C, weight=BOLD).move_to(
            [(g_left + x_5pct) / 2.0, g_y - 0.45, 0]
        )
        rej_lbl = Text("REJECT", font_size=17, color=RED_B, weight=BOLD).move_to(
            [(x_5pct + g_left + g_w) / 2.0, g_y - 0.45, 0]
        )

        ptr_val = ValueTracker(18.8)
        dyn_ptr = always_redraw(
            lambda: VGroup(
                Dot(
                    [g_left + g_w * (ptr_val.get_value() / 20.0), g_y, 0],
                    color=GREEN_C if ptr_val.get_value() < 5.0 else RED_C,
                    radius=0.115,
                ),
                MathTex(
                    rf"{ptr_val.get_value():.1f}\%",
                    font_size=23,
                    color=GREEN_C if ptr_val.get_value() < 5.0 else RED_B,
                ).move_to([g_left + g_w * (ptr_val.get_value() / 20.0), g_y + 0.44, 0]),
            )
        )

        play(
            FadeIn(qc_title, shift=DOWN * 0.12),
            Create(qc_rule),
            FadeIn(VGroup(green_zone, red_zone, thresh_line, thresh_lbl,
                   acc_lbl, rej_lbl, dyn_ptr), shift=UP * 0.15),
            run_time=2.6,
        )

        # 59.55s: "we only accept the linear approximation when its relative discrepancy,"
        wait_until(59.55)

        lhs_rd = Text("Relative Discrepancy  =", font_size=26, color=GREY_A)
        num_gap = MathTex(r"|\Delta y - dy|", font_size=42, color=RED_B)
        frac_bar = Line(LEFT * 1.15, RIGHT * 1.15,
                        color=WHITE, stroke_width=2.8)
        den_true = MathTex(r"|\Delta y|", font_size=42, color=TEAL_C)
        frac_grp = VGroup(num_gap, frac_bar, den_true).arrange(DOWN, buff=0.12)
        lt_5 = MathTex(r"<\; 5\%", font_size=50, color=GREEN_C)

        criterion_row = VGroup(lhs_rd, frac_grp, lt_5).arrange(
            RIGHT, buff=0.35).move_to([0, 0.25, 0])

        play(
            FadeIn(lhs_rd, shift=RIGHT * 0.15),
            Write(num_gap),
            Create(frac_bar),
            Write(den_true),
            run_time=3.6,
        )

        # 65.05s: "the gap divided by the true change,"
        wait_until(65.05)
        play(Indicate(num_gap, color=RED_C, scale_factor=1.18), run_time=0.8)
        play(Indicate(den_true, color=TEAL_B, scale_factor=1.18), run_time=0.8)

        # 67.00s: "stays below 5%." -> Trượt mượt con trỏ từ 18.8% (REJECT) vào vùng xanh 2.4% (ACCEPT)!
        wait_until(67.00)
        play(
            Write(lt_5),
            ptr_val.animate.set_value(2.4),
            run_time=2.4,
            rate_func=smooth,
        )

        lt_flash = Line(lt_5.get_left(), lt_5.get_right(), color=YELLOW_C, stroke_width=4.5).next_to(
            lt_5, DOWN, buff=0.14
        )
        play(
            ShowPassingFlash(lt_flash, time_width=0.55),
            Indicate(acc_lbl, color=YELLOW_C, scale_factor=1.22),
            run_time=1.0,
        )

        # Giữ hình thêm ~1.6s cuối để người xem kịp nhìn rõ toàn bộ quy tắc 5%
        wait_until(71.20)
