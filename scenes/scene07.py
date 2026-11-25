from manim import *
import numpy as np


class Scene07(Scene):
    def construct(self):
        # Bảng màu tối giản đồng bộ toàn bộ dự án
        self.camera.background_color = "#0F172A"
        SLATE = "#64748B"
        TRUNK_COL = "#92400E"
        LEAF_DARK = "#15803D"
        LEAF_LIGHT = "#22C55E"

        # Tự động ghép file tiếng khi render nháp (thêm dấu # khi render final không tiếng)
        self.add_sound("Recordings/Scene7.wav")

        # Bộ đếm thời gian khóa cứng từng mốc giây (audio 109.87s + ~1.3s giữ hình cuối = 111.20s)
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

        # Hàm dựng cây thông cách điệu gọn đẹp (đỉnh đúng tại y_ground + height)
        def make_tree(x_base, y_ground, height):
            trunk_h = height * 0.24
            trunk_w = height * 0.065
            trunk = Rectangle(
                width=trunk_w, height=trunk_h,
                fill_color=TRUNK_COL, fill_opacity=0.95, stroke_width=0
            ).move_to([x_base, y_ground + trunk_h / 2.0, 0])

            # 3 tầng tán tam giác xếp chồng sắc nét, đỉnh cao nhất khớp chính xác y_ground + height
            t1_bot = y_ground + trunk_h * 0.72
            t1_top = y_ground + height * 0.56
            t1 = Polygon(
                [x_base - height * 0.23, t1_bot, 0],
                [x_base + height * 0.23, t1_bot, 0],
                [x_base, t1_top, 0],
                fill_color=LEAF_DARK, fill_opacity=0.95, stroke_color=LEAF_LIGHT, stroke_width=1.0
            )
            t2_bot = y_ground + height * 0.36
            t2_top = y_ground + height * 0.79
            t2 = Polygon(
                [x_base - height * 0.18, t2_bot, 0],
                [x_base + height * 0.18, t2_bot, 0],
                [x_base, t2_top, 0],
                fill_color="#16A34A", fill_opacity=0.95, stroke_color=LEAF_LIGHT, stroke_width=1.0
            )
            t3_bot = y_ground + height * 0.60
            t3_top = y_ground + height
            t3 = Polygon(
                [x_base - height * 0.13, t3_bot, 0],
                [x_base + height * 0.13, t3_bot, 0],
                [x_base, t3_top, 0],
                fill_color=LEAF_LIGHT, fill_opacity=0.95, stroke_color="#86EFAC", stroke_width=1.0
            )
            return VGroup(trunk, t1, t2, t3)

        # Hàm dựng người kiểm lâm tối giản (tầm mắt tại y_ground + eye_h)
        def make_forester(x_pos, y_ground, eye_h):
            head_r = eye_h * 0.15
            head_c = np.array([x_pos, y_ground + eye_h, 0])
            head = Circle(
                radius=head_r, fill_color=WHITE, fill_opacity=0.95, stroke_width=0
            ).move_to(head_c)
            body = Line(
                [x_pos, y_ground + eye_h - head_r, 0],
                [x_pos, y_ground + eye_h * 0.38, 0],
                color=WHITE, stroke_width=3.2
            )
            leg_l = Line(
                [x_pos, y_ground + eye_h * 0.38, 0],
                [x_pos - head_r * 0.9, y_ground, 0],
                color=WHITE, stroke_width=2.8
            )
            leg_r = Line(
                [x_pos, y_ground + eye_h * 0.38, 0],
                [x_pos + head_r * 0.9, y_ground, 0],
                color=WHITE, stroke_width=2.8
            )
            arm = Line(
                [x_pos, y_ground + eye_h * 0.76, 0],
                [x_pos - head_r * 1.45, y_ground + eye_h * 0.96, 0],
                color=YELLOW_C, stroke_width=2.6
            )
            return VGroup(leg_l, leg_r, body, arm, head)

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
            "Case 2: Measuring a Tall Tree",
            font_size=25,
            color=YELLOW_C,
            weight=BOLD,
        ).to_edge(UP, buff=0.38).shift(RIGHT * 1.2)

        # =====================================================================
        # BEAT 1 (0.00s – 25.65s): BÀI TOÁN ĐO CHIỀU CAO CÂY KHÔNG CẦN TRÈO
        # "Our second case asks a classic field question: how do you measure a
        #  tall tree without climbing it? A forester stands 20 meters from the
        #  trunk, with his eye level at 1.6 meters, and aims a handheld
        #  clinometer at the treetop. It reads 40 degrees, giving a height of
        #  H = h_e + d tan θ, or 18.382 meters."
        # =====================================================================
        intro_tag = Text(
            "CASE 2  ·  CLASSIC FIELD QUESTION",
            font_size=20, color=TEAL_C, weight=BOLD
        ).move_to([0, 0.85, 0])

        play(
            FadeIn(sec_title, shift=DOWN * 0.15),
            FadeIn(intro_tag, shift=UP * 0.12),
            run_time=1.2,
        )

        # 3.95s: "how do you measure a tall tree without climbing it?"
        wait_until(3.95)
        intro_q = Text(
            "How do you measure a tall tree without climbing it?",
            font_size=31, color=WHITE, weight=BOLD
        ).move_to([0, 0.0, 0])
        intro_rule = Line(
            LEFT * 3.8, RIGHT * 3.8, color=TEAL_C, stroke_width=2.4, stroke_opacity=0.8
        ).next_to(intro_q, DOWN, buff=0.22)

        play(FadeIn(intro_q, shift=UP * 0.12),
             Create(intro_rule), run_time=2.0)

        # 6.55s: "A forester stands 20 meters from the trunk,"
        wait_until(6.55)

        y_g = -2.25
        tree_x = -4.95
        tree_h = 3.90
        y_top = y_g + tree_h       # +1.65
        eye_h = 0.45
        y_eye = y_g + eye_h        # -1.80
        # Góc thực chính xác 40 độ: d_px = (y_top - y_eye) / tan(40°) = 3.45 / 0.8391 = 4.11
        d_px = (y_top - y_eye) / np.tan(np.deg2rad(40.0))
        man_x = tree_x + d_px      # -0.84

        ground = Line([-6.1, y_g, 0], [0.15, y_g, 0],
                      color=GREY_B, stroke_width=2.2)
        tree = make_tree(tree_x, y_g, tree_h)
        forester = make_forester(man_x, y_g, eye_h)

        d_arrow = DoubleArrow(
            [tree_x, y_g - 0.36, 0], [man_x, y_g - 0.36, 0],
            buff=0, color=BLUE_B, stroke_width=2.4, tip_length=0.16
        )
        d_lbl = MathTex(r"d = 20\text{ m}", font_size=25, color=BLUE_B).next_to(
            d_arrow, DOWN, buff=0.1
        )

        play(
            FadeOut(VGroup(intro_tag, intro_q, intro_rule)),
            Create(ground),
            GrowFromEdge(tree, DOWN),
            FadeIn(forester, shift=LEFT * 0.25),
            GrowFromCenter(d_arrow),
            Write(d_lbl),
            run_time=2.3,
            rate_func=smooth,
        )

        # 9.50s: "with his eye level at 1.6 meters,"
        wait_until(9.50)
        eye_pt = np.array([man_x, y_eye, 0])
        trunk_eye_pt = np.array([tree_x, y_eye, 0])
        top_pt = np.array([tree_x, y_top, 0])

        eye_line = DashedLine(
            eye_pt, trunk_eye_pt, color=GREY_A, stroke_width=1.8, dash_length=0.12
        )
        he_tick = Line(
            [man_x + 0.35, y_g, 0], [man_x + 0.35, y_eye, 0],
            color=TEAL_B, stroke_width=3.2
        )
        he_lbl = MathTex(r"h_e = 1.6\text{ m}", font_size=22, color=TEAL_B).next_to(
            he_tick, RIGHT, buff=0.1
        )

        play(Create(eye_line), GrowFromEdge(
            he_tick, DOWN), Write(he_lbl), run_time=2.0)

        # 12.50s: "and aims a handheld clinometer at the treetop."
        wait_until(12.50)
        sight_line = Line(eye_pt, top_pt, color=YELLOW_C, stroke_width=3.0)
        clin_dot = Dot(eye_pt, color=YELLOW_C, radius=0.065)
        top_dot = Dot(top_pt, color=YELLOW_C, radius=0.065)

        play(
            FadeIn(clin_dot),
            Create(sight_line),
            FadeIn(top_dot),
            run_time=2.1,
            rate_func=smooth,
        )

        # 15.60s: "It reads 40 degrees,"
        wait_until(15.60)
        theta_rad = np.deg2rad(40.0)
        angle_arc = Arc(
            radius=0.88, start_angle=PI - theta_rad, angle=theta_rad,
            arc_center=eye_pt, color=YELLOW_C, stroke_width=2.8
        )
        angle_lbl = MathTex(r"\theta = 40^\circ", font_size=24, color=YELLOW_C).move_to(
            eye_pt + np.array([-1.32, 0.42, 0])
        )
        play(Create(angle_arc), Write(angle_lbl), run_time=1.25)

        # 17.15s: "giving a height of H equals h sub e"
        wait_until(17.15)
        rx = 1.15  # Căn lề trái sạch sẽ cho cột tính toán bên phải

        h_tag = Text("TREE HEIGHT", font_size=17, color=TEAL_C, weight=BOLD).move_to(
            [rx, 1.65, 0], aligned_edge=LEFT
        )
        h_eq = MathTex(
            r"H", r"= h_e", r"+ d\tan\theta", font_size=40, color=WHITE
        ).move_to([rx, 1.0, 0], aligned_edge=LEFT)
        h_eq[0].set_color(TEAL_C)
        h_eq[1].set_color(TEAL_B)
        h_eq[2].set_color(YELLOW_C)

        play(FadeIn(h_tag, shift=DOWN * 0.1),
             Write(h_eq[0]), Write(h_eq[1]), run_time=1.8)

        # 20.30s: "plus d tangent theta,"
        wait_until(20.30)
        h_above_brace = Brace(
            Line(trunk_eye_pt, top_pt), direction=LEFT, buff=0.58, color=TEAL_C
        )
        h_above_lbl = MathTex(r"d\tan\theta", font_size=22, color=TEAL_C).next_to(
            h_above_brace, LEFT, buff=0.08
        )

        play(
            Write(h_eq[2]),
            GrowFromCenter(h_above_brace),
            FadeIn(h_above_lbl, shift=RIGHT * 0.1),
            run_time=1.6,
        )

        # 22.15s: "or 18.382 meters."
        wait_until(22.15)
        h_val = MathTex(r"= 18.382\text{ m}", font_size=44, color=GREEN_C).move_to(
            [rx + 0.35, 0.22, 0], aligned_edge=LEFT
        )
        h_flash = Line(
            h_val.get_left(), h_val.get_right(), color=YELLOW_C, stroke_width=4
        ).next_to(h_val, DOWN, buff=0.12)

        play(Write(h_val), ShowPassingFlash(
            h_flash, time_width=0.55), run_time=2.2)

        # =====================================================================
        # BEAT 2 (25.65s – 57.80s): SAI SỐ ±1° -> NÓN BẤT ĐỊNH & KIỂM DUYỆT 5%
        # "Here's the problem: the clinometer only reads in whole degrees, so
        #  the angle carries an uncertainty of ±1°. Plugging that into our
        #  differential formula gives a height error of about 0.595 meters,
        #  putting the tree somewhere between 17.8 and 19 meters tall. Compared
        #  to the exact change of 0.604 meters, the discrepancy is only 1.47%,
        #  well inside our 5% rule."
        # =====================================================================
        wait_until(25.65)

        # Thu gọn phương trình H lên cao một chút để dành khoảng thoáng cho tính sai số
        h_compact = MathTex(
            r"H = h_e + d\tan\theta = 18.382\text{ m}", font_size=26, color=GREY_A
        ).move_to([rx, 1.82, 0], aligned_edge=LEFT)

        # Vạch chia từng độ nguyên quanh 40° (39°, 40°, 41°)
        tick_marks = VGroup()
        for deg_off in [-3.5, 0.0, 3.5]:
            ang = PI - np.deg2rad(40.0 + deg_off)
            p_in = eye_pt + 1.05 * np.array([np.cos(ang), np.sin(ang), 0])
            p_out = eye_pt + 1.25 * np.array([np.cos(ang), np.sin(ang), 0])
            tick_marks.add(
                Line(p_in, p_out, color=RED_B if deg_off !=
                     0 else YELLOW_C, stroke_width=2.6)
            )
        deg_note = Text(
            "Whole-degree readout only", font_size=18, color=ORANGE, weight=BOLD
        ).move_to([rx, 1.32, 0], aligned_edge=LEFT)

        play(
            FadeOut(VGroup(h_tag, h_above_brace, h_above_lbl)),
            ReplacementTransform(VGroup(h_eq, h_val), h_compact),
            Create(tick_marks),
            FadeIn(deg_note, shift=RIGHT * 0.15),
            run_time=2.5,
            rate_func=smooth,
        )

        # 29.05s: "so the angle carries an uncertainty of plus or minus 1 degree."
        wait_until(29.05)

        # Phóng đại nhẹ góc nón (±3.5° trên hình để mắt nhìn cực rõ) đại diện cho ±1°
        y_hi = y_eye + d_px * np.tan(np.deg2rad(43.5))
        y_lo = y_eye + d_px * np.tan(np.deg2rad(36.5))
        pt_hi = np.array([tree_x, y_hi, 0])
        pt_lo = np.array([tree_x, y_lo, 0])

        cone_poly = Polygon(
            eye_pt, pt_hi, pt_lo,
            fill_color=RED_C, fill_opacity=0.28,
            stroke_color=RED_B, stroke_width=1.8
        )
        dth_lbl = MathTex(r"\Delta\theta = \pm 1^\circ", font_size=28, color=RED_B).move_to(
            [rx, 0.85, 0], aligned_edge=LEFT
        )

        play(
            GrowFromPoint(cone_poly, eye_pt),
            Write(dth_lbl),
            run_time=2.7,
            rate_func=smooth,
        )

        # 33.35s: "Plugging that into our differential formula gives a height error of about"
        wait_until(33.35)
        dh_eq = MathTex(
            r"dH = d\sec^2\theta\cdot\Delta\theta", font_size=34, color=WHITE
        ).move_to([rx, 0.15, 0], aligned_edge=LEFT)
        play(Write(dh_eq), run_time=2.5)

        # 37.55s: "0.595 meters,"
        wait_until(37.55)
        dh_val = MathTex(r"\approx 0.595\text{ m}", font_size=38, color=YELLOW_C).move_to(
            [rx + 0.35, -0.52, 0], aligned_edge=LEFT
        )
        # Cọc sai số màu vàng/đỏ ngay trên đỉnh cây
        top_err_bar = Line(pt_lo, pt_hi, color=RED_C, stroke_width=5.5)
        cap_hi = Line(pt_hi + LEFT * 0.18, pt_hi + RIGHT *
                      0.18, color=RED_B, stroke_width=2.5)
        cap_lo = Line(pt_lo + LEFT * 0.18, pt_lo + RIGHT *
                      0.18, color=RED_B, stroke_width=2.5)
        top_err_grp = VGroup(top_err_bar, cap_hi, cap_lo)

        play(Write(dh_val), FadeIn(top_err_grp), run_time=1.9)

        # 40.25s: "putting the tree somewhere between 17.8 and 19 meters tall."
        wait_until(40.25)
        range_lbl_hi = MathTex(r"19.0\text{ m}", font_size=20, color=RED_B).next_to(
            cap_hi, LEFT, buff=0.1)
        range_lbl_lo = MathTex(r"17.8\text{ m}", font_size=20, color=RED_B).next_to(
            cap_lo, LEFT, buff=0.1)
        range_right = MathTex(
            r"H \in [\,17.8\text{ m},\; 19.0\text{ m}\,]", font_size=28, color=GREY_A
        ).move_to([rx, -1.15, 0], aligned_edge=LEFT)

        play(
            FadeIn(range_lbl_hi, shift=RIGHT * 0.1),
            FadeIn(range_lbl_lo, shift=RIGHT * 0.1),
            Write(range_right),
            Indicate(top_err_bar, color=YELLOW_C, scale_factor=1.12),
            run_time=3.2,
        )

        # 45.65s: "Compared to the exact change of 0.604 meters,"
        wait_until(45.65)
        div_r = Line([rx, -1.52, 0], [rx + 4.9, -1.52, 0],
                     color=SLATE, stroke_width=1.2, stroke_opacity=0.45)
        exact_dh = MathTex(
            r"\text{Exact }\Delta H = 0.604\text{ m}", font_size=28, color=TEAL_C
        ).move_to([rx, -1.92, 0], aligned_edge=LEFT)
        play(Create(div_r), Write(exact_dh), run_time=2.6)

        # 50.80s: "the discrepancy is only 1.47%,"
        wait_until(50.80)
        disc_val = MathTex(
            r"\text{Discrepancy} = 1.47\%", font_size=30, color=GREEN_C
        ).move_to([rx, -2.48, 0], aligned_edge=LEFT)
        play(Write(disc_val), run_time=2.4)

        # 54.65s: "well inside our 5% rule." -> Thanh kiểm duyệt mini đồng bộ Scene 5 & 6!
        wait_until(54.65)
        mb_w = 4.6
        mb_y = -3.02
        mb_left = rx
        mb_gw = mb_w * (5.0 / 8.0)
        mb_rw = mb_w * (3.0 / 8.0)
        mb_x5 = mb_left + mb_gw

        mb_green = RoundedRectangle(
            width=mb_gw, height=0.16, corner_radius=0.05,
            fill_color=GREEN_C, fill_opacity=0.88, stroke_width=0
        ).move_to([mb_left + mb_gw / 2.0, mb_y, 0])
        mb_red = RoundedRectangle(
            width=mb_rw, height=0.16, corner_radius=0.05,
            fill_color=RED_C, fill_opacity=0.35, stroke_width=0
        ).move_to([mb_x5 + mb_rw / 2.0, mb_y, 0])
        mb_5line = Line([mb_x5, mb_y - 0.22, 0], [mb_x5, mb_y +
                        0.24, 0], color=YELLOW_C, stroke_width=2.6)
        mb_5lbl = MathTex(r"5\%", font_size=18, color=YELLOW_C).next_to(
            mb_5line, RIGHT, buff=0.08).shift(UP * 0.16)
        mb_dot = Dot([mb_left + mb_w * (1.47 / 8.0), mb_y, 0],
                     color=WHITE, radius=0.09)
        mb_ring = Circle(radius=0.15, color=GREEN_C,
                         stroke_width=2.2).move_to(mb_dot.get_center())

        mini_bar_grp = VGroup(mb_green, mb_red, mb_5line,
                              mb_5lbl, mb_dot, mb_ring)
        play(
            FadeIn(mini_bar_grp, shift=UP * 0.12),
            Indicate(disc_val, color=YELLOW_C, scale_factor=1.1),
            run_time=2.0,
        )

        wait_until(57.00)
        beat12_all = VGroup(
            ground, tree, forester, d_arrow, d_lbl, eye_line, he_tick, he_lbl,
            sight_line, clin_dot, top_dot, angle_arc, angle_lbl, tick_marks,
            cone_poly, top_err_grp, range_lbl_hi, range_lbl_lo,
            h_compact, deg_note, dth_lbl, dh_eq, dh_val, range_right,
            div_r, exact_dh, disc_val, mini_bar_grp,
        )
        play(FadeOut(beat12_all), run_time=0.8)

        # =====================================================================
        # BEAT 3 (57.85s – 93.30s): CÂU HỎI THÔNG MINH HƠN — ĐỨNG ĐÂU ĐO CHUẨN NHẤT?
        # "Now for a much smarter question: where should the forester stand to
        #  get the best measurement? Watch what happens as he walks towards the
        #  tree. If he stands too far away, the linearization is super accurate,
        #  but the angle is so shallow that a 1 degree tilt blows up into a huge
        #  percentage error in height. On the other hand, if he stands too close,
        #  closer than about 5.87 meters, the angle gets steep, tangent theta
        #  shoots upward, and the linear estimate crosses our 5% limit and
        #  becomes invalid."
        # =====================================================================
        wait_until(57.85)

        q2_tag = Text("A SMARTER QUESTION", font_size=19,
                      color=YELLOW_C, weight=BOLD).move_to([0, 0.78, 0])
        q2_main = Text(
            "Where should the forester stand for the best measurement?",
            font_size=30, color=WHITE, weight=BOLD
        ).move_to([0, 0.0, 0])
        q2_rule = Line(LEFT * 4.2, RIGHT * 4.2, color=YELLOW_C, stroke_width=2.4, stroke_opacity=0.8).next_to(
            q2_main, DOWN, buff=0.22
        )

        play(
            FadeIn(q2_tag, shift=DOWN * 0.1),
            FadeIn(q2_main, shift=UP * 0.12),
            Create(q2_rule),
            run_time=2.6,
        )

        # 62.40s: Chuyển sang màn hình kép động: Hiện trường tỷ lệ 1:1 (trái) & Đồ thị chữ U (phải)
        wait_until(62.40)

        # Hằng số toán học chính xác của bài toán cây
        H_ABOVE = 20.0 * np.tan(np.deg2rad(40.0))  # 16.782 m
        H_TRUE = 1.6 + H_ABOVE                     # 18.382 m
        DTH_RAD = np.deg2rad(1.0)

        def err_pct_fn(d):
            return ((d + (H_ABOVE ** 2) / d) * DTH_RAD / H_TRUE) * 100.0

        # --- Sân khấu hiện trường tỷ lệ thật 1:1 bên trái ---
        g_y3 = -1.75
        tree_x3 = -5.75
        scale3 = 0.112            # 45 m -> 5.04 units (x = -0.71)
        eye_h3 = 0.28
        y_eye3 = g_y3 + eye_h3    # -1.47
        h_above_px = H_ABOVE * scale3  # 1.88 units -> y_top3 = +0.41
        y_top3 = y_eye3 + h_above_px

        ground3 = Line([-6.2, g_y3, 0], [-0.35, g_y3, 0],
                       color=GREY_B, stroke_width=2.0)
        tree3 = make_tree(tree_x3, g_y3, y_top3 - g_y3)

        # --- Hệ trục đồ thị sai số bên phải ---
        ax = Axes(
            x_range=[0, 50, 10],
            y_range=[2, 8, 1],
            x_length=5.45,
            y_length=4.15,
            axis_config={
                "color": GREY_B,
                "stroke_width": 1.8,
                "include_tip": True,
                "tip_width": 0.12,
                "tip_height": 0.12,
                "include_numbers": True,
                "font_size": 17,
            },
            x_axis_config={"numbers_to_include": [10, 20, 30, 40, 50]},
            y_axis_config={"numbers_to_include": [2, 4, 6, 8]},
        ).move_to([3.45, -0.45, 0])

        ax_x_lbl = Text("Distance d (m)", font_size=17, color=GREY_A).next_to(
            ax.x_axis, DOWN, buff=0.45
        )
        ax_y_lbl = Text("Height Error (%)", font_size=17, color=BLUE_B).next_to(
            ax.y_axis.get_top(), UP, buff=0.16
        ).shift(RIGHT * 0.45)

        # ValueTracker điều khiển khoảng cách d của người kiểm lâm
        d_t = ValueTracker(45.0)
        # ValueTracker theo dõi cận trái nhỏ nhất của đường cong đã được vẽ
        d_min_drawn = ValueTracker(45.0)

        def get_live_field():
            d = d_t.get_value()
            mx = tree_x3 + d * scale3
            ep = np.array([mx, y_eye3, 0])
            tp = np.array([tree_x3, y_top3, 0])
            th_rad = np.arctan(H_ABOVE / d)
            th_deg = np.rad2deg(th_rad)

            man = make_forester(mx, g_y3, eye_h3)
            # Nón bất định phóng nhẹ ±2.4° để thấy rõ sự co/phình theo d (tối thiểu tại 16.8m!)
            ang_hi = min(th_rad + np.deg2rad(2.4), np.deg2rad(81.0))
            ang_lo = max(th_rad - np.deg2rad(2.4), np.deg2rad(2.0))
            yh = y_eye3 + (d * scale3) * np.tan(ang_hi)
            yl = y_eye3 + (d * scale3) * np.tan(ang_lo)

            is_invalid = d < 5.87
            is_sweet = 15.0 <= d <= 20.0
            cone_col = RED_C if is_invalid else (
                GREEN_C if is_sweet else ORANGE)

            cone = Polygon(
                ep, [tree_x3, yh, 0], [tree_x3, yl, 0],
                fill_color=cone_col, fill_opacity=0.30,
                stroke_color=cone_col, stroke_width=1.4
            )
            ray = Line(ep, tp, color=YELLOW_C, stroke_width=2.2)
            band = Line([tree_x3, yl, 0], [tree_x3, yh, 0],
                        color=cone_col, stroke_width=5.5)

            # Cung góc ngắm θ
            arc_r = min(0.65, d * scale3 * 0.55)
            arc = Arc(
                radius=arc_r, start_angle=PI - th_rad, angle=th_rad,
                arc_center=ep, color=YELLOW_C, stroke_width=2.2
            )

            # Thông số đọc trực tiếp phía trên sân khấu trái
            readout = VGroup(
                MathTex(rf"d = {d:.1f}\text{{ m}}", font_size=26, color=WHITE),
                MathTex(rf"\theta = {th_deg:.1f}^\circ",
                        font_size=26, color=YELLOW_C),
                MathTex(
                    rf"\text{{Err}} = {err_pct_fn(d):.2f}\%",
                    font_size=26,
                    color=RED_B if is_invalid else (
                        GREEN_C if is_sweet else BLUE_B),
                ),
            ).arrange(RIGHT, buff=0.45).move_to([-3.25, 1.8, 0])

            return VGroup(cone, ray, band, arc, man, readout)

        dyn_field = always_redraw(get_live_field)

        # Đường cong xanh tự vẽ dần từ d = 45m về trái theo bước đi của kiểm lâm
        dyn_curve_trace = always_redraw(
            lambda: ax.plot(
                err_pct_fn,
                x_range=[max(d_min_drawn.get_value(), 4.2), 45.05],
                color=BLUE_C,
                stroke_width=3.6,
            )
            if d_min_drawn.get_value() < 44.8
            else VGroup()
        )

        dyn_curve_dot = always_redraw(
            lambda: Dot(
                ax.c2p(d_t.get_value(), min(err_pct_fn(d_t.get_value()), 7.9)),
                color=RED_C if d_t.get_value() < 5.87 else (
                    GREEN_C if 15.0 <= d_t.get_value() <= 20.0 else YELLOW_C),
                radius=0.095,
            )
        )

        play(
            FadeOut(VGroup(q2_tag, q2_main, q2_rule)),
            Create(ground3),
            GrowFromEdge(tree3, DOWN),
            Create(ax),
            FadeIn(ax_x_lbl),
            FadeIn(ax_y_lbl),
            FadeIn(dyn_field),
            FadeIn(dyn_curve_trace),
            FadeIn(dyn_curve_dot),
            run_time=2.4,
            rate_func=smooth,
        )

        # 66.45s: "If he stands too far away, the linearization is super accurate,"
        wait_until(66.45)
        far_tag = VGroup(
            Text("Too Far (d = 45 m)", font_size=18, color=ORANGE, weight=BOLD),
            Text("Linearization ✓  ·  Shallow θ", font_size=15, color=GREY_A),
        ).arrange(DOWN, buff=0.08).move_to(ax.c2p(36.0, 6.95))
        far_ptr = Arrow(
            far_tag.get_bottom(), ax.c2p(44.5, err_pct_fn(45.0) + 0.15),
            buff=0.08, color=ORANGE, stroke_width=2.2, max_tip_length_to_length_ratio=0.22
        )

        play(FadeIn(far_tag, shift=DOWN * 0.1),
             GrowArrow(far_ptr), run_time=3.0)

        # 70.90s: "but the angle is so shallow that a 1 degree tilt blows up into a huge percentage error in height."
        wait_until(70.90)
        far_warn = Text(
            "Shallow angle → Huge % error!", font_size=19, color=ORANGE, weight=BOLD
        ).move_to([-3.25, -2.5, 0])

        play(
            FadeIn(far_warn, shift=UP * 0.1),
            Indicate(dyn_curve_dot, color=ORANGE, scale_factor=1.6),
            run_time=3.5,
        )
        # Bước vào nhẹ từ 45 m -> 28 m, kéo theo đường cong xanh bắt đầu hạ xuống
        play(
            d_t.animate.set_value(28.0),
            d_min_drawn.animate.set_value(28.0),
            FadeOut(VGroup(far_tag, far_ptr, far_warn)),
            run_time=2.6,
            rate_func=smooth,
        )

        # 78.15s: "On the other hand, if he stands too close, closer than about 5.87 meters,"
        wait_until(78.15)
        play(
            d_t.animate.set_value(4.6),
            d_min_drawn.animate.set_value(4.6),
            run_time=3.8,
            rate_func=smooth,
        )

        # Bật vùng cấm màu đỏ d < 5.87 m trên đồ thị + vạch đứng 5.87 m
        inv_x_left = ax.c2p(0, 2)[0]
        inv_x_right = ax.c2p(5.87, 2)[0]
        inv_y_bot = ax.c2p(0, 2)[1]
        inv_y_top = ax.c2p(0, 8)[1]

        invalid_zone = Rectangle(
            width=inv_x_right - inv_x_left,
            height=inv_y_top - inv_y_bot,
            fill_color=RED_C,
            fill_opacity=0.26,
            stroke_width=0,
        ).move_to([(inv_x_left + inv_x_right) / 2.0, (inv_y_bot + inv_y_top) / 2.0, 0])

        limit_vline = DashedLine(
            ax.c2p(5.87, 2.0), ax.c2p(5.87, 8.0),
            color=RED_C, stroke_width=2.6, dash_length=0.12
        )
        limit_587_lbl = MathTex(r"5.87\text{ m}", font_size=19, color=RED_B).next_to(
            ax.c2p(5.87, 8.0), RIGHT, buff=0.08
        ).shift(DOWN * 0.15)

        # Đổi đoạn cong bên trái 5.87m thành nét đứt đỏ để nhấn mạnh không hợp lệ
        invalid_curve_seg = ax.plot(
            err_pct_fn, x_range=[4.2, 5.87], color=RED_C, stroke_width=4.2
        )

        play(
            FadeIn(invalid_zone),
            Create(limit_vline),
            Write(limit_587_lbl),
            Create(invalid_curve_seg),
            run_time=1.8,
        )

        # 84.25s: "the angle gets steep, tangent theta shoots upward,"
        wait_until(84.25)
        steep_note = MathTex(
            r"\text{Steep }\theta \;\longrightarrow\; \tan\theta\text{ shoots up!}",
            font_size=24, color=RED_B
        ).move_to([-3.25, -2.5, 0])

        play(FadeIn(steep_note, shift=UP * 0.1), run_time=2.5)

        # 87.55s: "and the linear estimate crosses our 5% limit and becomes invalid."
        wait_until(87.55)
        inv_tag = Text(
            "> 5% LIMIT\nINVALID", font_size=16, color=RED_B, weight=BOLD
        ).move_to(ax.c2p(12.2, 6.85))
        inv_ptr = Arrow(
            inv_tag.get_left(), ax.c2p(4.9, 6.5),
            buff=0.06, color=RED_C, stroke_width=2.2, max_tip_length_to_length_ratio=0.25
        )

        play(
            FadeIn(inv_tag, scale=0.9),
            GrowArrow(inv_ptr),
            Indicate(invalid_zone, color=RED_C, scale_factor=1.03),
            run_time=2.8,
        )

        # =====================================================================
        # BEAT 4 (93.30s – 111.20s): ĐÁY ĐƯỜNG CONG XANH (16.8m, 45°) & SWEET SPOT (15–20m)
        # "As the blue curve shows, the total measurement error hits rock bottom
        #  around 16.8 meters, right where the elevation angle is nearly 45
        #  degrees. So the sweet spot in this field is standing 15 to 20 meters
        #  from the trunk."
        # =====================================================================
        wait_until(93.30)

        # Thay thế đường vẽ động bằng đường cong xanh hoàn chỉnh tuyệt đẹp
        full_blue_curve = ax.plot(
            err_pct_fn, x_range=[5.87, 48.0], color=BLUE_C, stroke_width=4.0
        )
        self.remove(dyn_curve_trace)
        self.add(full_blue_curve, invalid_curve_seg, dyn_curve_dot)

        # Kiểm lâm bước mượt từ 4.6 m ra đúng đáy đường cong d = 16.8 m!
        play(
            FadeOut(VGroup(steep_note, inv_tag, inv_ptr)),
            ShowPassingFlash(full_blue_curve.copy().set_color(
                TEAL_A).set_stroke(width=6), time_width=0.45),
            d_t.animate.set_value(16.8),
            run_time=4.2,
            rate_func=smooth,
        )

        # Thả điểm đáy vàng tại (16.8 m, 3.19%)
        min_pt = ax.c2p(16.8, err_pct_fn(16.8))
        min_vguide = DashedLine(
            ax.c2p(16.8, 2.0), min_pt, color=YELLOW_C, stroke_width=1.8, dash_length=0.1
        )
        min_ring = Circle(radius=0.17, color=YELLOW_C,
                          stroke_width=2.6).move_to(min_pt)
        min_lbl = MathTex(
            r"\text{Min: } d \approx 16.8\text{ m}", font_size=24, color=YELLOW_C
        ).move_to(ax.c2p(28.5, 2.75))
        min_ptr = Arrow(
            min_lbl.get_left(), min_pt + RIGHT * 0.16,
            buff=0.06, color=YELLOW_C, stroke_width=2.2, max_tip_length_to_length_ratio=0.25
        )

        play(
            Create(min_vguide),
            Create(min_ring),
            Write(min_lbl),
            GrowArrow(min_ptr),
            run_time=1.8,
        )

        # 99.85s: "right where the elevation angle is nearly 45 degrees."
        wait_until(99.85)
        ang45_badge = MathTex(
            r"\theta \approx 45^\circ\;\text{ (Optimal Angle)}", font_size=26, color=YELLOW_C
        ).move_to([-3.25, -2.5, 0])
        ang45_flash = Line(
            ang45_badge.get_left(), ang45_badge.get_right(), color=YELLOW_C, stroke_width=3.5
        ).next_to(ang45_badge, DOWN, buff=0.1)

        play(
            Write(ang45_badge),
            ShowPassingFlash(ang45_flash, time_width=0.5),
            run_time=2.6,
        )

        # 103.50s: "So the sweet spot in this field is standing 15 to 20 meters from the trunk."
        wait_until(103.50)

        # Dải xanh ngọc SWEET SPOT (15m – 20m) trên ĐỒ THỊ bên phải
        sw_xl = ax.c2p(15.0, 2)[0]
        sw_xr = ax.c2p(20.0, 2)[0]
        sweet_graph_band = Rectangle(
            width=sw_xr - sw_xl,
            height=inv_y_top - inv_y_bot,
            fill_color=GREEN_C,
            fill_opacity=0.24,
            stroke_color=GREEN_C,
            stroke_width=1.4,
        ).move_to([(sw_xl + sw_xr) / 2.0, (inv_y_bot + inv_y_top) / 2.0, 0])

        # Dải xanh ngọc SWEET SPOT (15m – 20m) ngay trên MẶT ĐẤT bên trái!
        gx_15 = tree_x3 + 15.0 * scale3
        gx_20 = tree_x3 + 20.0 * scale3
        sweet_ground_bar = Line(
            [gx_15, g_y3, 0], [gx_20, g_y3, 0], color=GREEN_C, stroke_width=8.5
        )
        sweet_ground_lbl = MathTex(r"15\text{–}20\text{ m}", font_size=20, color=GREEN_C).next_to(
            sweet_ground_bar, DOWN, buff=0.14
        )

        play(
            FadeIn(sweet_graph_band),
            GrowFromCenter(sweet_ground_bar),
            FadeIn(sweet_ground_lbl, shift=UP * 0.08),
            run_time=3.2,
            rate_func=smooth,
        )

        # Bật nhãn chốt SWEET SPOT: 15–20 m nổi bật trên đồ thị
        sweet_title = Text(
            "SWEET SPOT: 15–20 m", font_size=21, color=GREEN_C, weight=BOLD
        ).move_to(ax.c2p(28.5, 6.95))
        sweet_flash = Line(
            sweet_title.get_left(), sweet_title.get_right(), color=YELLOW_C, stroke_width=3.8
        ).next_to(sweet_title, DOWN, buff=0.1)

        play(
            Write(sweet_title),
            ShowPassingFlash(sweet_flash, time_width=0.55),
            Indicate(sweet_ground_bar, color=YELLOW_C, scale_factor=1.18),
            run_time=2.0,
        )

        # Giữ hình thêm ~1.3s cuối để người xem kịp nhìn trọn kết luận
        wait_until(111.20)
