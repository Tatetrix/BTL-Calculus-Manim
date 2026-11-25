from manim import *
import numpy as np


class Scene03(Scene):
    def construct(self):
        # Bảng màu đồng bộ toàn bộ dự án
        self.camera.background_color = "#0F172A"
        SLATE = "#64748B"
        CARD_BG = "#1E293B"

        # Tự động ghép file tiếng khi render nháp (thêm dấu # khi render final không tiếng)
        self.add_sound("Recordings/Scene3.wav")

        # Bộ đếm thời gian khóa cứng mốc giây khớp 100% với Scene3.wav (81.92s)
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

        # Header cố định góc trái trên
        header_badge = VGroup(
            Text("Group 4 (CC01)", font_size=16, color=TEAL_C, weight=BOLD),
            Text("Topic 9: Error Propagation", font_size=18, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.06)
        header_badge.to_corner(UL, buff=0.35)

        header_line = Line(
            LEFT * 6.8, RIGHT * 6.8, color=SLATE, stroke_width=1, stroke_opacity=0.4
        ).next_to(header_badge, DOWN, buff=0.15, aligned_edge=LEFT)

        self.add(header_badge, header_line)

        sec_title = Text(
            "Theorem 1: The Absolute-Error Law",
            font_size=26,
            color=YELLOW_C,
            weight=BOLD,
        ).to_edge(UP, buff=0.38).shift(RIGHT * 1.2)

        # =====================================================================
        # PHẦN 1: CÂU HỎI MỞ ĐẦU — TẠI SAO PHẢI CÓ DẤU | · | ? (0.00s – 10.45s)
        # "Before we write down the formula, let's ask a natural question:
        #  why do error formulas always have absolute value bars around them?"
        # =====================================================================
        bar_l = MathTex(r"\Big|", font_size=94, color=YELLOW_C)
        bar_mid = VGroup(
            Text("Error Formulas", font_size=34, color=WHITE, weight=BOLD),
            MathTex(r"\Delta y,\; f'(a),\; \Delta x",
                    font_size=28, color=TEAL_C),
        ).arrange(DOWN, buff=0.18)
        bar_r = MathTex(r"\Big|", font_size=94, color=YELLOW_C)

        hook_core = VGroup(bar_l, bar_mid, bar_r).arrange(
            RIGHT, buff=0.35).shift(UP * 0.25)
        hook_q = Text(
            "Why do error formulas always have absolute value bars around them?",
            font_size=23,
            color=GREY_A,
        ).next_to(hook_core, DOWN, buff=0.55)

        play(
            FadeIn(sec_title, shift=DOWN * 0.15),
            FadeIn(hook_core, scale=0.92),
            FadeIn(hook_q, shift=UP * 0.15),
            run_time=1.2,
        )
        # Chờ đến đúng cụm "...always have absolute value bars around them?" (~6.0s)
        wait_until(5.8)
        play(
            Indicate(bar_l, color=RED_B, scale_factor=1.25),
            Indicate(bar_r, color=RED_B, scale_factor=1.25),
            run_time=1.8,
        )
        wait_until(9.60)
        play(FadeOut(VGroup(hook_core, hook_q)), run_time=0.75)

        # =====================================================================
        # PHẦN 2: CHỨNG MINH TRỰC QUAN CANCEL OUT VS. PILE UP (10.45s – 41.80s)
        # =====================================================================
        wait_until(10.50)

        # --- 2A. Thước số đo L = x1 - x2 (10.50s – 14.70s) ---
        # "Imagine measuring a length difference L = x1 - x2."
        nl = NumberLine(
            x_range=[0, 10, 1],
            length=10.0,
            color=GREY_B,
            include_numbers=True,
            font_size=20,
            numbers_to_include=[0, 2, 3, 4, 6, 7, 8, 10],
            decimal_number_config={"num_decimal_places": 0, "color": GREY_A},
        ).move_to([0, 1.2, 0])

        # ValueTracker điều khiển động 2 điểm đo x2 (trái) và x1 (phải)
        x2_t = ValueTracker(3.0)
        x1_t = ValueTracker(7.0)

        bar_y = 1.68

        # Thanh vàng L luôn nằm chính giữa x2 và x1
        dyn_L_bar = always_redraw(
            lambda: Rectangle(
                width=max((x1_t.get_value() - x2_t.get_value()), 0.1),
                height=0.38,
                fill_color=YELLOW_C,
                fill_opacity=0.88,
                stroke_color=YELLOW_A,
                stroke_width=1.8,
            ).move_to([
                (nl.n2p(x2_t.get_value())[0] +
                 nl.n2p(x1_t.get_value())[0]) / 2.0,
                bar_y,
                0,
            ])
        )

        # Hai cọc mốc đo x2 (xanh dương) và x1 (xanh ngọc)
        dyn_pin_x2 = always_redraw(
            lambda: VGroup(
                Line(
                    nl.n2p(x2_t.get_value()) + DOWN * 0.08,
                    [nl.n2p(x2_t.get_value())[0], bar_y + 0.36, 0],
                    color=BLUE_B,
                    stroke_width=3.5,
                ),
                Dot(nl.n2p(x2_t.get_value()), color=BLUE_B, radius=0.08),
                MathTex(
                    rf"x_2 = {x2_t.get_value():.1f}",
                    font_size=22,
                    color=BLUE_B,
                ).move_to([nl.n2p(x2_t.get_value())[0], bar_y + 0.62, 0]),
            )
        )

        dyn_pin_x1 = always_redraw(
            lambda: VGroup(
                Line(
                    nl.n2p(x1_t.get_value()) + DOWN * 0.08,
                    [nl.n2p(x1_t.get_value())[0], bar_y + 0.36, 0],
                    color=TEAL_C,
                    stroke_width=3.5,
                ),
                Dot(nl.n2p(x1_t.get_value()), color=TEAL_C, radius=0.08),
                MathTex(
                    rf"x_1 = {x1_t.get_value():.1f}",
                    font_size=22,
                    color=TEAL_C,
                ).move_to([nl.n2p(x1_t.get_value())[0], bar_y + 0.62, 0]),
            )
        )

        # Nhãn đọc độ dài L trực tiếp ở giữa dưới thước
        dyn_L_readout = always_redraw(
            lambda: MathTex(
                rf"L = x_1 - x_2 = {x1_t.get_value():.1f} - {x2_t.get_value():.1f} = {x1_t.get_value() - x2_t.get_value():.1f}",
                font_size=27,
                color=RED_B if abs(
                    (x1_t.get_value() - x2_t.get_value()) - 4.0) > 0.05 else YELLOW_C,
            ).move_to([0, 0.32, 0])
        )

        # Hai vạch mờ đánh dấu vị trí chuẩn ban đầu (3.0 và 7.0)
        true_mark_2 = DashedLine(
            nl.n2p(3.0), [nl.n2p(3.0)[0], bar_y + 0.25, 0],
            color=GREY_C, stroke_width=1.5, stroke_opacity=0.55
        )
        true_mark_1 = DashedLine(
            nl.n2p(7.0), [nl.n2p(7.0)[0], bar_y + 0.25, 0],
            color=GREY_C, stroke_width=1.5, stroke_opacity=0.55
        )

        play(
            Create(nl),
            FadeIn(true_mark_2),
            FadeIn(true_mark_1),
            FadeIn(dyn_pin_x2),
            FadeIn(dyn_pin_x1),
            GrowFromCenter(dyn_L_bar),
            Write(dyn_L_readout),
            run_time=1.8,
        )
        wait_until(14.70)

        # --- 2B. MINH HỌA "CANCEL OUT" (14.70s – 18.55s) ---
        # "You might think the errors subtract and cancel out."
        card_a_bg = RoundedRectangle(
            width=5.85, height=2.75, corner_radius=0.16,
            fill_color=CARD_BG, fill_opacity=0.94, stroke_color=GREEN_C, stroke_width=2
        ).move_to([-3.2, -1.75, 0])

        card_a_title = Text(
            "If both shift same way (Cancel Out)",
            font_size=19, color=GREEN_C, weight=BOLD
        ).move_to(card_a_bg.get_top() + DOWN * 0.4)

        card_a_desc = MathTex(
            r"\Delta x_1 = +0.5,\quad \Delta x_2 = +0.5",
            font_size=23, color=GREY_A
        ).next_to(card_a_title, DOWN, buff=0.25)

        card_a_eq = MathTex(
            r"\Delta L = (+0.5) - (+0.5) = 0",
            font_size=26, color=GREEN_B
        ).next_to(card_a_desc, DOWN, buff=0.25)

        card_a_note = Text(
            "Bar just slides right — length stays 4.0!",
            font_size=17, color=GREY_B
        ).next_to(card_a_eq, DOWN, buff=0.22)

        # Hai mũi tên xanh lá cùng hướng sang phải (+0.5)
        g_arr_2 = Arrow(
            [nl.n2p(3.0)[0], bar_y, 0], [nl.n2p(3.5)[0], bar_y, 0],
            buff=0, color=GREEN_C, stroke_width=4, max_tip_length_to_length_ratio=0.35
        ).shift(DOWN * 0.02)
        g_arr_1 = Arrow(
            [nl.n2p(7.0)[0], bar_y, 0], [nl.n2p(7.5)[0], bar_y, 0],
            buff=0, color=GREEN_C, stroke_width=4, max_tip_length_to_length_ratio=0.35
        ).shift(DOWN * 0.02)
        g_lbl_2 = MathTex(r"+0.5", font_size=19,
                          color=GREEN_C).next_to(g_arr_2, DOWN, buff=0.14)
        g_lbl_1 = MathTex(r"+0.5", font_size=19,
                          color=GREEN_C).next_to(g_arr_1, DOWN, buff=0.14)

        play(
            FadeIn(card_a_bg), FadeIn(card_a_title), FadeIn(card_a_desc),
            x2_t.animate.set_value(3.5),
            x1_t.animate.set_value(7.5),
            GrowArrow(g_arr_2), GrowArrow(g_arr_1),
            FadeIn(g_lbl_2), FadeIn(g_lbl_1),
            run_time=2.0,
            rate_func=smooth,
        )
        play(Write(card_a_eq), FadeIn(card_a_note), run_time=1.1)
        wait_until(18.55)

        # --- 2C. MINH HỌA "TOO LOW & TOO HIGH" — ÉP NGẮN TỪ 2 ĐẦU (18.55s – 24.55s) ---
        # "But what if x1 is read a bit too low while x2 is read a bit too high?"
        play(
            FadeOut(VGroup(g_arr_2, g_arr_1, g_lbl_2, g_lbl_1)),
            x2_t.animate.set_value(3.0),
            x1_t.animate.set_value(7.0),
            run_time=0.75,
        )

        # Khối lỗi đỏ ở đầu phải (x1 đo hụt sang trái -0.5)
        err1_block = Rectangle(
            width=0.5, height=0.38, fill_color=RED_C, fill_opacity=0.88,
            stroke_color=WHITE, stroke_width=1.5
        ).move_to([(nl.n2p(6.5)[0] + nl.n2p(7.0)[0]) / 2.0, bar_y, 0])
        err1_arrow = Arrow(
            [nl.n2p(7.0)[0], bar_y + 0.92,
             0], [nl.n2p(6.5)[0], bar_y + 0.92, 0],
            buff=0, color=RED_C, stroke_width=3.5, max_tip_length_to_length_ratio=0.35
        )
        err1_txt = MathTex(r"-0.5\text{ (too low)}", font_size=19, color=RED_B).next_to(
            err1_arrow, RIGHT, buff=0.1
        )

        # Trượt x1 sang trái (7.0 -> 6.5) đúng lúc đọc "x1 is read a bit too low"
        play(
            x1_t.animate.set_value(6.5),
            FadeIn(err1_block),
            GrowArrow(err1_arrow),
            FadeIn(err1_txt),
            run_time=1.8,
            rate_func=smooth,
        )

        # Khối lỗi đỏ ở đầu trái (x2 đo dư sang phải +0.5)
        err2_block = Rectangle(
            width=0.5, height=0.38, fill_color="#DC2626", fill_opacity=0.88,
            stroke_color=WHITE, stroke_width=1.5
        ).move_to([(nl.n2p(3.0)[0] + nl.n2p(3.5)[0]) / 2.0, bar_y, 0])
        err2_arrow = Arrow(
            [nl.n2p(3.0)[0], bar_y + 0.92,
             0], [nl.n2p(3.5)[0], bar_y + 0.92, 0],
            buff=0, color=RED_C, stroke_width=3.5, max_tip_length_to_length_ratio=0.35
        )
        err2_txt = MathTex(r"+0.5\text{ (too high)}", font_size=19, color=RED_B).next_to(
            err2_arrow, LEFT, buff=0.1
        )

        # Trượt x2 sang phải (3.0 -> 3.5) đúng lúc đọc "while x2 is read a bit too high?"
        play(
            x2_t.animate.set_value(3.5),
            FadeIn(err2_block),
            GrowArrow(err2_arrow),
            FadeIn(err2_txt),
            run_time=1.9,
            rate_func=smooth,
        )
        wait_until(24.55)

        # --- 2D. GẠCH BỎ CANCEL OUT & XẾP CHỒNG 2 LỖI THÀNH BIÊN CỰC ĐẠI (24.55s – 33.80s) ---
        # "Instead of cancelling, their errors pile up into the worst-case bound: |Δx1| + |Δx2|."
        cross_a = VGroup(
            Line(card_a_bg.get_corner(DL) + UR * 0.25,
                 card_a_bg.get_corner(UR) + DL * 0.25, color=RED_C, stroke_width=4.5),
            Line(card_a_bg.get_corner(UL) + DR * 0.25,
                 card_a_bg.get_corner(DR) + UL * 0.25, color=RED_C, stroke_width=4.5),
        )

        card_b_bg = RoundedRectangle(
            width=6.05, height=2.75, corner_radius=0.16,
            fill_color=CARD_BG, fill_opacity=0.96, stroke_color=RED_C, stroke_width=2.5
        ).move_to([3.2, -1.75, 0])

        card_b_title = Text(
            "Opposite signs → Errors Pile Up!",
            font_size=20, color=RED_B, weight=BOLD
        ).move_to(card_b_bg.get_top() + DOWN * 0.38)

        card_b_calc = MathTex(
            r"\Delta L = (-0.5) - (+0.5) = -1.0\;\text{ (Doubled!)}",
            font_size=22, color=YELLOW_C
        ).next_to(card_b_title, DOWN, buff=0.2)

        play(
            Create(cross_a),
            VGroup(card_a_bg, card_a_title, card_a_desc, card_a_eq,
                   card_a_note).animate.set_opacity(0.45),
            FadeIn(card_b_bg), FadeIn(card_b_title), Write(card_b_calc),
            run_time=1.6,
        )
        # Chờ đến đúng cụm "...the absolute value of delta x1 plus the absolute value of delta x2." (~28.8s)
        wait_until(28.50)

        # Tách 2 khối lỗi đỏ từ 2 đầu thước bay xuống ghép nối đuôi nhau trong Thẻ B!
        fly_err1 = err1_block.copy()
        fly_err2 = err2_block.copy()

        target_b1 = Rectangle(
            width=1.05, height=0.36, fill_color=RED_C, fill_opacity=0.95,
            stroke_color=WHITE, stroke_width=1.5
        ).move_to([2.65, -1.72, 0])
        target_b2 = Rectangle(
            width=1.05, height=0.36, fill_color="#DC2626", fill_opacity=0.95,
            stroke_color=WHITE, stroke_width=1.5
        ).next_to(target_b1, RIGHT, buff=0.04)

        b1_in = MathTex(r"|\Delta x_1|", font_size=18,
                        color=WHITE).move_to(target_b1.get_center())
        b2_in = MathTex(r"|\Delta x_2|", font_size=18,
                        color=WHITE).move_to(target_b2.get_center())

        play(
            Transform(fly_err1, target_b1),
            Transform(fly_err2, target_b2),
            run_time=2.0,
            rate_func=smooth,
        )

        stacked_pair = VGroup(fly_err1, fly_err2)
        bound_eq = MathTex(
            r"|\Delta L| \le |\Delta x_1| + |\Delta x_2|",
            font_size=27, color=WHITE
        ).move_to(card_b_bg.get_bottom() + UP * 0.45)

        play(
            FadeIn(b1_in), FadeIn(b2_in),
            Write(bound_eq),
            run_time=1.5,
        )
        play(Indicate(bound_eq, color=YELLOW_C, scale_factor=1.1), run_time=0.8)
        wait_until(33.80)

        # --- 2E. Chuyển về hàm 1 biến của Giải tích 1 (33.80s – 41.80s) ---
        # "Since that's a two-variable example, we'll leave it there and return to single-variable functions for Calculus 1."
        part2_all = VGroup(
            nl, true_mark_2, true_mark_1, dyn_pin_x2, dyn_pin_x1, dyn_L_bar, dyn_L_readout,
            err1_block, err1_arrow, err1_txt, err2_block, err2_arrow, err2_txt,
            card_a_bg, card_a_title, card_a_desc, card_a_eq, card_a_note, cross_a,
            card_b_bg, card_b_title, card_b_calc, stacked_pair, b1_in, b2_in, bound_eq,
        )

        bridge_content = VGroup(
            Text("2-Variable Example  ✓", font_size=22, color=GREY_A),
            MathTex(r"\longrightarrow", font_size=34, color=YELLOW_C),
            Text("Single-Variable: y = f(x)  (Calculus 1)",
                 font_size=23, color=TEAL_C, weight=BOLD),
        ).arrange(RIGHT, buff=0.28)
        bridge_box = SurroundingRectangle(
            bridge_content, color=TEAL_C, buff=0.28, corner_radius=0.16,
            fill_color=CARD_BG, fill_opacity=0.97
        )
        bridge_pill = VGroup(bridge_box, bridge_content).move_to(DOWN * 0.1)

        play(
            part2_all.animate.set_opacity(0.15),
            FadeIn(bridge_pill, scale=0.92),
            run_time=1.3,
        )
        # Chờ đến khoảng nghỉ dài 1.45s giữa 40.65s và 42.10s
        wait_until(40.70)
        play(FadeOut(part2_all), FadeOut(bridge_pill), run_time=1.1)

        # =====================================================================
        # PHẦN 3: HÀM 1 BIẾN y = f(x) — DAO ĐỘNG DẤU & LẤY ĐỘ LỚN (42.00s – 57.65s)
        # =====================================================================
        wait_until(42.00)

        ax = Axes(
            x_range=[0, 4.2, 1],
            y_range=[0, 4.2, 1],
            x_length=5.6,
            y_length=4.5,
            axis_config={
                "color": GREY_B,
                "stroke_width": 2,
                "include_tip": True,
                "tip_width": 0.14,
                "tip_height": 0.14,
            },
        ).move_to([-2.6, -0.45, 0])

        ax_x_lbl = MathTex(r"x", font_size=24, color=GREY_B).next_to(
            ax.x_axis.get_end(), DOWN, buff=0.1)
        ax_y_lbl = MathTex(r"y", font_size=24, color=GREY_B).next_to(
            ax.y_axis.get_end(), LEFT, buff=0.1)

        a_pt = 2.0

        def f1(x):
            return 0.18 * (x**2) + 0.30 * x + 0.65

        def L1(x):
            return f1(a_pt) + 1.02 * (x - a_pt)

        curve1 = ax.plot(f1, x_range=[0.25, 3.65],
                         color=BLUE_C, stroke_width=3.6)
        tan1 = ax.plot(L1, x_range=[0.35, 3.65],
                       color=YELLOW_C, stroke_width=2.8)
        dot_a = Dot(ax.c2p(a_pt, f1(a_pt)), color=WHITE, radius=0.075)
        lbl_a = MathTex(r"(a, f(a))", font_size=20,
                        color=WHITE).next_to(dot_a, UL, buff=0.1)

        dx_tracker = ValueTracker(0.75)

        def get_wobble_dx():
            dx = dx_tracker.get_value()
            if abs(dx) < 0.02:
                return VGroup()
            p1 = ax.c2p(a_pt, f1(a_pt))
            p2 = ax.c2p(a_pt + dx, f1(a_pt))
            col = BLUE_B if dx >= 0 else ORANGE
            seg = Line(p1, p2, color=col, stroke_width=4.5)
            lbl = MathTex(r"\Delta x", font_size=21, color=col).next_to(
                seg, DOWN if dx >= 0 else UP, buff=0.1
            )
            return VGroup(seg, lbl)

        def get_wobble_dy():
            dx = dx_tracker.get_value()
            if abs(dx) < 0.02:
                return VGroup()
            p_base = ax.c2p(a_pt + dx, f1(a_pt))
            p_tan = ax.c2p(a_pt + dx, L1(a_pt + dx))
            col = TEAL_C if dx >= 0 else RED_C
            seg = Line(p_base, p_tan, color=col, stroke_width=5)
            dot = Dot(p_tan, color=col, radius=0.07)
            lbl = MathTex(r"dy", font_size=22, color=col).next_to(
                seg, RIGHT if dx >= 0 else LEFT, buff=0.12
            )
            return VGroup(seg, dot, lbl)

        dyn_dx = always_redraw(get_wobble_dx)
        dyn_dy = always_redraw(get_wobble_dy)

        sign_panel_bg = RoundedRectangle(
            width=5.2, height=2.25, corner_radius=0.15,
            fill_color=CARD_BG, fill_opacity=0.92, stroke_color=SLATE, stroke_width=1.8
        ).move_to([3.65, 1.0, 0])

        sign_hdr = Text(
            "Single Variable: Sign Still Matters", font_size=19, color=YELLOW_C, weight=BOLD
        ).move_to(sign_panel_bg.get_top() + DOWN * 0.4)

        dyn_sign_readout = always_redraw(
            lambda: VGroup(
                MathTex(
                    rf"\Delta x = {dx_tracker.get_value():+.2f}",
                    font_size=28,
                    color=BLUE_B if dx_tracker.get_value() >= 0 else ORANGE,
                ),
                MathTex(
                    rf"dy = {1.02 * dx_tracker.get_value():+.2f}",
                    font_size=28,
                    color=TEAL_C if dx_tracker.get_value() >= 0 else RED_C,
                ),
            )
            .arrange(DOWN, buff=0.22)
            .move_to(sign_panel_bg.get_center() + DOWN * 0.22)
        )

        # "For a single variable y = f(x), the sign of the error still matters." (42.1s – 47.2s)
        play(
            Create(ax), Write(ax_x_lbl), Write(ax_y_lbl),
            Create(curve1), Create(tan1), FadeIn(dot_a), Write(lbl_a),
            FadeIn(dyn_dx), FadeIn(dyn_dy),
            FadeIn(sign_panel_bg), FadeIn(sign_hdr), FadeIn(dyn_sign_readout),
            run_time=2.0,
        )
        wait_until(47.90)

        # "Delta x can wobble to the left or to the right, and dy flips sign right along with it." (48.1s – 53.25s)
        play(dx_tracker.animate.set_value(-0.75),
             run_time=1.3, rate_func=smooth)
        play(dx_tracker.animate.set_value(0.75), run_time=1.3, rate_func=smooth)
        play(dx_tracker.animate.set_value(-0.70),
             run_time=1.2, rate_func=smooth)
        play(dx_tracker.animate.set_value(0.75), run_time=1.3, rate_func=smooth)
        wait_until(53.50)

        # "Because we want the worst-case bound, we take the magnitude." (53.5s – 57.25s)
        mag_bg = RoundedRectangle(
            width=5.2, height=1.75, corner_radius=0.15,
            fill_color=CARD_BG, fill_opacity=0.95, stroke_color=GREEN_C, stroke_width=2
        ).move_to([3.65, -1.35, 0])
        mag_hdr = Text(
            "Worst-Case Bound → Take Magnitude", font_size=18, color=GREEN_C, weight=BOLD
        ).move_to(mag_bg.get_top() + DOWN * 0.42)
        mag_eq_plain = MathTex(r"dy = f'(a)\,\Delta x", font_size=28, color=GREY_A).move_to(
            mag_bg.get_center() + DOWN * 0.25
        )
        mag_eq_abs = MathTex(r"|dy| = |f'(a)|\,|\Delta x|", font_size=30, color=YELLOW_C).move_to(
            mag_bg.get_center() + DOWN * 0.25
        )

        play(FadeIn(mag_bg), FadeIn(mag_hdr),
             Write(mag_eq_plain), run_time=1.4)
        wait_until(56.00)
        # Đóng dấu trị tuyệt đối ngay lúc nói "...we take the magnitude."
        play(ReplacementTransform(mag_eq_plain, mag_eq_abs), run_time=1.1)
        wait_until(57.65)

        # =====================================================================
        # PHẦN 4: ĐỊNH LÝ 1 — QUY TẮC SAI SỐ TUYỆT ĐỐI (57.65s – 69.00s)
        # "This gives Theorem 1, the absolute-error law:
        #  |Δy| ≈ |f'(a)| · Δx."
        # =====================================================================
        play(
            FadeOut(VGroup(sign_panel_bg, sign_hdr,
                    dyn_sign_readout, mag_bg, mag_hdr, mag_eq_abs)),
            run_time=0.55,
        )

        thm_title = Text(
            "THEOREM 1: ABSOLUTE-ERROR LAW",
            font_size=20,
            color=YELLOW_C,
            weight=BOLD,
        )
        thm_eq = MathTex(
            r"|\Delta y|", r"\approx", r"|f'(a)|", r"\,|\Delta x|",
            font_size=38,
            color=WHITE,
        )
        thm_eq[0].set_color(TEAL_C)
        thm_eq[2].set_color(YELLOW_C)
        thm_eq[3].set_color(BLUE_B)

        thm_note = Text(
            "Worst-case absolute error bound",
            font_size=18,
            color=GREY_A,
        )
        thm_content = VGroup(
            thm_title, thm_eq, thm_note).arrange(DOWN, buff=0.25)
        thm_box = SurroundingRectangle(
            thm_content, color=YELLOW_C, buff=0.3, corner_radius=0.16,
            fill_color=CARD_BG, fill_opacity=0.96
        )
        thm_card = VGroup(thm_box, thm_content).move_to([3.65, 0.35, 0])

        play(FadeIn(thm_box), FadeIn(thm_title), run_time=1.2)
        wait_until(61.10)

        # Khớp từng thành phần công thức đúng nhịp đọc 61.3s -> 68.65s
        play(Write(thm_eq[0]), Write(thm_eq[1]), run_time=1.8)
        play(Write(thm_eq[2]), run_time=1.5)
        play(Indicate(thm_eq[2], color=ORANGE,
             scale_factor=1.22), run_time=1.0)
        # Ngừng nhịp đúng khoảng pause trước "...times delta x" (67.60s)
        wait_until(67.40)
        play(Write(thm_eq[3]), FadeIn(thm_note), run_time=1.2)
        wait_until(69.00)

        # =====================================================================
        # PHẦN 5: ĐỘ DỐC |f'(a)| LÀ BỘ KHUẾCH ĐẠI SAI SỐ (69.00s – 81.92s)
        # "Notice how the steepness of the slope, |f'(a)|, acts like an error
        #  amplifier — the steeper the curve, the more it magnifies a tiny
        #  measurement slip."
        # =====================================================================
        play(
            thm_card.animate.scale(0.86).move_to([3.65, 1.55, 0]),
            FadeOut(VGroup(curve1, tan1, dot_a, lbl_a, dyn_dx, dyn_dy)),
            run_time=1.0,
        )

        # Khóa cứng một sai số đầu vào rất nhỏ Δx, thay đổi độ dốc |f'(a)| từ 0.35 lên 2.85
        slope_tracker = ValueTracker(0.35)
        amp_x0 = 1.65
        amp_y0 = 1.00
        fixed_dx = 0.72

        amp_dot_a = Dot(ax.c2p(amp_x0, amp_y0), color=WHITE, radius=0.075)
        fixed_dx_seg = Line(
            ax.c2p(amp_x0, amp_y0),
            ax.c2p(amp_x0 + fixed_dx, amp_y0),
            color=BLUE_B,
            stroke_width=5.5,
        )
        fixed_dx_lbl = MathTex(r"\Delta x\text{ (tiny, fixed)}", font_size=19, color=BLUE_B).next_to(
            fixed_dx_seg, DOWN, buff=0.14
        )

        def get_amp_curve():
            m = slope_tracker.get_value()
            x_min = max(0.35, amp_x0 + (0.25 - amp_y0) / max(m, 0.2))
            x_max = min(3.85, amp_x0 + (3.85 - amp_y0) / max(m, 0.2))
            return ax.plot(
                lambda x: amp_y0 + m * (x - amp_x0) +
                0.06 * ((x - amp_x0) ** 2),
                x_range=[x_min, x_max],
                color=BLUE_C,
                stroke_width=3.2,
            )

        def get_amp_tangent():
            m = slope_tracker.get_value()
            x_min = max(0.35, amp_x0 + (0.25 - amp_y0) / max(m, 0.2))
            x_max = min(3.85, amp_x0 + (3.95 - amp_y0) / max(m, 0.2))
            return ax.plot(
                lambda x: amp_y0 + m * (x - amp_x0),
                x_range=[x_min, x_max],
                color=RED_C if m > 1.8 else (YELLOW_C if m > 1.0 else GREEN_C),
                stroke_width=3.2,
            )

        def get_amp_output():
            m = slope_tracker.get_value()
            p_base = ax.c2p(amp_x0 + fixed_dx, amp_y0)
            p_top = ax.c2p(amp_x0 + fixed_dx, amp_y0 + m * fixed_dx)
            col = RED_C if m > 1.8 else (YELLOW_C if m > 1.0 else GREEN_C)
            bar = Line(p_base, p_top, color=col, stroke_width=7.5)
            tip = Dot(p_top, color=col, radius=0.08)
            lbl = MathTex(r"|dy|", font_size=25, color=col).next_to(
                bar, RIGHT, buff=0.14)
            return VGroup(bar, tip, lbl)

        dyn_amp_curve = always_redraw(get_amp_curve)
        dyn_amp_tan = always_redraw(get_amp_tangent)
        dyn_amp_out = always_redraw(get_amp_output)

        meter_bg = RoundedRectangle(
            width=5.25, height=2.55, corner_radius=0.15,
            fill_color=CARD_BG, fill_opacity=0.94, stroke_color=ORANGE, stroke_width=2
        ).move_to([3.65, -1.25, 0])

        meter_hdr = Text(
            "Slope = Error Amplifier", font_size=21, color=ORANGE, weight=BOLD
        ).move_to(meter_bg.get_top() + DOWN * 0.42)

        meter_bar_w = 4.3
        meter_track = Rectangle(
            width=meter_bar_w, height=0.34, color=GREY_D, fill_opacity=0.65, stroke_width=1.2
        ).move_to(meter_bg.get_bottom() + UP * 0.55)

        dyn_meter_fill = always_redraw(
            lambda: Rectangle(
                width=max(meter_bar_w *
                          min(slope_tracker.get_value() / 3.0, 1.0), 0.08),
                height=0.34,
                color=RED_C if slope_tracker.get_value() > 1.8 else (
                    YELLOW_C if slope_tracker.get_value() > 1.0 else GREEN_C),
                fill_opacity=0.95,
                stroke_width=0,
            )
            .align_to(meter_track, LEFT)
            .set_y(meter_track.get_y())
        )

        dyn_meter_readout = always_redraw(
            lambda: MathTex(
                rf"|f'(a)| = {slope_tracker.get_value():.2f}\times",
                font_size=30,
                color=RED_B if slope_tracker.get_value() > 1.8 else (
                    YELLOW_C if slope_tracker.get_value() > 1.0 else GREEN_C),
            ).move_to(meter_bg.get_center() + UP * 0.08)
        )

        play(
            FadeIn(dyn_amp_curve), FadeIn(dyn_amp_tan), FadeIn(amp_dot_a),
            GrowFromEdge(fixed_dx_seg, LEFT), FadeIn(
                fixed_dx_lbl), FadeIn(dyn_amp_out),
            FadeIn(meter_bg), FadeIn(meter_hdr), FadeIn(meter_track),
            FadeIn(dyn_meter_fill), FadeIn(dyn_meter_readout),
            run_time=1.4,
        )
        # Khớp câu "...the absolute value of f prime of a," (71.95s – 74.25s)
        wait_until(72.00)
        play(
            Indicate(thm_eq[2], color=ORANGE, scale_factor=1.2),
            Indicate(dyn_meter_readout, color=YELLOW_C, scale_factor=1.15),
            run_time=1.5,
        )
        # Khớp câu "...acts like an error amplifier —" (74.55s – 76.75s)
        wait_until(74.40)
        play(slope_tracker.animate.set_value(
            1.45), run_time=2.2, rate_func=smooth)

        # Khớp câu "...the steeper the curve, the more it magnifies a tiny measurement slip." (77.10s – 81.10s)
        wait_until(77.00)
        play(slope_tracker.animate.set_value(
            2.85), run_time=3.5, rate_func=smooth)
        play(Indicate(dyn_meter_readout, color=RED_C,
             scale_factor=1.18), run_time=0.8)

        # Kết thúc chuẩn xác tại cuối file audio (81.92s)
        wait_until(81.92)
