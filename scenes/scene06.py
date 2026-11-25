from manim import *
import numpy as np


class Scene06(Scene):
    def construct(self):
        # Bảng màu tối giản đồng bộ toàn bộ dự án
        self.camera.background_color = "#0F172A"
        SLATE = "#64748B"
        WOOD_FILL = "#92400E"
        WOOD_RING = "#B45309"
        WOOD_STROKE = "#F59E0B"

        # Tự động ghép file tiếng khi render nháp (thêm dấu # khi render final không tiếng)
        self.add_sound("Recordings/Scene6.wav")

        # Bộ đếm thời gian khóa cứng từng mốc giây (audio 108.96s + 1.2s giữ hình cuối = 110.20s)
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
            "Case 1: The Circular Tabletop",
            font_size=25,
            color=YELLOW_C,
            weight=BOLD,
        ).to_edge(UP, buff=0.38).shift(RIGHT * 1.2)

        # =====================================================================
        # BEAT 1 (0.00s – 14.80s): CHỌN 2/3 CASE STUDY -> CASE 1: MẶT BÀN TRÒN
        # "To put this 5% rule into the test, we have selected two representative
        #  scenarios from the three case studies in our report. We'll kick things
        #  off with our first real-world problem, a circular tabletop."
        # =====================================================================
        intro_hdr = Text(
            "PUTTING THE 5% RULE TO THE TEST",
            font_size=26, color=WHITE, weight=BOLD
        ).move_to([0, 1.55, 0])
        intro_rule = Line(LEFT * 3.2, RIGHT * 3.2, color=YELLOW_C, stroke_width=2.2, stroke_opacity=0.75).next_to(
            intro_hdr, DOWN, buff=0.18
        )

        play(
            FadeIn(sec_title, shift=DOWN * 0.15),
            FadeIn(intro_hdr, shift=UP * 0.12),
            Create(intro_rule),
            run_time=1.2,
        )

        # 2.50s: Hiện 3 nhánh case study tối giản (không dùng khung vuông nặng)
        wait_until(2.50)

        def make_case_node(num, title, subtitle, color, x_pos):
            circ = Circle(radius=0.34, color=color, stroke_width=3.0)
            num_t = Text(num, font_size=24, color=color,
                         weight=BOLD).move_to(circ.get_center())
            t_lbl = Text(title, font_size=21, color=WHITE,
                         weight=BOLD).next_to(circ, DOWN, buff=0.25)
            s_lbl = Text(subtitle, font_size=16, color=GREY_B).next_to(
                t_lbl, DOWN, buff=0.1)
            return VGroup(circ, num_t, t_lbl, s_lbl).move_to([x_pos, -0.45, 0])

        c1_node = make_case_node(
            "1", "Circular Tabletop", "Area & Profit", YELLOW_C, -4.1)
        c2_node = make_case_node(
            "2", "Tree Height", "Clinometer Angle", TEAL_C, 0.0)
        c3_node = make_case_node(
            "3", "Cliff Drop", "Free-Fall Timing", GREY_B, 4.1)

        play(
            LaggedStart(
                FadeIn(c1_node, shift=UP * 0.2),
                FadeIn(c2_node, shift=UP * 0.2),
                FadeIn(c3_node, shift=UP * 0.2),
                lag_ratio=0.25,
            ),
            run_time=2.2,
        )

        # 5.50s: Chọn 2 kịch bản tiêu biểu (làm mờ Case 3)
        wait_until(5.50)
        c3_tag = Text("(in report)", font_size=15, color=GREY_C).next_to(
            c3_node, DOWN, buff=0.14)
        play(
            c3_node.animate.set_opacity(0.28),
            FadeIn(c3_tag),
            Indicate(c1_node[0], color=YELLOW_A, scale_factor=1.12),
            Indicate(c2_node[0], color=TEAL_B, scale_factor=1.12),
            run_time=1.8,
        )

        # 9.85s: Tập trung vào Case 1 — Circular Tabletop
        wait_until(9.85)
        focus_ring = Circle(radius=0.46, color=YELLOW_C, stroke_width=2.0, stroke_opacity=0.65).move_to(
            c1_node[0].get_center()
        )
        play(
            c2_node.animate.set_opacity(0.25),
            c3_node.animate.set_opacity(0.12),
            c3_tag.animate.set_opacity(0.12),
            c1_node.animate.scale(1.12),
            Create(focus_ring),
            run_time=2.5,
            rate_func=smooth,
        )

        # 13.00s: "a circular tabletop." -> Chuyển mượt sang mặt bàn thật
        wait_until(13.00)
        play(
            Indicate(c1_node[2], color=YELLOW_C, scale_factor=1.12),
            run_time=0.9,
        )
        play(
            FadeOut(VGroup(intro_hdr, intro_rule, c1_node,
                    c2_node, c3_node, c3_tag, focus_ring)),
            run_time=0.9,
        )

        # =====================================================================
        # BEAT 2 (15.15s – 39.05s): MẶT BÀN GỖ 60 CM & CÚ GỌT LÉN 1 CM
        # "A wood workshop builds a circular tabletop with a radius of 60 centimeters.
        #  At 50 dong per square centimeter, the customer pays 565,200 dong.
        #  Now, suppose a sneaky artisan secretly trims 1 centimeter off the radius
        #  while keeping the full payment. How much extra profit does he think he makes?"
        # =====================================================================
        wait_until(15.15)

        table_c = np.array([-3.0, -0.4, 0])
        outer_R = 2.15
        inner_R = 1.90  # Phóng nhẹ bề rộng vành khăn để nhìn rõ 1 cm

        inner_disc = Circle(
            radius=inner_R,
            fill_color=WOOD_FILL,
            fill_opacity=0.92,
            stroke_color=WOOD_STROKE,
            stroke_width=1.8,
        ).move_to(table_c)

        # Vân gỗ đồng tâm tinh tế tạo cảm giác mặt bàn thật
        wood_grains = VGroup(
            Circle(radius=0.55, color=WOOD_RING, stroke_width=1.2,
                   stroke_opacity=0.45).move_to(table_c),
            Circle(radius=1.12, color=WOOD_RING, stroke_width=1.2,
                   stroke_opacity=0.40).move_to(table_c),
            Circle(radius=1.58, color=WOOD_RING, stroke_width=1.2,
                   stroke_opacity=0.35).move_to(table_c),
        )

        shaved_ring = Annulus(
            inner_radius=inner_R,
            outer_radius=outer_R,
            fill_color=WOOD_FILL,
            fill_opacity=0.92,
            stroke_color=WOOD_STROKE,
            stroke_width=2.0,
        ).move_to(table_c)

        r_arrow = Arrow(
            table_c, table_c + RIGHT * outer_R, buff=0,
            color=WHITE, stroke_width=3.0, max_tip_length_to_length_ratio=0.11
        )
        r_lbl = MathTex(r"r = 60\text{ cm}", font_size=28, color=WHITE).next_to(
            r_arrow, UP, buff=0.14
        )

        play(
            GrowFromCenter(inner_disc),
            FadeIn(wood_grains),
            FadeIn(shaved_ring),
            GrowArrow(r_arrow),
            Write(r_lbl),
            run_time=2.6,
            rate_func=smooth,
        )

        # 20.55s: "At 50 dong per square centimeter,"
        wait_until(20.55)
        # Căn lề trái gọn gàng cho cột thông số bên phải (không khung vuông)
        col_x = 1.15

        spec_hdr = Text("WORKSHOP ORDER", font_size=17, color=TEAL_C, weight=BOLD).move_to(
            [col_x, 1.55, 0], aligned_edge=LEFT
        )
        spec_rate = MathTex(
            r"\text{Rate} = 50\text{ dong/cm}^2", font_size=30, color=GREY_A
        ).move_to([col_x, 0.95, 0], aligned_edge=LEFT)

        play(FadeIn(spec_hdr, shift=DOWN * 0.1), Write(spec_rate), run_time=1.6)

        # 23.10s: "the customer pays 565,200 dong."
        wait_until(23.10)
        spec_pay = MathTex(
            r"\text{Payment} = 565{,}200\text{ dong}", font_size=33, color=GREEN_C
        ).move_to([col_x, 0.2, 0], aligned_edge=LEFT)
        spec_area_note = MathTex(
            r"\big(A = \pi \cdot 60^2 \approx 11{,}304\text{ cm}^2\big)",
            font_size=20, color=GREY_B
        ).move_to([col_x, -0.32, 0], aligned_edge=LEFT)

        play(Write(spec_pay), FadeIn(spec_area_note, shift=UP * 0.08), run_time=2.0)

        # 26.65s: "Now, suppose a sneaky artisan"
        wait_until(26.65)
        trim_divider = Line([col_x, -0.82, 0], [col_x + 4.7, -0.82, 0],
                            color=SLATE, stroke_width=1.2, stroke_opacity=0.45)
        trim_lbl = MathTex(
            r"\text{Secret Trim: }\;\Delta r = 1\text{ cm}", font_size=30, color=RED_B
        ).move_to([col_x, -1.3, 0], aligned_edge=LEFT)

        play(Create(trim_divider), FadeIn(
            trim_lbl, shift=RIGHT * 0.15), run_time=1.5)

        # 29.20s: "secretly trims 1 centimeter off the radius" -> Tia cắt đỏ quét 360° quanh vành!
        wait_until(29.20)
        cut_arc = Circle(radius=inner_R, color=RED_C,
                         stroke_width=4.5).move_to(table_c)
        dr_seg = Line(
            table_c + RIGHT * inner_R, table_c + RIGHT * outer_R,
            color=RED_C, stroke_width=6
        )
        dr_tag = MathTex(r"\Delta r", font_size=23, color=RED_B).next_to(
            dr_seg, DOWN, buff=0.14)

        play(
            Create(cut_arc),
            shaved_ring.animate.set_fill(
                RED_C, opacity=0.78).set_stroke(RED_B, width=2.2),
            FadeIn(dr_seg),
            FadeIn(dr_tag),
            run_time=2.5,
            rate_func=smooth,
        )

        # 32.40s: "while keeping the full payment." -> Nhấn sáng khoản tiền giữ nguyên
        wait_until(32.40)
        play(Indicate(spec_pay, color=YELLOW_C, scale_factor=1.08), run_time=1.2)

        # 35.00s: "How much extra profit does he think he makes?"
        wait_until(35.00)
        profit_q = Text(
            "Extra Profit = ?", font_size=34, color=YELLOW_C, weight=BOLD
        ).move_to([col_x, -2.18, 0], aligned_edge=LEFT)
        profit_line = Line(
            profit_q.get_left(), profit_q.get_right(), color=YELLOW_C, stroke_width=2.5
        ).next_to(profit_q, DOWN, buff=0.12)

        play(Write(profit_q), Create(profit_line), run_time=1.8)

        # 38.10s: Chuẩn bị cho hiệu ứng trải phẳng vành khăn ngay giữa màn hình
        wait_until(38.10)
        L_bar = 7.4
        R_unroll = L_bar / (2.0 * np.pi)  # ~1.178
        h_bar = 0.34
        unroll_u = ValueTracker(0.0)

        def build_unroll_ribbon():
            u = unroll_u.get_value()
            # Từ -0.65 (dạng vòng) nâng mượt lên +0.95 (dải phẳng)
            y0 = -0.65 + 1.60 * u
            kappa = (1.0 - u) / R_unroll
            n_pts = 84
            s = np.linspace(-L_bar / 2.0, L_bar / 2.0, n_pts)
            if kappa > 1e-4:
                rad = 1.0 / kappa
                th = s * kappa
                x_out = rad * np.sin(th)
                y_out = y0 + rad * (1.0 - np.cos(th))
                x_in = (rad - h_bar) * np.sin(th)
                y_in = y0 + rad - (rad - h_bar) * np.cos(th)
            else:
                x_out = s
                y_out = np.full_like(s, y0)
                x_in = s
                y_in = np.full_like(s, y0 + h_bar)

            pts_out = [np.array([x_out[i], y_out[i], 0.0])
                       for i in range(n_pts)]
            pts_in = [np.array([x_in[i], y_in[i], 0.0])
                      for i in range(n_pts - 1, -1, -1)]
            col = interpolate_color(RED_C, YELLOW_C, u)
            return Polygon(
                *(pts_out + pts_in),
                fill_color=col,
                fill_opacity=0.88,
                stroke_color=WHITE,
                stroke_width=1.6,
            )

        # Đưa vành khăn đỏ từ mặt bàn về đúng vị trí vòng khởi đầu ở chính giữa
        ring_start_pos = np.array([0.0, -0.65 + R_unroll, 0.0])
        ring_init_proxy = Annulus(
            inner_radius=R_unroll - h_bar,
            outer_radius=R_unroll,
            fill_color=RED_C,
            fill_opacity=0.88,
            stroke_color=WHITE,
            stroke_width=1.6,
        ).move_to(ring_start_pos)

        beat2_clear = VGroup(
            inner_disc, wood_grains, r_arrow, r_lbl, cut_arc, dr_seg, dr_tag,
            spec_hdr, spec_rate, spec_pay, spec_area_note, trim_divider, trim_lbl,
            profit_q, profit_line,
        )
        play(
            FadeOut(beat2_clear),
            ReplacementTransform(shaved_ring, ring_init_proxy),
            run_time=0.95,
            rate_func=smooth,
        )

        # =====================================================================
        # BEAT 3 (39.10s – 62.80s): TRẢI PHẲNG VÀNH KHĂN THẬT -> dA = 2πr Δr
        # "If we unroll that shaved outer ring, it looks almost like a thin rectangle
        #  of length 2 pi r and width delta r. So our differential estimate for the
        #  lost area is dA equals 2 pi r delta r, which comes out to 376.8 square
        #  centimeters, or 18,840 dong."
        # =====================================================================
        wait_until(39.10)

        dyn_ribbon = always_redraw(build_unroll_ribbon)
        self.remove(ring_init_proxy)
        self.add(dyn_ribbon)

        # Trải phẳng thực sự bằng biến đổi độ cong κ: 1/R -> 0!
        play(unroll_u.animate.set_value(1.0), run_time=3.8, rate_func=smooth)

        # Cố định dải hình chữ nhật phẳng ở y in [0.95, 1.29]
        self.remove(dyn_ribbon)
        flat_rect = Rectangle(
            width=L_bar, height=h_bar,
            fill_color=YELLOW_C, fill_opacity=0.88,
            stroke_color=WHITE, stroke_width=1.6,
        ).move_to([0.0, 0.95 + h_bar / 2.0, 0.0])
        self.add(flat_rect)

        # 43.85s: "of length 2 pi r"
        wait_until(43.85)
        brace_len = Brace(flat_rect, direction=UP, buff=0.12, color=WHITE)
        lbl_len = MathTex(r"2\pi r", font_size=30, color=WHITE).next_to(
            brace_len, UP, buff=0.1)
        play(GrowFromCenter(brace_len), Write(lbl_len), run_time=1.35)

        # 45.60s: "and width delta r."
        wait_until(45.60)
        brace_wid = Brace(flat_rect, direction=RIGHT, buff=0.12, color=RED_B)
        lbl_wid = MathTex(r"\Delta r", font_size=28, color=RED_B).next_to(
            brace_wid, RIGHT, buff=0.12)
        play(GrowFromCenter(brace_wid), Write(lbl_wid), run_time=1.05)

        # 46.95s: "So our differential estimate for the lost area"
        wait_until(46.95)
        diff_tag = Text(
            "DIFFERENTIAL ESTIMATE", font_size=18, color=YELLOW_C, weight=BOLD
        ).move_to([0, 0.15, 0])
        play(FadeIn(diff_tag, shift=DOWN * 0.1), run_time=1.2)

        # 50.65s: "is dA equals 2 pi r delta r,"
        wait_until(50.65)
        eq_da = MathTex(r"dA = 2\pi r\,\Delta r", font_size=50,
                        color=WHITE).move_to([0, -0.58, 0])
        play(Write(eq_da), run_time=2.0)

        # 53.20s: "which comes out to 376.8 square centimeters"
        wait_until(53.20)
        val_da_cm = MathTex(
            r"= 376.8\text{ cm}^2", font_size=40, color=YELLOW_B).move_to([-1.85, -1.55, 0])
        play(Write(val_da_cm), run_time=2.2)

        # 58.65s: "or 18,840 dong."
        wait_until(58.65)
        val_da_money = MathTex(
            r"\approx 18{,}840\text{ dong}", font_size=40, color=YELLOW_C).move_to([2.05, -1.55, 0])
        money_flash = Line(
            val_da_money.get_left(), val_da_money.get_right(),
            color=YELLOW_C, stroke_width=4
        ).next_to(val_da_money, DOWN, buff=0.12)
        play(Write(val_da_money), ShowPassingFlash(
            money_flash, time_width=0.55), run_time=2.2)

        # 61.80s: Đẩy dải chữ nhật lên gọn trên cùng, dịch cột ước lượng sang trái để so sánh
        wait_until(61.80)
        bar_bundle = VGroup(flat_rect, brace_len, lbl_len, brace_wid, lbl_wid)

        left_x = -3.15
        right_x = 3.15
        left_tag_new = Text("DIFFERENTIAL ESTIMATE", font_size=18,
                            color=YELLOW_C, weight=BOLD).move_to([left_x, 0.45, 0])
        left_eq_new = MathTex(r"dA = 2\pi r\,\Delta r", font_size=30,
                              color=GREY_A).move_to([left_x, -0.15, 0])
        left_cm_new = MathTex(
            r"376.80\text{ cm}^2", font_size=34, color=YELLOW_B).move_to([left_x, -0.82, 0])
        left_dong_new = MathTex(
            r"18{,}840\text{ dong}", font_size=36, color=YELLOW_C).move_to([left_x, -1.52, 0])

        play(
            bar_bundle.animate.scale(0.86).move_to([0, 1.8, 0]),
            Transform(diff_tag, left_tag_new),
            Transform(eq_da, left_eq_new),
            Transform(val_da_cm, left_cm_new),
            Transform(val_da_money, left_dong_new),
            run_time=1.0,
            rate_func=smooth,
        )

        # =====================================================================
        # BEAT 4 (62.90s – 87.75s): HÌNH HỌC CHÍNH XÁC & MẢNH DƯ ĐỎ π(Δr)²
        # "Let's check that against the exact geometry. The true area lost is
        #  373.66 square centimeters, worth 18,683 dong. Our quick tangent-line
        #  estimate is off by only 157 dong, less than 1%. That tiny difference
        #  is just the red sliver pi times delta r squared."
        # =====================================================================
        wait_until(62.90)

        mid_div = Line([0, 0.7, 0], [0, -1.85, 0], color=SLATE,
                       stroke_width=1.4, stroke_opacity=0.45)
        right_tag = Text("EXACT GEOMETRY", font_size=18,
                         color=TEAL_C, weight=BOLD).move_to([right_x, 0.45, 0])
        right_eq = MathTex(r"\Delta A = \pi r^2 - \pi(r-\Delta r)^2",
                           font_size=28, color=GREY_A).move_to([right_x, -0.15, 0])

        play(Create(mid_div), FadeIn(right_tag, shift=DOWN * 0.1),
             Write(right_eq), run_time=2.4)

        # 66.35s: "The true area lost is 373.66 square centimeters,"
        wait_until(66.35)
        right_cm = MathTex(r"373.66\text{ cm}^2", font_size=34, color=TEAL_B).move_to(
            [right_x, -0.82, 0])
        play(Write(right_cm), run_time=2.2)

        # 71.70s: "worth 18,683 dong."
        wait_until(71.70)
        right_dong = MathTex(r"18{,}683\text{ dong}", font_size=36, color=TEAL_C).move_to(
            [right_x, -1.52, 0])
        play(Write(right_dong), run_time=1.9)

        # 75.85s: "Our quick tangent-line estimate is off by only 157 dong,"
        wait_until(75.85)
        bot_rule = Line([-4.6, -2.1, 0], [4.6, -2.1, 0],
                        color=SLATE, stroke_width=1.2, stroke_opacity=0.4)
        gap_eq = MathTex(
            r"\text{Difference} = 157\text{ dong}", font_size=34, color=RED_B
        ).move_to([-1.25, -2.68, 0])
        play(Create(bot_rule), Write(gap_eq), run_time=2.2)

        # 80.95s: "less than 1%."
        wait_until(80.95)
        lt1_lbl = MathTex(r"(< 1\%!)", font_size=34, color=GREEN_C).next_to(
            gap_eq, RIGHT, buff=0.35)
        play(Write(lt1_lbl), Indicate(
            lt1_lbl, color=YELLOW_C, scale_factor=1.18), run_time=1.2)

        # 82.50s: "That tiny difference is just the red sliver pi times delta r squared."
        # Tách đúng mảnh tam giác vuông đỏ ở mép phải dải chữ nhật (hình thang thật ở bên trong!)
        wait_until(82.50)

        rect_top_r = flat_rect.get_corner(UR)
        rect_bot_r = flat_rect.get_corner(DR)
        rect_top_l = flat_rect.get_corner(UL)
        rect_bot_l = flat_rect.get_corner(DL)
        sliver_w = 0.72  # Đủ rộng để nhìn rõ tam giác dư π(Δr)² ở mép phải

        # Hình thang xanh ngọc = diện tích thực ΔA = ½(2πr + 2π(r-Δr))·Δr = 2πrΔr - π(Δr)²
        true_trap = Polygon(
            rect_bot_l,
            rect_bot_r,
            rect_top_r + LEFT * sliver_w,
            rect_top_l,
            fill_color=TEAL_C,
            fill_opacity=0.88,
            stroke_color=WHITE,
            stroke_width=1.5,
        )
        # Mảnh tam giác đỏ = phần chênh lệch chính xác π(Δr)²!
        red_sliver = Polygon(
            rect_bot_r,
            rect_top_r,
            rect_top_r + LEFT * sliver_w,
            fill_color=RED_C,
            fill_opacity=0.98,
            stroke_color=WHITE,
            stroke_width=1.8,
        )
        sliver_arrow = Arrow(
            rect_bot_r + DOWN * 0.65 + RIGHT * 0.45,
            red_sliver.get_center() + DOWN * 0.08 + RIGHT * 0.08,
            buff=0, color=RED_C, stroke_width=2.8, max_tip_length_to_length_ratio=0.3
        )
        sliver_tex = MathTex(
            r"\pi(\Delta r)^2", font_size=28, color=RED_B
        ).next_to(sliver_arrow.get_start(), RIGHT, buff=0.12)

        play(
            FadeIn(true_trap),
            FadeIn(red_sliver, scale=1.2),
            GrowArrow(sliver_arrow),
            Write(sliver_tex),
            run_time=2.2,
            rate_func=smooth,
        )
        play(Indicate(red_sliver, color=YELLOW_C, scale_factor=1.22), run_time=1.0)

        wait_until(87.00)
        beat4_all = VGroup(
            bar_bundle, diff_tag, eq_da, val_da_cm, val_da_money,
            mid_div, right_tag, right_eq, right_cm, right_dong,
            bot_rule, gap_eq, lt1_lbl, true_trap, red_sliver, sliver_arrow, sliver_tex,
        )
        play(FadeOut(beat4_all), run_time=0.75)

        # =====================================================================
        # BEAT 5 (87.85s – 110.20s): GIỚI HẠN 5% -> Δr ≈ 5.71 CM
        # "Now, how much could he trim before our linear formula breaks down?
        #  Setting the relative discrepancy delta r over 2r minus delta r equal
        #  to 5% tells us the limit is delta r is approximately 5.71 centimeters.
        #  Anywhere up to there, the linear estimate is rock solid."
        # =====================================================================
        wait_until(87.85)

        dr_t = ValueTracker(1.0)
        sim_c = np.array([-3.75, -0.4, 0.0])
        sim_R = 2.05

        # Mặt bàn động bên trái: vành gọt dày dần khi Δr tăng từ 1.00 lên 5.71 cm
        dyn_disc = always_redraw(
            lambda: Circle(
                radius=max(sim_R * (1.0 - dr_t.get_value() / 19.0), 0.65),
                fill_color=WOOD_FILL,
                fill_opacity=0.92,
                stroke_color=WOOD_STROKE,
                stroke_width=1.8,
            ).move_to(sim_c)
        )
        dyn_ring = always_redraw(
            lambda: Annulus(
                inner_radius=max(
                    sim_R * (1.0 - dr_t.get_value() / 19.0), 0.65),
                outer_radius=sim_R,
                fill_color=RED_C if dr_t.get_value() >= 5.70 else ORANGE,
                fill_opacity=0.82,
                stroke_color=WHITE,
                stroke_width=1.6,
            ).move_to(sim_c)
        )
        dyn_dr_caption = always_redraw(
            lambda: MathTex(
                rf"\Delta r = {dr_t.get_value():.2f}\text{{ cm}}",
                font_size=30,
                color=RED_B if dr_t.get_value() >= 5.70 else YELLOW_C,
            ).move_to([sim_c[0], sim_c[1] - sim_R - 0.48, 0])
        )

        # Cột phân tích tối giản bên phải
        rx_c = 2.55
        lim_hdr = Text(
            "5% BREAKDOWN LIMIT", font_size=21, color=YELLOW_C, weight=BOLD
        ).move_to([rx_c, 1.85, 0])
        lim_rule = Line(
            [rx_c - 2.4, 1.55, 0], [rx_c + 2.4, 1.55, 0],
            color=YELLOW_C, stroke_width=1.8, stroke_opacity=0.65
        )

        play(
            FadeIn(dyn_disc),
            FadeIn(dyn_ring),
            FadeIn(dyn_dr_caption),
            FadeIn(lim_hdr, shift=DOWN * 0.12),
            Create(lim_rule),
            run_time=2.4,
        )

        # 92.20s: "Setting the relative discrepancy delta r over 2r minus delta r"
        wait_until(92.20)
        eq_disc = MathTex(
            r"\frac{\Delta r}{2r - \Delta r}",
            r"=\; 5\%",
            font_size=44,
            color=WHITE,
        ).move_to([rx_c, 0.72, 0])
        eq_disc[1].set_color(YELLOW_C)

        play(Write(eq_disc[0]), run_time=2.8)

        # 96.75s: "equal to 5%" -> Hiện = 5% và thanh dung sai đồng bộ phong cách Scene 5!
        wait_until(96.75)

        b_w = 5.4
        b_y = -0.68
        b_left = rx_c - b_w / 2.0
        # Thang đo từ 0% đến 8% -> vạch 5% nằm tại 5/8 chiều dài
        green_w = b_w * (5.0 / 8.0)
        red_w = b_w * (3.0 / 8.0)
        x_5 = b_left + green_w

        g_zone = RoundedRectangle(
            width=green_w, height=0.22, corner_radius=0.06,
            fill_color=GREEN_C, fill_opacity=0.85, stroke_width=0
        ).move_to([b_left + green_w / 2.0, b_y, 0])

        r_zone = RoundedRectangle(
            width=red_w, height=0.22, corner_radius=0.06,
            fill_color=RED_C, fill_opacity=0.35, stroke_width=0
        ).move_to([x_5 + red_w / 2.0, b_y, 0])

        m_5 = Line([x_5, b_y - 0.34, 0], [x_5, b_y + 0.36, 0],
                   color=YELLOW_C, stroke_width=3.0)
        m_5_lbl = MathTex(r"5\%", font_size=22, color=YELLOW_C).next_to(
            m_5, UP, buff=0.08)

        def get_pct():
            d = dr_t.get_value()
            return (d / (120.0 - d)) * 100.0

        dyn_marker = always_redraw(
            lambda: VGroup(
                Dot(
                    [b_left + b_w * min(get_pct() / 8.0, 1.0), b_y, 0],
                    color=RED_C if get_pct() >= 4.99 else GREEN_C,
                    radius=0.11,
                ),
                MathTex(
                    rf"{get_pct():.2f}\%",
                    font_size=22,
                    color=RED_B if get_pct() >= 4.99 else GREEN_C,
                ).move_to([b_left + b_w * min(get_pct() / 8.0, 1.0), b_y - 0.42, 0]),
            )
        )

        play(
            Write(eq_disc[1]),
            FadeIn(VGroup(g_zone, r_zone, m_5, m_5_lbl,
                   dyn_marker), shift=UP * 0.12),
            run_time=1.5,
        )

        # 98.50s: "tells us the limit is delta r is approximately 5.71 centimeters."
        wait_until(98.50)
        play(dr_t.animate.set_value(5.714), run_time=3.8, rate_func=smooth)

        # 102.35s: "5.71 centimeters."
        wait_until(102.35)
        lim_ans = MathTex(
            r"\text{Limit: }\;\Delta r \approx 5.71\text{ cm}",
            font_size=38, color=YELLOW_C
        ).move_to([rx_c, -1.88, 0])
        play(Write(lim_ans), run_time=1.5)

        # 104.45s: "Anywhere up to there, the linear estimate is rock solid."
        wait_until(104.45)
        rock_tag = Text(
            "0 < Δr ≤ 5.71 cm  ·  ROCK SOLID",
            font_size=19, color=GREEN_C, weight=BOLD
        ).move_to([rx_c, -2.55, 0])
        ans_flash = Line(
            lim_ans.get_left(), lim_ans.get_right(), color=GREEN_C, stroke_width=4.2
        ).next_to(lim_ans, DOWN, buff=0.12)

        play(
            Indicate(g_zone, color=GREEN_B, scale_factor=1.06),
            FadeIn(rock_tag, shift=UP * 0.1),
            ShowPassingFlash(ans_flash, time_width=0.55),
            run_time=2.4,
        )

        # Giữ hình thêm ~1.2s cuối để người xem kịp đọc trọn kết luận
        wait_until(110.20)
