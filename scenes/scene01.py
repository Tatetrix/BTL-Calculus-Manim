from manim import *
import numpy as np


class Scene01(Scene):
    def construct(self):
        # Bảng màu đồng bộ toàn bộ dự án
        self.camera.background_color = "#0F172A"
        SLATE = "#64748B"
        CARD_BG = "#1E293B"

        # Tự động ghép file tiếng khi render nháp (xóa hoặc thêm # khi render final không tiếng)
        self.add_sound("Recordings/Scene01(1).wav")

        # =====================================================================
        # PHẦN 1: MÀN HÌNH MỞ ĐẦU & THU GỌN HEADER (0:00 – 0:08.5 | 8.5s)
        # =====================================================================
        title_main = Text(
            "CALCULUS 1 PROJECT",
            font_size=46,
            color=TEAL_C,
            weight=BOLD,
        ).shift(UP * 1.15)

        title_sub = Text(
            "Topic 9: Differentials, Linearization & Error Propagation",
            font_size=26,
            color=WHITE,
            weight=BOLD,
        ).next_to(title_main, DOWN, buff=0.35)

        title_line = Line(
            LEFT * 4.6, RIGHT * 4.6, color=YELLOW_C, stroke_width=2.5
        ).next_to(title_sub, DOWN, buff=0.35)

        group_tag = Text(
            "Group 4 — Class CC01",
            font_size=22,
            color=GREY_B,
        ).next_to(title_line, DOWN, buff=0.3)

        self.play(
            FadeIn(title_main, shift=DOWN * 0.2),
            FadeIn(title_sub, shift=UP * 0.15),
            run_time=1.2,
        )
        self.play(Create(title_line), FadeIn(group_tag), run_time=0.8)
        # Chờ đọc lời chào & giới thiệu nhóm
        self.wait(5.0)

        # Thu gọn lên thanh header cố định góc trái trên
        header_badge = VGroup(
            Text("Group 4 (CC01)", font_size=16, color=TEAL_C, weight=BOLD),
            Text("Topic 9: Error Propagation", font_size=18, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.06)
        header_badge.to_corner(UL, buff=0.35)

        header_line = Line(
            LEFT * 6.8, RIGHT * 6.8, color=SLATE, stroke_width=1, stroke_opacity=0.4
        ).next_to(header_badge, DOWN, buff=0.15, aligned_edge=LEFT)

        self.play(
            FadeOut(VGroup(title_main, title_sub, title_line)),
            ReplacementTransform(group_tag, header_badge),
            Create(header_line),
            run_time=1.5,
        )

        # =====================================================================
        # PHẦN 2: CHỨNG MINH MỌI PHÉP ĐO ĐỀU LÀ XẤP XỈ (0:08.5 – 0:34.5 | 26.0s)
        # =====================================================================
        sec2_title = Text(
            "Why Every Instrument Reading Is an Approximation",
            font_size=25,
            color=YELLOW_C,
            weight=BOLD,
        ).to_edge(UP, buff=0.38).shift(RIGHT * 1.45)

        # Thanh trực quan hóa: Giá trị thật liên tục vs Số đọc rời rạc
        approx_banner = VGroup(
            MathTex(r"\text{True Continuous Value}",
                    font_size=24, color=BLUE_B),
            MathTex(r"\neq", font_size=28, color=RED_C),
            MathTex(r"\text{Instrument Reading (Rounded)}",
                    font_size=24, color=YELLOW_C),
        ).arrange(RIGHT, buff=0.3).move_to(UP * 1.4)

        self.play(FadeIn(sec2_title, shift=DOWN * 0.15), run_time=0.8)
        self.play(FadeIn(approx_banner, scale=0.95), run_time=1.0)
        # Chờ đọc câu hỏi: "So have you ever noticed that every number we read..."
        self.wait(6.2)

        self.play(FadeOut(approx_banner), run_time=0.4)

        # ---------------------------------------------------------------------
        # 2A. THƯỚC KẺ + KÍNH LÚP PHÓNG ĐẠI (0:16.5 – 0:21.5 | 5.0s)
        # ---------------------------------------------------------------------
        ruler_stage = VGroup()
        ruler_body = Rectangle(
            width=5.4, height=0.85, fill_color="#334155", fill_opacity=1,
            stroke_color=WHITE, stroke_width=1.8
        ).move_to([-1.2, -0.85, 0])

        # Vạch chia trên thước
        r_ticks = VGroup()
        for i in range(11):
            x_pos = ruler_body.get_left()[0] + 0.4 + i * 0.46
            h = 0.34 if i % 5 == 0 else 0.2
            r_ticks.add(
                Line(
                    [x_pos, ruler_body.get_top()[1], 0],
                    [x_pos, ruler_body.get_top()[1] - h, 0],
                    color=WHITE, stroke_width=2
                )
            )
        r_lbl_42 = MathTex(r"4.2", font_size=18, color=GREY_A).next_to(
            r_ticks[6], DOWN, buff=0.08)
        r_lbl_43 = MathTex(r"4.3", font_size=18, color=GREY_A).next_to(
            r_ticks[7], DOWN, buff=0.08)

        # Thanh vật thể màu xanh dừng lửng ở giữa vạch 4.2 và 4.3
        target_x = (r_ticks[6].get_center()[0] +
                    r_ticks[7].get_center()[0]) * 0.5 + 0.05
        measured_rod = Rectangle(
            width=target_x - ruler_body.get_left()[0],
            height=0.36,
            fill_color=BLUE_C,
            fill_opacity=0.85,
            stroke_color=BLUE_B,
            stroke_width=1.5,
        ).align_to(ruler_body, LEFT).shift(UP * 0.68)

        # Vòng chọn vùng phóng đại trên thước
        focus_box = RoundedRectangle(
            width=0.75, height=0.95, corner_radius=0.08,
            color=YELLOW_C, stroke_width=2.2
        ).move_to([target_x, ruler_body.get_top()[1] + 0.05, 0])

        ruler_stage.add(ruler_body, r_ticks, r_lbl_42,
                        r_lbl_43, measured_rod, focus_box)

        # KÍNH LÚP ZOOM-IN BÊN PHẢI
        lens_center = np.array([3.65, 0.25, 0])
        lens_r = 1.42
        lens_bg = Circle(
            radius=lens_r, fill_color=CARD_BG, fill_opacity=0.98,
            stroke_color=YELLOW_C, stroke_width=3.5
        ).move_to(lens_center)

        # Hai vạch chia phóng đại bên trong kính lúp
        z_tick_left = Line(
            lens_center + LEFT * 0.72 + DOWN * 0.55,
            lens_center + LEFT * 0.72 + UP * 0.45,
            color=WHITE, stroke_width=3.5
        )
        z_tick_right = Line(
            lens_center + RIGHT * 0.72 + DOWN * 0.55,
            lens_center + RIGHT * 0.72 + UP * 0.45,
            color=WHITE, stroke_width=3.5
        )
        z_lbl_left = MathTex(r"4.2\text{ cm}", font_size=20, color=GREY_A).next_to(
            z_tick_left, DOWN, buff=0.1)
        z_lbl_right = MathTex(r"4.3\text{ cm}", font_size=20, color=YELLOW_C).next_to(
            z_tick_right, DOWN, buff=0.1)

        # Mép vật thể phóng đại dừng tại 4.26 cm (nằm lơ lửng giữa 2 vạch!)
        z_rod = Rectangle(
            width=1.45, height=0.45, fill_color=BLUE_C, fill_opacity=0.9,
            stroke_color=BLUE_B, stroke_width=2
        ).move_to(lens_center + LEFT * 0.52 + UP * 0.12)
        z_edge_x = z_rod.get_right()[0]
        z_true_line = DashedLine(
            [z_edge_x, lens_center[1] - 0.55, 0],
            [z_edge_x, lens_center[1] + 0.65, 0],
            color=BLUE_B, stroke_width=2.2
        )

        # Vùng sai số làm tròn màu đỏ giữa 4.26 và 4.30
        z_err_gap = Rectangle(
            width=z_tick_right.get_center()[0] - z_edge_x,
            height=0.45,
            fill_color=RED_C,
            fill_opacity=0.55,
            stroke_color=RED_C,
            stroke_width=1.5,
        ).align_to(z_rod, LEFT).shift(RIGHT * z_rod.width).set_y(z_rod.get_y())
        z_err_lbl = MathTex(r"\Delta x", font_size=22, color=RED_B).next_to(
            z_err_gap, UP, buff=0.08)

        # Hai tia nối từ ô chọn trên thước tới kính lúp
        ray1 = DashedLine(focus_box.get_top(), lens_bg.get_top(
        ) + LEFT * 0.4, color=YELLOW_C, stroke_width=1.5)
        ray2 = DashedLine(focus_box.get_bottom(), lens_bg.get_bottom(
        ) + LEFT * 0.4, color=YELLOW_C, stroke_width=1.5)

        zoom_lens = VGroup(
            lens_bg, z_tick_left, z_tick_right, z_lbl_left, z_lbl_right,
            z_rod, z_true_line, z_err_gap, z_err_lbl
        )
        ruler_caption = Text(
            "Ruler: Finite tick marks → rounds between ticks",
            font_size=20, color=TEAL_C, weight=BOLD
        ).move_to([0.8, -2.25, 0])

        self.play(FadeIn(ruler_stage), FadeIn(ruler_caption), run_time=0.8)
        self.play(
            Create(ray1), Create(ray2),
            FadeIn(zoom_lens, scale=0.6),
            run_time=1.3,
        )
        self.play(Indicate(z_err_gap, color=RED_C,
                  scale_factor=1.15), run_time=0.7)
        # Chờ hết câu: "A ruler has finite tick marks,"
        self.wait(1.8)

        # Thu nhỏ Thước kẻ vào cột Dock bên trái
        dock_ruler = VGroup(
            RoundedRectangle(width=2.5, height=0.95, corner_radius=0.12, fill_color=CARD_BG,
                             fill_opacity=0.95, stroke_color=TEAL_C, stroke_width=1.8),
            Text("Ruler", font_size=18, color=TEAL_C,
                 weight=BOLD).shift(UP * 0.18),
            MathTex(r"\pm\Delta x\text{ (ticks)}",
                    font_size=18, color=RED_B).shift(DOWN * 0.2),
        ).move_to([-4.95, 1.05, 0])

        self.play(
            FadeOut(VGroup(zoom_lens, ray1, ray2, ruler_caption)),
            ReplacementTransform(ruler_stage, dock_ruler),
            run_time=0.6,
        )

        # ---------------------------------------------------------------------
        # 2B. ĐỒNG HỒ BẤM GIỜ: KIM QUÉT LIÊN TỤC VS SỐ NHẢY BẬC (0:21.5 – 0:24.5 | 3.0s)
        # ---------------------------------------------------------------------
        t_tracker = ValueTracker(3.40)
        sw_center = np.array([1.1, 0.35, 0])
        sw_ring = Circle(
            radius=1.15, fill_color=CARD_BG, fill_opacity=0.95,
            stroke_color=BLUE_C, stroke_width=3.5
        ).move_to(sw_center)

        # Kim analog quay mượt liên tục
        sw_hand = always_redraw(
            lambda: Line(
                sw_center,
                sw_center + 0.9 * np.array([
                    np.sin((t_tracker.get_value() - 3.40) * 18),
                    np.cos((t_tracker.get_value() - 3.40) * 18),
                    0
                ]),
                color=YELLOW_C,
                stroke_width=3,
            )
        )
        # Màn hình số nhảy từng nấc 0.1s (làm tròn thô)
        sw_lcd = always_redraw(
            lambda: VGroup(
                RoundedRectangle(width=2.4, height=0.65, corner_radius=0.1, fill_color="#0F172A",
                                 fill_opacity=1, stroke_color=BLUE_B, stroke_width=1.8),
                MathTex(
                    rf"{np.round(t_tracker.get_value(), 1):.1f}\text{{ s}}",
                    font_size=28,
                    color=GREEN_C,
                ),
            ).move_to(sw_center + DOWN * 1.65)
        )
        sw_true_lbl = always_redraw(
            lambda: MathTex(
                rf"\text{{True: }}{t_tracker.get_value():.3f}\text{{ s}}",
                font_size=22,
                color=GREY_A,
            ).next_to(sw_ring, RIGHT, buff=0.45)
        )
        sw_caption = Text(
            "Stopwatch: Finite resolution → discrete jumps",
            font_size=20, color=BLUE_C, weight=BOLD
        ).move_to([1.1, -2.35, 0])

        self.play(
            FadeIn(sw_ring), FadeIn(sw_hand), FadeIn(sw_lcd),
            FadeIn(sw_true_lbl), FadeIn(sw_caption),
            run_time=0.5,
        )
        self.play(t_tracker.animate.set_value(3.486),
                  run_time=1.4, rate_func=linear)
        self.wait(0.5)

        # Thu nhỏ Đồng hồ vào cột Dock bên trái
        dock_watch = VGroup(
            RoundedRectangle(width=2.5, height=0.95, corner_radius=0.12, fill_color=CARD_BG,
                             fill_opacity=0.95, stroke_color=BLUE_C, stroke_width=1.8),
            Text("Stopwatch", font_size=18, color=BLUE_C,
                 weight=BOLD).shift(UP * 0.18),
            MathTex(r"\pm\Delta t\text{ (resolution)}",
                    font_size=18, color=RED_B).shift(DOWN * 0.2),
        ).move_to([-4.95, -0.25, 0])

        self.play(
            FadeOut(VGroup(sw_hand, sw_lcd, sw_true_lbl, sw_caption)),
            ReplacementTransform(sw_ring, dock_watch),
            run_time=0.5,
        )

        # ---------------------------------------------------------------------
        # 2C. CÂN ĐIỆN TỬ: QUẢ CÂN RƠI & LÀM TRÒN CHỮ SỐ (0:24.5 – 0:27.5 | 3.0s)
        # ---------------------------------------------------------------------
        sc_base = RoundedRectangle(
            width=3.2, height=1.1, corner_radius=0.15,
            fill_color=CARD_BG, fill_opacity=0.95, stroke_color=PURPLE_B, stroke_width=2.5
        ).move_to([1.1, -0.95, 0])
        sc_pan = Line(
            sc_base.get_top() + UP * 0.22 + LEFT * 1.3,
            sc_base.get_top() + UP * 0.22 + RIGHT * 1.3,
            color=WHITE, stroke_width=4
        )
        sc_lcd = MathTex(r"50.2\text{ g}", font_size=32, color=YELLOW_C).move_to(
            sc_base.get_center())

        weight_block = RoundedRectangle(
            width=1.1, height=0.75, corner_radius=0.1,
            fill_color=PURPLE_C, fill_opacity=0.9, stroke_color=WHITE, stroke_width=1.8
        ).move_to(sc_pan.get_center() + UP * 1.1)
        true_mass_lbl = MathTex(
            r"\text{True Mass: } 50.238\text{ g}", font_size=23, color=GREY_A
        ).next_to(sc_base, RIGHT, buff=0.45)
        sc_caption = Text(
            "Scale: Finite precision → truncates extra digits",
            font_size=20, color=PURPLE_B, weight=BOLD
        ).move_to([1.1, -2.25, 0])

        self.play(
            FadeIn(sc_base), Create(sc_pan), FadeIn(sc_caption),
            weight_block.animate.move_to(sc_pan.get_center() + UP * 0.4),
            run_time=0.9,
        )
        self.play(Write(sc_lcd), FadeIn(true_mass_lbl), run_time=0.7)
        self.wait(0.8)

        dock_scale = VGroup(
            RoundedRectangle(width=2.5, height=0.95, corner_radius=0.12, fill_color=CARD_BG,
                             fill_opacity=0.95, stroke_color=PURPLE_B, stroke_width=1.8),
            Text("Scale", font_size=18, color=PURPLE_B,
                 weight=BOLD).shift(UP * 0.18),
            MathTex(r"\pm\Delta m\text{ (precision)}",
                    font_size=18, color=RED_B).shift(DOWN * 0.2),
        ).move_to([-4.95, -1.55, 0])

        self.play(
            FadeOut(VGroup(sc_pan, sc_lcd, weight_block,
                    true_mass_lbl, sc_caption)),
            ReplacementTransform(sc_base, dock_scale),
            run_time=0.5,
        )

        # ---------------------------------------------------------------------
        # 2D. HỘI TỤ SAI SỐ BÁM THEO (0:27.5 – 0:34.5 | 7.0s)
        # ---------------------------------------------------------------------
        err_summary_box = RoundedRectangle(
            width=6.6, height=2.2, corner_radius=0.18,
            fill_color=CARD_BG, fill_opacity=0.95, stroke_color=RED_C, stroke_width=2.5
        ).move_to([1.55, -0.25, 0])

        err_eq = MathTex(
            r"\text{Reading} = \text{True Value} \pm \Delta x",
            font_size=32,
            color=WHITE,
        ).move_to(err_summary_box.get_center() + UP * 0.3)

        err_sub = Text(
            "A small error always tags along with every measurement.",
            font_size=19,
            color=RED_B,
        ).move_to(err_summary_box.get_center() + DOWN * 0.42)

        merge_arrows = VGroup(
            Arrow(dock_ruler.get_right(), err_summary_box.get_left() +
                  UP * 0.5, color=RED_C, stroke_width=2.5),
            Arrow(dock_watch.get_right(), err_summary_box.get_left(),
                  color=RED_C, stroke_width=2.5),
            Arrow(dock_scale.get_right(), err_summary_box.get_left() +
                  DOWN * 0.5, color=RED_C, stroke_width=2.5),
        )

        self.play(
            Create(merge_arrows),
            FadeIn(err_summary_box, scale=0.95),
            Write(err_eq),
            FadeIn(err_sub),
            run_time=1.5,
        )
        self.wait(5.2)

        # =====================================================================
        # PHẦN 3: SAI SỐ TUYỆT ĐỐI VS. TƯƠNG ĐỐI (0:34.5 – 1:11.0 | 36.5s)
        # =====================================================================
        self.play(
            FadeOut(VGroup(sec2_title, dock_ruler, dock_watch, dock_scale,
                    merge_arrows, err_summary_box, err_eq, err_sub)),
            run_time=0.7,
        )

        sec3_title = Text(
            "Two Ways to Look at an Error",
            font_size=26,
            color=YELLOW_C,
            weight=BOLD,
        ).to_edge(UP, buff=0.38).shift(RIGHT * 1.1)

        split_line = DashedLine(
            [0, 2.35, 0], [0, -3.35, 0], color=SLATE, stroke_width=2
        )

        self.play(FadeIn(sec3_title, shift=DOWN * 0.15),
                  Create(split_line), run_time=0.9)
        # Chờ đọc: "Now, there are two ways to look at that error."
        self.wait(2.4)

        # --- Nửa trái: Absolute Error (0:38.5 – 0:44.5 | 6.0s) ---
        abs_hdr = Text("1. Absolute Error", font_size=24,
                       color=ORANGE, weight=BOLD).move_to([-3.3, 1.85, 0])
        abs_sub = Text("Raw size in physical units", font_size=18,
                       color=GREY_A).next_to(abs_hdr, DOWN, buff=0.12)

        # Thanh kẹp đo đoạn 1 cm phát sáng
        seg_1cm = Line([-4.3, 0.75, 0], [-2.7, 0.75, 0],
                       color=RED_C, stroke_width=7)
        cap_l = Line([-4.3, 0.55, 0], [-4.3, 0.95, 0],
                     color=WHITE, stroke_width=3)
        cap_r = Line([-2.7, 0.55, 0], [-2.7, 0.95, 0],
                     color=WHITE, stroke_width=3)
        abs_val = MathTex(r"|\Delta x| = 1\text{ cm}", font_size=28, color=WHITE).next_to(
            seg_1cm, DOWN, buff=0.22)
        caliper_group = VGroup(seg_1cm, cap_l, cap_r, abs_val)

        self.play(FadeIn(abs_hdr), FadeIn(abs_sub), run_time=0.8)
        self.play(GrowFromCenter(seg_1cm), FadeIn(cap_l),
                  FadeIn(cap_r), Write(abs_val), run_time=1.0)
        self.wait(4.2)

        # --- Nửa phải: Relative Error (0:44.5 – 0:51.5 | 7.0s) ---
        rel_hdr = Text("2. Relative Error", font_size=24,
                       color=TEAL_C, weight=BOLD).move_to([3.3, 1.85, 0])
        rel_sub = Text("Compared to total object size", font_size=18,
                       color=GREY_A).next_to(rel_hdr, DOWN, buff=0.12)

        rel_formula = MathTex(
            r"\frac{|\Delta x|}{|x|} = \frac{\text{Mistake}}{\text{Object Size}}",
            font_size=27,
            color=WHITE,
        ).move_to([3.3, 0.65, 0])

        self.play(FadeIn(rel_hdr), FadeIn(rel_sub), run_time=0.8)
        self.play(Write(rel_formula), run_time=1.2)
        self.wait(5.0)

        # --- Ví dụ 1 (Góc dưới trái): Mặt bàn 60 cm -> 1.7% (0:51.5 – 1:00.5 | 9.0s) ---
        table_c = np.array([-4.75, -1.55, 0])
        table_disc = Circle(
            radius=0.92, fill_color="#92400E", fill_opacity=0.92,
            stroke_color="#F59E0B", stroke_width=2
        ).move_to(table_c)
        table_rad = Arrow(table_c, table_c + RIGHT * 0.92, buff=0, color=WHITE,
                          stroke_width=2.5, max_tip_length_to_length_ratio=0.18)
        table_r_lbl = MathTex(r"60\text{ cm}", font_size=19, color=WHITE).next_to(
            table_rad, UP, buff=0.06)

        # Vành lỗi 1 cm đỏ chớp sáng ở mép bàn
        table_err_arc = Annulus(
            inner_radius=0.92, outer_radius=1.06,
            fill_color=RED_C, fill_opacity=0.85, stroke_width=0
        ).move_to(table_c)

        # Thanh đo phần trăm cho mặt bàn
        t_bar_bg = Rectangle(width=2.3, height=0.24, color=GREY_D,
                             fill_opacity=0.6, stroke_width=1).move_to([-2.15, -1.95, 0])
        t_bar_fill = Rectangle(width=1.55, height=0.24, color=ORANGE, fill_opacity=0.95,
                               stroke_width=0).align_to(t_bar_bg, LEFT).set_y(t_bar_bg.get_y())
        t_stat = VGroup(
            Text("60 cm Tabletop", font_size=19, color=YELLOW_C, weight=BOLD),
            MathTex(r"\frac{1\text{ cm}}{60\text{ cm}} \approx 1.7\%",
                    font_size=24, color=ORANGE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([-2.15, -1.15, 0])

        self.play(
            FadeIn(table_disc), GrowArrow(table_rad), Write(table_r_lbl),
            FadeIn(table_err_arc), FadeIn(t_stat),
            FadeIn(t_bar_bg), GrowFromEdge(t_bar_fill, LEFT),
            run_time=1.8,
        )
        self.play(Indicate(table_err_arc, color=RED_C,
                  scale_factor=1.1), run_time=0.8)
        self.wait(6.4)

        # --- Ví dụ 2 (Góc dưới phải): Sân bóng 100 m -> 0.01% (1:00.5 – 1:11.0 | 10.5s) ---
        pitch_c = np.array([1.75, -1.55, 0])
        pitch_rect = Rectangle(
            width=2.35, height=1.45, fill_color="#15803D", fill_opacity=0.92,
            stroke_color=WHITE, stroke_width=2
        ).move_to(pitch_c)
        pitch_mid = Line(pitch_rect.get_top(),
                         pitch_rect.get_bottom(), color=WHITE, stroke_width=1.5)
        pitch_circle = Circle(radius=0.25, color=WHITE,
                              stroke_width=1.5).move_to(pitch_c)
        pitch_len_lbl = MathTex(r"100\text{ m}", font_size=19, color=WHITE).next_to(
            pitch_rect, DOWN, buff=0.08)

        # Cũng đúng lỗi 1 cm bay sang mép sân bóng và thu nhỏ thành chấm đỏ li ti
        fly_err = seg_1cm.copy()
        pitch_err_dot = Dot(pitch_rect.get_right() +
                            RIGHT * 0.04, color=RED_C, radius=0.05)

        p_bar_bg = Rectangle(width=2.3, height=0.24, color=GREY_D,
                             fill_opacity=0.6, stroke_width=1).move_to([4.65, -1.95, 0])
        p_bar_fill = Rectangle(width=0.06, height=0.24, color=GREEN_C, fill_opacity=0.95,
                               stroke_width=0).align_to(p_bar_bg, LEFT).set_y(p_bar_bg.get_y())
        p_stat = VGroup(
            Text("100 m Football Field", font_size=19,
                 color=GREEN_C, weight=BOLD),
            MathTex(r"\frac{1\text{ cm}}{10{,}000\text{ cm}} = 0.01\%",
                    font_size=22, color=GREEN_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([4.65, -1.15, 0])

        self.play(
            FadeIn(pitch_rect), Create(pitch_mid), Create(
                pitch_circle), Write(pitch_len_lbl),
            ReplacementTransform(fly_err, pitch_err_dot),
            FadeIn(p_stat), FadeIn(p_bar_bg), FadeIn(p_bar_fill),
            run_time=2.0,
        )
        # Chờ đọc hết câu: "Same mistake, but completely different impact."
        self.wait(8.5)

        # =====================================================================
        # PHẦN 4: SƠ ĐỒ LAN TRUYỀN SAI SỐ QUA HÀM SỐ (1:11.0 – 1:30.0 | 19.0s)
        # =====================================================================
        part3_all = VGroup(
            sec3_title, split_line, abs_hdr, abs_sub, caliper_group,
            rel_hdr, rel_sub, rel_formula,
            table_disc, table_rad, table_r_lbl, table_err_arc, t_bar_bg, t_bar_fill, t_stat,
            pitch_rect, pitch_mid, pitch_circle, pitch_len_lbl, pitch_err_dot, p_bar_bg, p_bar_fill, p_stat,
        )
        self.play(FadeOut(part3_all), run_time=0.7)

        sec4_title = Text(
            "How Does Error Propagate Through a Formula?",
            font_size=26,
            color=YELLOW_C,
            weight=BOLD,
        ).to_edge(UP, buff=0.38).shift(RIGHT * 1.35)

        # Hộp Input x ± Δx
        in_lbl = Text("Measured Input", font_size=17, color=GREY_B)
        in_tex = MathTex(r"x \pm \Delta x", font_size=34, color=YELLOW_C)
        in_content = VGroup(in_lbl, in_tex).arrange(DOWN, buff=0.16)
        in_box = SurroundingRectangle(
            in_content, color=YELLOW_C, buff=0.26, corner_radius=0.15,
            fill_color=CARD_BG, fill_opacity=0.95
        )
        node_in = VGroup(in_box, in_content).move_to([-4.35, 0.7, 0])

        self.play(FadeIn(sec4_title, shift=DOWN * 0.15),
                  FadeIn(node_in, shift=RIGHT * 0.25), run_time=1.0)
        # Chờ đọc: "Here's the catch though: we rarely stop at the measured number itself."
        self.wait(4.8)

        # Hộp Hàm số y = f(x) + 2 hình minh họa động bên dưới (1:17.5 – 1:25.0 | 7.5s)
        fn_lbl = Text("Formula", font_size=17, color=GREY_B)
        fn_tex = MathTex(r"y = f(x)", font_size=36, color=TEAL_C)
        fn_content = VGroup(fn_lbl, fn_tex).arrange(DOWN, buff=0.16)
        fn_box = SurroundingRectangle(
            fn_content, color=TEAL_C, buff=0.3, corner_radius=0.15,
            fill_color=CARD_BG, fill_opacity=0.95
        )
        node_fn = VGroup(fn_box, fn_content).move_to([0, 0.7, 0])
        arr1 = Arrow(node_in.get_right(), node_fn.get_left(),
                     buff=0.15, color=WHITE, stroke_width=3)

        self.play(GrowArrow(arr1), FadeIn(node_fn, scale=0.92), run_time=1.1)

        # Thẻ minh họa 1 (dưới trái): Vòng tròn nở diện tích A = πr²
        c_card_bg = RoundedRectangle(width=4.4, height=1.55, corner_radius=0.14, fill_color=CARD_BG,
                                     fill_opacity=0.9, stroke_color=BLUE_C, stroke_width=1.8).move_to([-2.8, -1.75, 0])
        mini_circle = Circle(radius=0.48, fill_color=BLUE_C, fill_opacity=0.45,
                             stroke_color=BLUE_B, stroke_width=2).move_to(c_card_bg.get_left() + RIGHT * 0.85)
        mini_rad = Line(mini_circle.get_center(
        ), mini_circle.get_right(), color=YELLOW_C, stroke_width=2.5)
        c_card_txt = VGroup(
            Text("Area from Radius", font_size=18, color=BLUE_B, weight=BOLD),
            MathTex(r"A = \pi r^2", font_size=26, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).next_to(mini_circle, RIGHT, buff=0.4)

        # Thẻ minh họa 2 (dưới phải): Tia ngắm đo chiều cao cây H = h_e + d tan θ
        t_card_bg = RoundedRectangle(width=4.8, height=1.55, corner_radius=0.14, fill_color=CARD_BG,
                                     fill_opacity=0.9, stroke_color=GREEN_C, stroke_width=1.8).move_to([2.8, -1.75, 0])
        t_ground = Line(t_card_bg.get_left() + RIGHT * 0.4 + DOWN * 0.45,
                        t_card_bg.get_left() + RIGHT * 1.75 + DOWN * 0.45, color=GREY_B, stroke_width=2)
        t_tree = Triangle(fill_color=GREEN_C, fill_opacity=0.85, stroke_width=1).stretch_to_fit_width(
            0.45).stretch_to_fit_height(0.95).move_to(t_ground.get_left() + RIGHT * 0.25 + UP * 0.48)
        t_sight = DashedLine(t_ground.get_right() + UP * 0.12,
                             t_tree.get_top(), color=YELLOW_C, stroke_width=2)
        t_card_txt = VGroup(
            Text("Tree Height from Angle", font_size=18,
                 color=GREEN_B, weight=BOLD),
            MathTex(r"H = h_e + d\tan\theta", font_size=24, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).next_to(t_ground, RIGHT, buff=0.35).shift(UP * 0.45)

        self.play(
            FadeIn(c_card_bg), GrowFromCenter(
                mini_circle), Create(mini_rad), FadeIn(c_card_txt),
            FadeIn(t_card_bg), Create(t_ground), FadeIn(
                t_tree), Create(t_sight), FadeIn(t_card_txt),
            run_time=1.6,
        )
        # Chờ đọc: "...to compute something else, like an area of a radius or height of a tree from an angle."
        self.wait(4.8)

        # Hộp Output y ± Δy = ? bật sáng (1:25.0 – 1:30.0 | 5.0s)
        out_lbl = Text("Computed Output", font_size=17, color=GREY_B)
        out_tex = MathTex(r"y \pm \Delta y = \;?", font_size=34, color=RED_B)
        out_content = VGroup(out_lbl, out_tex).arrange(DOWN, buff=0.16)
        out_box = SurroundingRectangle(
            out_content, color=RED_C, buff=0.26, corner_radius=0.15,
            fill_color=CARD_BG, fill_opacity=0.95
        )
        node_out = VGroup(out_box, out_content).move_to([4.35, 0.7, 0])
        arr2 = Arrow(node_fn.get_right(), node_out.get_left(),
                     buff=0.15, color=WHITE, stroke_width=3)

        self.play(
            Indicate(in_tex, color=RED_C, scale_factor=1.15),
            GrowArrow(arr2),
            FadeIn(node_out, scale=1.08),
            run_time=1.5,
        )
        self.play(Indicate(out_tex, color=YELLOW_C,
                  scale_factor=1.15), run_time=1.0)
        # Chờ đọc hết câu hỏi cuối: "So if x is uncertain by a tiny amount, how uncertain does y become?"
        self.wait(2.5)
