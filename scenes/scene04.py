from manim import *
import numpy as np


class Scene04(Scene):
    def construct(self):
        # Bảng màu tối giản đồng bộ toàn bộ dự án
        self.camera.background_color = "#0F172A"
        SLATE = "#64748B"

        # Tự động ghép file tiếng khi render nháp (thêm dấu # khi render final không tiếng)
        self.add_sound("Recordings/Scene04.wav")

        # Bộ đếm thời gian khóa cứng từng mốc giây (tổng đúng 61.18s)
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
            "Theorem 2: The Relative-Error Law",
            font_size=25,
            color=YELLOW_C,
            weight=BOLD,
        ).to_edge(UP, buff=0.38).shift(RIGHT * 1.2)

        # =====================================================================
        # BEAT 1 (0.00s – 7.95s): ĐỒNG HỒ PHẦN TRĂM TỐI GIẢN VS ĐƠN VỊ THÔ
        # "Of course, in engineering and science, knowing the percentage error
        #  often tells us way more than raw units."
        # =====================================================================
        play(FadeIn(sec_title, shift=DOWN * 0.15), run_time=0.7)
        # Chờ đến đúng cụm "...knowing the percentage error" (2.55s)
        wait_until(2.55)

        # Vòng đo mảnh kiểu đồng hồ chính xác ở bên trái (không khung vuông rườm rà)
        dial_c = np.array([-2.35, -0.1, 0])
        dial_track = Circle(
            radius=1.35, color=SLATE, stroke_width=4, stroke_opacity=0.35
        ).move_to(dial_c)
        dial_arc = Arc(
            radius=1.35, start_angle=PI / 2, angle=-TAU * 0.82,
            color=TEAL_C, stroke_width=7, arc_center=dial_c
        )
        dial_glow = Arc(
            radius=1.35, start_angle=PI / 2, angle=-TAU * 0.82,
            color=TEAL_C, stroke_width=16, stroke_opacity=0.18, arc_center=dial_c
        )
        pct_num = MathTex(r"\pm 1.5\%", font_size=44,
                          color=WHITE).move_to(dial_c)
        pct_sub = Text(
            "Percentage Error", font_size=20, color=TEAL_C, weight=BOLD
        ).next_to(dial_track, DOWN, buff=0.32)

        play(
            Create(dial_track),
            Create(dial_arc),
            FadeIn(dial_glow),
            Write(pct_num),
            FadeIn(pct_sub, shift=UP * 0.1),
            run_time=1.9,
            rate_func=smooth,
        )

        # Chờ đến đúng cụm "...way more than raw units." (5.15s)
        wait_until(5.15)

        gt_sym = MathTex(r">", font_size=56,
                         color=YELLOW_C).move_to([0.35, -0.1, 0])
        raw_num = MathTex(r"\pm 0.5\text{ mm}", font_size=38, color=GREY_B).move_to(
            [2.85, -0.1, 0])
        raw_sub = Text("Raw Units", font_size=19, color=GREY_C).next_to(
            raw_num, DOWN, buff=0.95)

        play(
            FadeIn(gt_sym, scale=0.6),
            FadeIn(raw_num, shift=LEFT * 0.2),
            FadeIn(raw_sub),
            run_time=1.3,
        )
        wait_until(7.20)
        play(
            FadeOut(VGroup(dial_track, dial_arc, dial_glow,
                    pct_num, pct_sub, gt_sym, raw_num, raw_sub)),
            run_time=0.75,
        )

        # =====================================================================
        # BEAT 2 (8.10s – 18.75s): BIẾN ĐỔI ĐẠI SỐ THUẦN TÚY GIỮA MÀN HÌNH
        # "If we simply divide both sides of our absolute error law
        #  by the absolute value of f of a, we get Theorem 2, the relative error law."
        # =====================================================================
        wait_until(8.10)

        # Công thức Định lý 1 cỡ lớn, thoáng ở chính giữa màn hình
        thm1_eq = MathTex(
            r"|\Delta y|", r"\approx", r"|f'(a)|", r"\,|\Delta x|",
            font_size=52, color=WHITE
        ).move_to([0, 0.15, 0])
        thm1_eq[0].set_color(TEAL_C)
        thm1_eq[2].set_color(YELLOW_C)
        thm1_eq[3].set_color(BLUE_B)

        thm1_tag = Text(
            "Theorem 1 · Absolute-Error Law", font_size=18, color=GREY_B
        ).next_to(thm1_eq, UP, buff=0.45)

        play(Write(thm1_eq), FadeIn(thm1_tag, shift=DOWN * 0.1), run_time=1.6)

        # Chờ đến đúng cụm "...by the absolute value of f of a," (12.60s)
        wait_until(12.60)

        # Nhấc nhẹ công thức lên, kéo 2 gạch phân số và đẩy mẫu số |f(a)| lên cả 2 vế
        lift_vec = UP * 0.55
        bar_l = Line(
            thm1_eq[0].get_left() + LEFT * 0.12,
            thm1_eq[0].get_right() + RIGHT * 0.12,
            color=WHITE, stroke_width=2.8
        ).next_to(thm1_eq[0], DOWN, buff=0.14).shift(lift_vec)

        bar_r = Line(
            thm1_eq[2].get_left() + LEFT * 0.12,
            thm1_eq[2].get_right() + RIGHT * 0.12,
            color=WHITE, stroke_width=2.8
        ).next_to(thm1_eq[2], DOWN, buff=0.14).shift(lift_vec)

        den_l = MathTex(r"|f(a)|", font_size=46, color=ORANGE).next_to(
            bar_l, DOWN, buff=0.15)
        den_r = MathTex(r"|f(a)|", font_size=46, color=ORANGE).next_to(
            bar_r, DOWN, buff=0.15)
        cond_note = MathTex(r"f(a) \neq 0", font_size=24,
                            color=GREY_A).move_to([0, -1.75, 0])

        play(
            thm1_eq.animate.shift(lift_vec),
            thm1_tag.animate.shift(lift_vec * 0.8),
            Create(bar_l),
            Create(bar_r),
            FadeIn(den_l, shift=UP * 0.35),
            FadeIn(den_r, shift=UP * 0.35),
            FadeIn(cond_note),
            run_time=2.0,
            rate_func=smooth,
        )

        # Chờ đến đúng cụm "we get Theorem 2, the relative error law." (15.25s)
        wait_until(15.25)

        # Chuẩn bị dòng công thức đầy đủ của Beat 2 + Beat 3 để căn lề chuẩn từng pixel
        full_thm2 = MathTex(
            r"\frac{|\Delta y|}{|f(a)|}",
            r"\approx",
            r"\left|\frac{f'(a)}{f(a)}\right|",
            r"\,|\Delta x|",
            r"=",
            r"\Big|\,d\big(\ln|f(a)|\big)\,\Big|",
            font_size=44,
            color=WHITE,
        ).move_to([0, 0.15, 0])
        full_thm2[0].set_color(TEAL_C)
        full_thm2[2].set_color(YELLOW_C)
        full_thm2[3].set_color(BLUE_B)
        full_thm2[5].set_color(YELLOW_C)

        # Bản gọn ban đầu (chưa mở rộng vế logarit) nằm chính giữa màn hình
        thm2_short = full_thm2[:4].copy().move_to([0, 0.15, 0])

        thm2_tag = Text(
            "THEOREM 2  ·  RELATIVE-ERROR LAW",
            font_size=19, color=YELLOW_C, weight=BOLD
        ).next_to(thm2_short, UP, buff=0.5)

        gold_line = Line(
            thm2_short.get_left() + LEFT * 0.25,
            thm2_short.get_right() + RIGHT * 0.25,
            color=YELLOW_C, stroke_width=2.2, stroke_opacity=0.8
        ).next_to(thm2_short, DOWN, buff=0.35)

        div_src = VGroup(thm1_eq, bar_l, bar_r, den_l, den_r)
        play(
            ReplacementTransform(thm1_tag, thm2_tag),
            ReplacementTransform(div_src, thm2_short),
            Create(gold_line),
            cond_note.animate.next_to(
                gold_line, DOWN, buff=0.35).set_color(GREY_B),
            run_time=2.2,
            rate_func=smooth,
        )

        # =====================================================================
        # BEAT 3 (18.75s – 33.70s): ĐỌC TỪNG VẾ & MỞ RỘNG TRỰC TIẾP SANG LOGARIT
        # "Delta y [over f(a)] is approximately |f'(a)/f(a)| times delta x,
        #  which by the chain rule is just logarithmic differential, |d(ln|f(a)|)|."
        # =====================================================================
        # 18.75s: Nhấn nhẹ vế trái
        wait_until(18.75)
        play(Indicate(thm2_short[0], color=TEAL_C,
             scale_factor=1.12), run_time=1.5)

        # 21.35s: Nhấn nhẹ cụm |f'(a)/f(a)|
        wait_until(21.35)
        play(Indicate(thm2_short[2], color=ORANGE,
             scale_factor=1.15), run_time=2.2)

        # 24.40s: Nhấn nhẹ cụm |Δx|
        wait_until(24.40)
        play(Indicate(thm2_short[3], color=BLUE_B,
             scale_factor=1.18), run_time=1.0)

        # 25.70s: "...which by the chain rule is just" -> Trượt nhẹ công thức sang trái, hiện ngoặc nhọn Chain Rule
        wait_until(25.70)
        chain_brace = Brace(
            full_thm2[2:4], direction=DOWN, buff=0.18, color=BLUE_B)
        chain_lbl = MathTex(
            r"\text{Chain Rule: }\;\big(\ln|f|\big)' = \frac{f'}{f}",
            font_size=24, color=BLUE_B
        ).next_to(chain_brace, DOWN, buff=0.14)

        play(
            FadeOut(gold_line),
            FadeOut(cond_note),
            Transform(thm2_short, full_thm2[:4]),
            thm2_tag.animate.move_to([0, 1.55, 0]),
            GrowFromCenter(chain_brace),
            FadeIn(chain_lbl, shift=UP * 0.1),
            run_time=1.8,
            rate_func=smooth,
        )

        # 28.00s: "logarithmic differential," -> Nối thẳng = |d(ln|f(a)|)| ngay trên cùng 1 dòng!
        wait_until(28.00)
        log_lbl = Text(
            "Logarithmic Differential", font_size=19, color=TEAL_C, weight=BOLD
        ).next_to(full_thm2[5], DOWN, buff=0.45)

        play(
            Write(full_thm2[4]),
            Write(full_thm2[5]),
            FadeIn(log_lbl, shift=UP * 0.1),
            run_time=1.8,
        )

        # 30.30s: "...the absolute value of d of natural log of the absolute value of f of a."
        wait_until(30.30)
        flash_line = Line(
            full_thm2[5].get_left(), full_thm2[5].get_right(),
            color=YELLOW_C, stroke_width=4.5
        ).next_to(full_thm2[5], DOWN, buff=0.12)

        play(
            ShowPassingFlash(flash_line, time_width=0.55),
            Indicate(full_thm2[5], color=YELLOW_A, scale_factor=1.08),
            run_time=2.4,
        )

        wait_until(33.20)
        play(
            FadeOut(VGroup(
                thm2_short, full_thm2[4], full_thm2[5], thm2_tag, chain_brace, chain_lbl, log_lbl)),
            run_time=0.5,
        )

        # =====================================================================
        # BEAT 4 (33.75s – 41.95s): HẠ SỐ MŨ — LŨY THỪA THÀNH TOÁN NHẨM
        # "Why is this so handy? Because it turns power laws into mental math."
        # =====================================================================
        wait_until(33.75)

        handy_q = Text(
            "Why is this so handy?", font_size=36, color=WHITE, weight=BOLD
        ).move_to([0, 0.15, 0])
        q_accent = Line(LEFT * 1.8, RIGHT * 1.8, color=YELLOW_C, stroke_width=2.5).next_to(
            handy_q, DOWN, buff=0.22
        )

        play(FadeIn(handy_q, shift=UP * 0.15), Create(q_accent), run_time=1.2)

        # 36.80s: "Because it turns power laws into mental math."
        wait_until(36.80)

        # Đặt y = C x^n lớn và sạch ngay giữa trái (tách riêng n an toàn không lỗi LaTeX)
        pw_base = MathTex(r"y = ", r"C", r"\,x", font_size=56,
                          color=WHITE).move_to([-3.3, -0.1, 0])
        pw_base[1].set_color(GREY_A)
        pw_base[2].set_color(BLUE_B)
        pw_n = MathTex(r"n", font_size=36, color=YELLOW_C).next_to(
            pw_base[2], UR, buff=0.04).shift(DOWN * 0.12)

        pw_arrow = Arrow([-1.55, -0.1, 0], [-0.15, -0.1, 0],
                         color=TEAL_C, stroke_width=3.5)
        pw_arrow_lbl = MathTex(r"d(\ln|\cdot|)", font_size=22, color=TEAL_C).next_to(
            pw_arrow, UP, buff=0.12)

        play(
            handy_q.animate.scale(0.68).move_to(
                [0, 1.85, 0]).set_color(GREY_A),
            FadeOut(q_accent),
            Write(pw_base),
            Write(pw_n),
            GrowArrow(pw_arrow),
            FadeIn(pw_arrow_lbl),
            run_time=1.4,
        )

        # 38.20s: Hằng số C mờ đi, số mũ n bay vòng cung xuống làm hệ số nhân |n|!
        res_pw = MathTex(
            r"\frac{|\Delta y|}{|y|} \approx",
            r"|n|",
            r"\cdot \frac{|\Delta x|}{|x|}",
            font_size=46, color=WHITE
        ).move_to([2.95, -0.1, 0])
        res_pw[0].set_color(TEAL_C)
        res_pw[1].set_color(YELLOW_C)
        res_pw[2].set_color(BLUE_B)

        pw_caption = Text(
            "Power Laws  →  Instant Mental Math",
            font_size=22, color=GREEN_C, weight=BOLD
        ).move_to([0, -1.95, 0])

        n_fly = pw_n.copy()
        self.add(n_fly)
        play(
            pw_base[1].animate.set_opacity(0.22),
            ReplacementTransform(n_fly, res_pw[1], path_arc=-0.55),
            Write(res_pw[0]),
            Write(res_pw[2]),
            FadeIn(pw_caption, shift=UP * 0.15),
            run_time=2.2,
            rate_func=smooth,
        )

        wait_until(41.20)
        play(
            FadeOut(VGroup(handy_q, pw_base, pw_n, pw_arrow,
                    pw_arrow_lbl, res_pw, pw_caption)),
            run_time=0.75,
        )

        # =====================================================================
        # BEAT 5 (42.05s – 61.18s): VÍ DỤ y = 5x^3 + DẢI THANH NHÂN 3 TỐI GIẢN
        # "Take y = 5x^3, where x has a 1.5% error. Taking logarithms brings the
        #  exponent 3 right down in front, so the relative error in y is simply
        #  3 times 1.5 percent, or 4.5 percent."
        # =====================================================================
        wait_until(42.05)

        # 42.05s: "Take y equals 5 x cubed," -> Chỉ 1 công thức lớn sắc nét ở tâm trên
        ex_base = MathTex(r"y = ", r"5", r"\,x", font_size=58,
                          color=WHITE).move_to([0, 0.95, 0])
        ex_base[1].set_color(GREY_A)
        ex_base[2].set_color(BLUE_B)
        ex_exp3 = MathTex(r"3", font_size=38, color=YELLOW_C).next_to(
            ex_base[2], UR, buff=0.04).shift(DOWN * 0.12)
        ex_group = VGroup(ex_base, ex_exp3)

        play(Write(ex_base), Write(ex_exp3), run_time=1.6)

        # 44.55s: "where x has a 1.5% error." -> Dải thanh đơn mảnh mượt ở nửa dưới
        wait_until(44.55)

        seg_w = 2.05
        bar_y = -1.65
        bar_track = RoundedRectangle(
            width=seg_w * 3 + 0.24, height=0.62, corner_radius=0.1,
            color=SLATE, stroke_width=1.4, stroke_opacity=0.45, fill_opacity=0.0
        ).move_to([0, bar_y, 0])

        seg1 = RoundedRectangle(
            width=seg_w, height=0.52, corner_radius=0.08,
            fill_color=BLUE_C, fill_opacity=0.92, stroke_color=BLUE_B, stroke_width=1.5
        ).move_to([0, bar_y, 0])
        seg1_txt = MathTex(r"1.5\%", font_size=26,
                           color=WHITE).move_to(seg1.get_center())

        bar_label = Text(
            "Input x error", font_size=19, color=BLUE_B, weight=BOLD
        ).next_to(bar_track, UP, buff=0.22)

        play(
            Create(bar_track),
            GrowFromCenter(seg1),
            FadeIn(seg1_txt),
            FadeIn(bar_label, shift=UP * 0.1),
            run_time=1.8,
        )

        # 47.50s: "Taking logarithms brings the exponent 3 right down in front,"
        wait_until(47.50)

        ln_eq = MathTex(
            r"\ln|y| =", r"\ln 5", r"+", r"3", r"\,\ln|x|",
            font_size=46, color=WHITE
        ).move_to([0, 0.35, 0])
        ln_eq[1].set_color(GREY_B)
        ln_eq[3].set_color(YELLOW_C)
        ln_eq[4].set_color(BLUE_B)

        fly_3 = ex_exp3.copy()
        self.add(fly_3)
        play(
            ex_group.animate.scale(0.68).move_to(
                [0, 1.85, 0]).set_opacity(0.55),
            Write(ln_eq[0]),
            Write(ln_eq[1]),
            Write(ln_eq[2]),
            ReplacementTransform(fly_3, ln_eq[3], path_arc=-0.45),
            Write(ln_eq[4]),
            run_time=2.2,
            rate_func=smooth,
        )

        # Gạch bỏ ln 5 gọn gàng (hằng số đạo hàm bằng 0)
        strike_ln5 = Line(
            ln_eq[1].get_corner(DL) + LEFT * 0.05,
            ln_eq[1].get_corner(UR) + RIGHT * 0.05,
            color=RED_C, stroke_width=3.2
        )
        play(
            Create(strike_ln5),
            ln_eq[1].animate.set_opacity(0.25),
            ln_eq[2].animate.set_opacity(0.25),
            Indicate(ln_eq[3], color=YELLOW_C, scale_factor=1.3),
            run_time=1.1,
        )

        # 51.85s: "so the relative error in" -> Gọn sạch thành 1 dòng kết quả duy nhất ở tâm trên
        wait_until(51.85)

        final_eq = MathTex(
            r"\frac{|\Delta y|}{|y|} \approx",
            r"3 \times",
            r"1.5\%",
            r"= 4.5\%",
            font_size=50,
            color=WHITE,
        ).move_to([0, 0.65, 0])
        final_eq[0].set_color(TEAL_C)
        final_eq[1].set_color(YELLOW_C)
        final_eq[2].set_color(BLUE_B)
        final_eq[3].set_color(GREEN_C)

        bar_label_y = Text(
            "Output y error  (3×)", font_size=19, color=YELLOW_C, weight=BOLD
        ).next_to(bar_track, UP, buff=0.22)

        play(
            FadeOut(VGroup(ex_group, ln_eq, strike_ln5)),
            Write(final_eq[0]),
            Transform(bar_label, bar_label_y),
            run_time=1.6,
        )

        # 54.15s: "y is simply 3 times" -> Thanh 1.5% tách mượt thành 3 đốt bằng nhau!
        wait_until(54.15)

        seg2 = seg1.copy()
        seg3 = seg1.copy()
        self.add(seg2, seg3)

        p1 = [-seg_w - 0.06, bar_y, 0]
        p2 = [0.0, bar_y, 0]
        p3 = [seg_w + 0.06, bar_y, 0]

        play(
            Write(final_eq[1]),
            FadeOut(seg1_txt),
            seg1.animate.move_to(p1).set_fill(
                TEAL_C, opacity=0.92).set_stroke(TEAL_B),
            seg2.animate.move_to(p2).set_fill(
                TEAL_C, opacity=0.92).set_stroke(TEAL_B),
            seg3.animate.move_to(p3).set_fill(
                TEAL_C, opacity=0.92).set_stroke(TEAL_B),
            run_time=1.5,
            rate_func=smooth,
        )

        # 56.15s: "1.5 percent," -> Hiện đồng loạt nhãn 1.5% trên cả 3 đốt
        wait_until(56.15)
        t1 = MathTex(r"1.5\%", font_size=24, color=WHITE).move_to(p1)
        t2 = MathTex(r"1.5\%", font_size=24, color=WHITE).move_to(p2)
        t3 = MathTex(r"1.5\%", font_size=24, color=WHITE).move_to(p3)

        play(
            Write(final_eq[2]),
            LaggedStart(FadeIn(t1), FadeIn(t2), FadeIn(t3), lag_ratio=0.25),
            run_time=1.2,
        )

        # 57.75s: "or 4.5 percent." -> Hợp nhất 3 đốt thành 1 dải ngọc lục bảo 4.5% phát sáng!
        wait_until(57.75)
        merged_bar = RoundedRectangle(
            width=seg_w * 3 + 0.12, height=0.58, corner_radius=0.1,
            fill_color=GREEN_C, fill_opacity=0.95, stroke_color=YELLOW_C, stroke_width=2.2
        ).move_to([0, bar_y, 0])
        merged_lbl = MathTex(
            r"4.5\%\;\text{ Relative Error}", font_size=27, color="#0F172A"
        ).move_to(merged_bar.get_center())

        play(
            Write(final_eq[3]),
            ReplacementTransform(
                VGroup(seg1, seg2, seg3, t1, t2, t3), merged_bar),
            FadeIn(merged_lbl),
            run_time=1.8,
            rate_func=smooth,
        )

        # Quét 1 tia sáng vàng tinh tế dưới kết quả 4.5%
        res_flash = Line(
            final_eq[3].get_left(), final_eq[3].get_right(),
            color=YELLOW_C, stroke_width=4.5
        ).next_to(final_eq[3], DOWN, buff=0.14)
        play(ShowPassingFlash(res_flash, time_width=0.5), run_time=0.9)

        # Chốt chuẩn cuối file audio (61.18s)
        wait_until(61.18)
