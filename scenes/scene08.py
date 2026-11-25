from manim import *
import numpy as np


class Scene08(Scene):
    def construct(self):
        # Bảng màu tối giản đồng bộ toàn bộ dự án
        self.camera.background_color = "#0F172A"
        SLATE = "#64748B"
        WOOD_FILL = "#92400E"
        WOOD_STROKE = "#F59E0B"

        # Tự động ghép file tiếng khi render nháp (thêm dấu # khi render final không tiếng)
        self.add_sound("Recordings/Scene8.wav")

        # Bộ đếm thời gian khóa cứng từng mốc giây khớp 100% với Scene8.wav (40.87s -> 41.20s)
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
            "Summary & Takeaways",
            font_size=25,
            color=YELLOW_C,
            weight=BOLD,
        ).to_edge(UP, buff=0.38).shift(RIGHT * 1.2)

        # =====================================================================
        # BEAT 1 (0.00s – 20.10s): HAI QUY TẮC GỌN ĐẸP & HÀNG RÀO TRỊ TUYỆT ĐỐI
        # "To wrap up, calculus turns messy error propagation into two clean
        #  rules: one, the derivative gives us the worst-case absolute error,
        #  and the logarithmic derivative gives us the relative error, with
        #  absolute value bars ensuring that worst-case errors never falsely
        #  cancel out."
        # =====================================================================
        wrap_txt = Text("TO WRAP UP", font_size=34, color=WHITE,
                        weight=BOLD).move_to([0, 0.35, 0])
        wrap_line = Line(LEFT * 2.2, RIGHT * 2.2, color=YELLOW_C, stroke_width=2.5).next_to(
            wrap_txt, DOWN, buff=0.22
        )

        play(
            FadeIn(sec_title, shift=DOWN * 0.15),
            FadeIn(wrap_txt, shift=UP * 0.12),
            Create(wrap_line),
            run_time=1.2,
        )

        # 1.90s: "calculus turns messy error propagation into two clean rules:"
        wait_until(1.90)

        messy_expr = MathTex(
            r"\Delta y = f(a + \Delta x) - f(a)", font_size=34, color=GREY_B
        ).move_to([0, 0.25, 0])

        mid_div = Line([0, 1.85, 0], [0, -0.75, 0], color=SLATE,
                       stroke_width=1.4, stroke_opacity=0.45)

        r1_hdr = Text("1 · ABSOLUTE ERROR", font_size=19,
                      color=YELLOW_C, weight=BOLD).move_to([-3.3, 1.55, 0])
        r2_hdr = Text("2 · RELATIVE ERROR", font_size=19,
                      color=TEAL_C, weight=BOLD).move_to([3.3, 1.55, 0])

        play(
            FadeOut(VGroup(wrap_txt, wrap_line)),
            FadeIn(messy_expr, scale=0.92),
            run_time=0.9,
        )
        play(
            FadeOut(messy_expr, scale=1.15),
            Create(mid_div),
            FadeIn(r1_hdr, shift=DOWN * 0.12),
            FadeIn(r2_hdr, shift=DOWN * 0.12),
            run_time=1.9,
            rate_func=smooth,
        )

        # 5.55s: "one, the derivative gives us the worst-case absolute error,"
        wait_until(5.55)
        r1_eq = MathTex(
            r"|", r"\Delta y", r"|", r"\approx", r"|", r"f'(a)", r"|", r"\,|", r"\Delta x", r"|",
            font_size=40, color=WHITE
        ).move_to([-3.3, 0.55, 0])
        r1_eq[1].set_color(TEAL_C)
        r1_eq[5].set_color(YELLOW_C)
        r1_eq[8].set_color(BLUE_B)

        r1_sub = Text("Derivative  →  Worst-case bound",
                      font_size=18, color=GREY_A).move_to([-3.3, -0.35, 0])
        r1_flash = Line(
            r1_eq[4].get_left(), r1_eq[6].get_right(), color=YELLOW_C, stroke_width=4.0
        ).next_to(r1_eq[5], DOWN, buff=0.14)

        play(Write(r1_eq), FadeIn(r1_sub, shift=UP * 0.1), run_time=2.1)
        play(ShowPassingFlash(r1_flash, time_width=0.55), run_time=0.8)

        # 9.35s: "and the logarithmic derivative gives us the relative error,"
        wait_until(9.35)
        r2_eq = MathTex(
            r"\frac{|\Delta y|}{|f(a)|}",
            r"\approx",
            r"\Big|",
            r"\,d\big(\ln|f(a)|\big)\,",
            r"\Big|",
            font_size=36, color=WHITE
        ).move_to([3.3, 0.55, 0])
        r2_eq[0].set_color(TEAL_C)
        r2_eq[3].set_color(YELLOW_C)

        r2_sub = Text("Logarithmic Derivative  →  % Error",
                      font_size=18, color=GREY_A).move_to([3.3, -0.35, 0])
        r2_flash = Line(
            r2_eq[2].get_left(), r2_eq[4].get_right(), color=TEAL_C, stroke_width=4.0
        ).next_to(r2_eq[3], DOWN, buff=0.14)

        play(Write(r2_eq), FadeIn(r2_sub, shift=UP * 0.1), run_time=2.3)
        play(ShowPassingFlash(r2_flash, time_width=0.55), run_time=0.8)

        # 13.40s: "with absolute value bars ensuring that"
        wait_until(13.40)
        abs_bars_grp = VGroup(
            r1_eq[0], r1_eq[2], r1_eq[4], r1_eq[6], r1_eq[7], r1_eq[9],
            r2_eq[2], r2_eq[4],
        )

        bot_div = Line([-5.2, -1.15, 0], [5.2, -1.15, 0],
                       color=SLATE, stroke_width=1.2, stroke_opacity=0.4)
        guard_sym = MathTex(r"\Big|\;\cdot\;\Big|", font_size=42,
                            color=YELLOW_C).move_to([-3.65, -1.95, 0])

        play(
            abs_bars_grp.animate.set_color(YELLOW_C),
            Indicate(abs_bars_grp, color=ORANGE, scale_factor=1.18),
            Create(bot_div),
            FadeIn(guard_sym, scale=0.85),
            run_time=2.3,
        )

        # 15.95s: "worst-case errors never falsely cancel out."
        wait_until(15.95)
        guard_txt = Text(
            "Worst-case errors never falsely cancel out",
            font_size=24, color=WHITE, weight=BOLD
        ).next_to(guard_sym, RIGHT, buff=0.4)
        guard_flash = Line(
            guard_txt.get_left(), guard_txt.get_right(), color=YELLOW_C, stroke_width=3.5
        ).next_to(guard_txt, DOWN, buff=0.12)

        play(FadeIn(guard_txt, shift=RIGHT * 0.15), run_time=1.5)
        play(ShowPassingFlash(guard_flash, time_width=0.55), run_time=1.1)

        wait_until(19.25)
        beat1_all = VGroup(
            mid_div, r1_hdr, r2_hdr, r1_eq, r1_sub, r2_eq, r2_sub,
            bot_div, guard_sym, guard_txt,
        )
        play(FadeOut(beat1_all), run_time=0.85)

        # =====================================================================
        # BEAT 2 (20.90s – 32.10s): ỨNG DỤNG THỰC TẾ TRONG NGƯỠNG 5%
        # "Across our applications, linearization proves to be a fast, reliable
        #  field tool, as long as our uncertainty stays inside that 5%
        #  discrepancy threshold."
        # =====================================================================
        wait_until(20.90)

        # Hồi tưởng tối giản Case 1 (bên trái trên)
        mini_table_disc = Circle(
            radius=0.38, fill_color=WOOD_FILL, fill_opacity=0.92,
            stroke_color=WOOD_STROKE, stroke_width=1.4
        )
        mini_table_trim = Annulus(
            inner_radius=0.38, outer_radius=0.46,
            fill_color=RED_C, fill_opacity=0.85, stroke_width=0
        )
        mini_table_icon = VGroup(mini_table_disc, mini_table_trim)
        mini_table_txt = VGroup(
            Text("Case 1 · Tabletop", font_size=18, color=WHITE, weight=BOLD),
            MathTex(r"0.84\% < 5\%\;\checkmark", font_size=21, color=GREEN_C),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        cb1 = VGroup(mini_table_icon, mini_table_txt).arrange(
            RIGHT, buff=0.28).move_to([-3.25, 1.4, 0])

        # Hồi tưởng tối giản Case 2 (bên phải trên)
        mt_trunk = Rectangle(width=0.08, height=0.26, fill_color=WOOD_FILL,
                             fill_opacity=0.95, stroke_width=0).shift(DOWN * 0.25)
        mt_leaves = Polygon(
            [-0.28, -0.15, 0], [0.28, -0.15, 0], [0, 0.45, 0],
            fill_color="#22C55E", fill_opacity=0.95, stroke_width=0
        )
        mt_ray = Line([0.48, -0.32, 0], [0, 0.45, 0],
                      color=YELLOW_C, stroke_width=2.0)
        mini_tree_icon = VGroup(mt_trunk, mt_leaves, mt_ray)
        mini_tree_txt = VGroup(
            Text("Case 2 · Tree Height", font_size=18, color=WHITE, weight=BOLD),
            MathTex(r"1.47\% < 5\%\;\checkmark", font_size=21, color=GREEN_C),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        cb2 = VGroup(mini_tree_icon, mini_tree_txt).arrange(
            RIGHT, buff=0.25).move_to([3.25, 1.4, 0])

        play(
            FadeIn(cb1, shift=UP * 0.15),
            FadeIn(cb2, shift=UP * 0.15),
            run_time=1.75,
        )

        # 22.85s: "linearization proves to be a fast, reliable field tool,"
        wait_until(22.85)
        tool_hdr = Text(
            "Linearization: A Fast, Reliable Field Tool",
            font_size=31, color=WHITE, weight=BOLD
        ).move_to([0, -0.05, 0])
        tool_rule = Line(LEFT * 3.8, RIGHT * 3.8, color=TEAL_C, stroke_width=2.4, stroke_opacity=0.8).next_to(
            tool_hdr, DOWN, buff=0.18
        )
        play(FadeIn(tool_hdr, shift=UP * 0.12),
             Create(tool_rule), run_time=2.8)

        # 26.75s: "as long as our uncertainty stays inside that 5% discrepancy threshold."
        wait_until(26.75)

        b_w = 8.8
        b_y = -1.85
        b_left = -b_w / 2.0  # -4.4
        # Thang đo 0% -> 10% (vạch 5% nằm chính giữa x = 0.0)
        g_zone = RoundedRectangle(
            width=b_w * 0.5, height=0.24, corner_radius=0.06,
            fill_color=GREEN_C, fill_opacity=0.88, stroke_width=0
        ).move_to([-b_w * 0.25, b_y, 0])
        r_zone = RoundedRectangle(
            width=b_w * 0.5, height=0.24, corner_radius=0.06,
            fill_color=RED_C, fill_opacity=0.30, stroke_width=0
        ).move_to([b_w * 0.25, b_y, 0])

        thresh_line = Line([0, b_y - 0.38, 0], [0, b_y +
                           0.42, 0], color=YELLOW_C, stroke_width=3.2)
        thresh_lbl = MathTex(r"5\%\text{ Threshold}", font_size=22, color=YELLOW_C).next_to(
            thresh_line, UP, buff=0.08
        )
        acc_lbl = Text("SAFE ZONE  (< 5%)", font_size=16, color=GREEN_C, weight=BOLD).move_to(
            [-2.2, b_y - 0.65, 0]
        )
        rej_lbl = Text("BEYOND LIMITS  (> 5%)", font_size=16, color=RED_B, weight=BOLD).move_to(
            [2.2, b_y - 0.65, 0]
        )

        # Hai chấm kết quả của Case 1 (0.84%) & Case 2 (1.47%) đặt nhãn lệch trên/dưới để tuyệt đối không đè nhau
        x_c1 = b_left + b_w * (0.84 / 10.0)
        x_c2 = b_left + b_w * (1.47 / 10.0)
        dot_c1 = Dot([x_c1, b_y, 0], color=WHITE, radius=0.095)
        dot_c2 = Dot([x_c2, b_y, 0], color=WHITE, radius=0.095)
        lbl_c1 = MathTex(r"0.84\%", font_size=20, color=GREEN_B).move_to(
            [x_c1, b_y + 0.36, 0])
        lbl_c2 = MathTex(r"1.47\%", font_size=20, color=GREEN_B).move_to(
            [x_c2, b_y - 0.34, 0])

        bar_base = VGroup(g_zone, r_zone, thresh_line,
                          thresh_lbl, acc_lbl, rej_lbl)
        c_dots = VGroup(dot_c1, dot_c2, lbl_c1, lbl_c2)

        play(
            FadeIn(bar_base, shift=UP * 0.15),
            FadeIn(c_dots, scale=0.8),
            run_time=3.6,
            rate_func=smooth,
        )
        play(
            Indicate(thresh_lbl, color=YELLOW_A, scale_factor=1.12),
            Indicate(g_zone, color=GREEN_B, scale_factor=1.04),
            run_time=0.9,
        )

        # 31.60s: Giữ lại thanh 5% trượt nhẹ xuống đáy, dọn phần trên cho Beat 3
        wait_until(31.60)
        play(
            FadeOut(VGroup(cb1, cb2, tool_hdr, tool_rule, c_dots)),
            bar_base.animate.shift(DOWN * 0.5),
            run_time=0.5,
        )

        # =====================================================================
        # BEAT 3 (32.15s – 39.30s): VƯỢT GIỚI HẠN -> TAYLOR BẬC 2 & NHIỀU BIẾN
        # "Beyond those limits, we reach for second-order Taylor corrections
        #  or multivariable differentials."
        # =====================================================================
        wait_until(32.15)

        b_y3 = b_y - 0.5  # -2.35
        ptr_x = ValueTracker(b_left + b_w * 0.15)
        dyn_beyond_dot = always_redraw(
            lambda: Dot(
                [ptr_x.get_value(), b_y3, 0],
                color=RED_C if ptr_x.get_value() > 0 else GREEN_C,
                radius=0.11,
            )
        )
        self.add(dyn_beyond_dot)

        play(
            g_zone.animate.set_fill(opacity=0.22),
            r_zone.animate.set_fill(opacity=0.72),
            ptr_x.animate.set_value(b_left + b_w * 0.78),
            run_time=1.2,
            rate_func=smooth,
        )

        # 33.45s: "we reach for second-order Taylor corrections"
        wait_until(33.45)

        b3_div = Line([0, 1.95, 0], [0, -1.25, 0], color=SLATE,
                      stroke_width=1.4, stroke_opacity=0.45)

        # Cột trái: Đường cong + tiếp tuyến mờ + Parabol Taylor bậc 2 ôm sát đường cong!
        tay_hdr = Text("2ND-ORDER TAYLOR", font_size=19,
                       color=YELLOW_C, weight=BOLD).move_to([-3.3, 1.8, 0])

        mini_ax = Axes(
            x_range=[0, 2.2, 1],
            y_range=[0, 3.0, 1],
            x_length=3.6,
            y_length=1.65,
            axis_config={
                "color": GREY_B,
                "stroke_width": 1.4,
                "include_ticks": False,
                "include_tip": True,
                "tip_width": 0.1,
                "tip_height": 0.1,
            },
        ).move_to([-3.3, 0.58, 0])

        # Đường cong thật f(x) = 0.08x^3 + 0.36x^2 + 0.35x
        t_true = mini_ax.plot(lambda x: 0.08 * (x**3) + 0.36 * (x**2) +
                              0.35 * x, x_range=[0, 2.05], color=BLUE_C, stroke_width=3.2)
        # Tiếp tuyến bậc 1 (lệch xa ở x lớn)
        t_lin = mini_ax.plot(
            lambda x: 0.35 * x, x_range=[0, 2.05], color=GREY_B, stroke_width=2.0, stroke_opacity=0.55)
        # Parabol Taylor bậc 2 (ôm khít đường cong!)
        t_quad = mini_ax.plot(lambda x: 0.36 * (x**2) + 0.35 * x,
                              x_range=[0, 2.05], color=YELLOW_C, stroke_width=3.0)

        tay_eq = MathTex(
            r"\Delta y \approx f'(a)\Delta x", r"+ \tfrac{1}{2}f''(a)(\Delta x)^2",
            font_size=26, color=WHITE
        ).move_to([-3.3, -0.78, 0])
        tay_eq[1].set_color(YELLOW_C)

        play(
            Create(b3_div),
            FadeIn(tay_hdr, shift=DOWN * 0.1),
            Create(mini_ax),
            Create(t_true),
            Create(t_lin),
            Create(t_quad),
            Write(tay_eq),
            run_time=2.8,
            rate_func=smooth,
        )

        # 36.65s: "or multivariable differentials."
        wait_until(36.65)

        mv_hdr = Text("MULTIVARIABLE DIFFERENTIALS", font_size=19,
                      color=TEAL_C, weight=BOLD).move_to([3.3, 1.8, 0])

        # Sơ đồ gọn: (x ± dx, y ± dy) -> z = f(x, y)
        mv_in_x = MathTex(r"x \pm dx", font_size=25,
                          color=BLUE_B).move_to([1.65, 1.02, 0])
        mv_in_y = MathTex(r"y \pm dy", font_size=25,
                          color=ORANGE).move_to([1.65, 0.25, 0])
        mv_fn = MathTex(r"z = f(x, y)", font_size=28,
                        color=TEAL_C).move_to([4.65, 0.64, 0])
        mv_arr1 = Arrow(mv_in_x.get_right(), mv_fn.get_left() + UP * 0.08, buff=0.14,
                        color=BLUE_B, stroke_width=2.2, max_tip_length_to_length_ratio=0.18)
        mv_arr2 = Arrow(mv_in_y.get_right(), mv_fn.get_left() + DOWN * 0.08, buff=0.14,
                        color=ORANGE, stroke_width=2.2, max_tip_length_to_length_ratio=0.18)

        mv_eq = MathTex(
            r"dz =", r"\frac{\partial f}{\partial x}\,dx", r"+", r"\frac{\partial f}{\partial y}\,dy",
            font_size=31, color=WHITE
        ).move_to([3.3, -0.78, 0])
        mv_eq[1].set_color(BLUE_B)
        mv_eq[3].set_color(ORANGE)

        play(
            FadeIn(mv_hdr, shift=DOWN * 0.1),
            FadeIn(VGroup(mv_in_x, mv_in_y, mv_fn)),
            GrowArrow(mv_arr1),
            GrowArrow(mv_arr2),
            Write(mv_eq),
            run_time=1.95,
        )

        # 38.65s: Chuyển sạch sẽ sang màn hình cảm ơn cuối video
        wait_until(38.65)
        beat3_all = VGroup(
            header_badge, header_line, sec_title,
            bar_base, dyn_beyond_dot, b3_div,
            tay_hdr, mini_ax, t_true, t_lin, t_quad, tay_eq,
            mv_hdr, mv_in_x, mv_in_y, mv_fn, mv_arr1, mv_arr2, mv_eq,
        )
        play(FadeOut(beat3_all), run_time=0.65)

        # =====================================================================
        # BEAT 4 (39.35s – 41.20s): OUTRO — THANKS FOR WATCHING!
        # "Thanks for watching!"
        # =====================================================================
        wait_until(39.35)

        thanks_main = Text(
            "Thanks for watching!",
            font_size=52, color=WHITE, weight=BOLD
        ).move_to([0, 0.55, 0])

        thanks_line = Line(LEFT * 3.4, RIGHT * 3.4, color=YELLOW_C, stroke_width=2.6).next_to(
            thanks_main, DOWN, buff=0.28
        )

        credits_group = Text(
            "Group 4 — Class CC01",
            font_size=24, color=TEAL_C, weight=BOLD
        ).next_to(thanks_line, DOWN, buff=0.35)

        credits_sub = Text(
            "Calculus 1 · Topic 9: Differentials, Linearization & Error Propagation",
            font_size=19, color=GREY_B
        ).next_to(credits_group, DOWN, buff=0.18)

        play(
            FadeIn(thanks_main, scale=0.92),
            Create(thanks_line),
            FadeIn(credits_group, shift=UP * 0.12),
            FadeIn(credits_sub, shift=UP * 0.12),
            run_time=1.2,
            rate_func=smooth,
        )

        end_flash = Line(
            thanks_line.get_left(), thanks_line.get_right(),
            color=YELLOW_A, stroke_width=4.5
        ).move_to(thanks_line.get_center())
        play(ShowPassingFlash(end_flash, time_width=0.55), run_time=0.65)

        # Chốt sát cuối audio (40.87s) — giữ ngắn gọn để tiết kiệm tổng thời lượng
        wait_until(41.20)
