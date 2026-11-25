from manim import *
import numpy as np


class Scene02(Scene):
    def construct(self):
        # Bảng màu đồng bộ toàn bộ dự án
        self.camera.background_color = "#0F172A"
        SLATE = "#64748B"
        CARD_BG = "#1E293B"

        # Tự động ghép file tiếng khi render nháp (thêm dấu # ở đầu dòng khi render final)
        self.add_sound("Recordings/Scene02.wav")

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
            "The Core Idea: Local Linearization",
            font_size=26,
            color=YELLOW_C,
            weight=BOLD,
        ).to_edge(UP, buff=0.38).shift(RIGHT * 1.2)

        # =====================================================================
        # HÀM SỐ & TIẾP TUYẾN MẪU CHO MÔ PHỎNG ZOOM
        # f(x) = 0.22x^2 + 0.35x + 0.9 tại a = 1.5 -> f(1.5) = 1.92, f'(1.5) = 1.01
        # =====================================================================
        a_val = 1.5
        fa_val = 1.92
        slope_a = 1.01

        def f(x):
            return 0.22 * (x**2) + 0.35 * x + 0.9

        def L(x):
            return fa_val + slope_a * (x - a_val)

        zoom_tracker = ValueTracker(1.0)
        axes_center = np.array([-2.25, -0.35, 0])

        def get_axes():
            z = zoom_tracker.get_value()
            dx = 2.6 / z
            dy = 1.8 / z
            return Axes(
                x_range=[a_val - dx, a_val + dx, dx / 2.0],
                y_range=[fa_val - dy, fa_val + dy, dy / 2.0],
                x_length=6.1,
                y_length=4.4,
                axis_config={
                    "color": GREY_B,
                    "stroke_width": 1.8,
                    "include_ticks": True,
                    "tick_size": 0.06,
                    "include_tip": False,
                },
            ).move_to(axes_center)

        dyn_axes = always_redraw(get_axes)

        dyn_curve = always_redraw(
            lambda: get_axes().plot(
                f,
                x_range=[
                    a_val - 2.55 / zoom_tracker.get_value(),
                    a_val + 2.55 / zoom_tracker.get_value(),
                ],
                color=BLUE_C,
                stroke_width=3.8,
            )
        )

        dyn_tangent = always_redraw(
            lambda: get_axes().plot(
                L,
                x_range=[
                    a_val - 2.55 / zoom_tracker.get_value(),
                    a_val + 2.55 / zoom_tracker.get_value(),
                ],
                color=YELLOW_C,
                stroke_width=3.2,
            )
        )

        # Điểm neo P(a, f(a)) luôn nằm chính giữa khung đồ thị khi zoom
        anchor_dot = Dot(axes_center, color=WHITE, radius=0.075)
        anchor_ring = Circle(radius=0.14, color=YELLOW_C,
                             stroke_width=2).move_to(axes_center)
        anchor_lbl = MathTex(r"(a, f(a))", font_size=22, color=WHITE).next_to(
            anchor_dot, UL, buff=0.12
        )

        # =====================================================================
        # PHẦN 1: THAY ĐƯỜNG CONG PHỨC TẠP BẰNG TIẾP TUYẾN (0:00 – 0:11.0 | 11.0s)
        # =====================================================================
        # Thẻ đại số rườm rà bên phải bị gạch bỏ
        messy_lines = VGroup(
            Text("Messy Exact Algebra:", font_size=20, color=RED_B, weight=BOLD),
            MathTex(
                r"\Delta y = f(a + \Delta x) - f(a)",
                font_size=24,
                color=GREY_A,
            ),
            MathTex(
                r"= \sqrt{(a+\Delta x)^3 + \sin(a+\Delta x)} - \dots",
                font_size=19,
                color=GREY_B,
            ),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        messy_box = SurroundingRectangle(
            messy_lines,
            color=RED_C,
            buff=0.22,
            corner_radius=0.14,
            fill_color=CARD_BG,
            fill_opacity=0.92,
        )
        messy_card = VGroup(messy_box, messy_lines).move_to([3.55, 0.85, 0])

        self.play(
            FadeIn(sec_title, shift=DOWN * 0.15),
            Create(dyn_axes),
            Create(dyn_curve),
            FadeIn(messy_card, shift=LEFT * 0.2),
            run_time=1.5,
        )
        # Chờ đọc: "Uh, to answer that without doing messy algebra every time,"
        self.wait(2.7)

        # Gạch chéo thẻ đại số phức tạp & vẽ đường tiếp tuyến vàng mượt mà
        cross_line = Line(
            messy_card.get_corner(DL) + UR * 0.12,
            messy_card.get_corner(UR) + DL * 0.12,
            color=RED_C,
            stroke_width=4,
        )

        simple_lines = VGroup(
            Text("Calculus Shortcut:", font_size=21, color=TEAL_C, weight=BOLD),
            Text("Replace a complicated curve", font_size=19, color=WHITE),
            Text("with its tangent line.", font_size=19,
                 color=YELLOW_C, weight=BOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        simple_box = SurroundingRectangle(
            simple_lines,
            color=TEAL_C,
            buff=0.24,
            corner_radius=0.14,
            fill_color=CARD_BG,
            fill_opacity=0.92,
        )
        simple_card = VGroup(
            simple_box, simple_lines).move_to([3.55, -1.15, 0])

        self.play(
            Create(cross_line),
            FadeIn(anchor_dot),
            Create(anchor_ring),
            Write(anchor_lbl),
            Create(dyn_tangent),
            FadeIn(simple_card, shift=UP * 0.2),
            run_time=1.8,
        )
        # Chờ đọc: "...calculus gives us a wonderfully simple idea: replace a complicated curve with its tangent line."
        self.wait(5.0)

        # =====================================================================
        # PHẦN 2: ZOOM-IN SÁT ĐIỂM a — ĐƯỜNG CONG DUỖI PHẲNG (0:11.0 – 0:23.0 | 12.0s)
        # =====================================================================
        self.play(
            FadeOut(VGroup(messy_card, cross_line, simple_card)),
            run_time=0.6,
        )

        # Vòng kính lúp phóng đại quanh P(a, f(a))
        zoom_scope = Circle(
            radius=1.65, color=YELLOW_C, stroke_width=3, stroke_opacity=0.85
        ).move_to(axes_center)
        zoom_badge = VGroup(
            Text("Zooming in around x = a", font_size=21,
                 color=YELLOW_C, weight=BOLD),
            MathTex(r"\text{Magnification: } 1\times \longrightarrow 8.5\times",
                    font_size=22, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        zoom_box = SurroundingRectangle(
            zoom_badge, color=YELLOW_C, buff=0.22, corner_radius=0.14,
            fill_color=CARD_BG, fill_opacity=0.92
        )
        zoom_card = VGroup(zoom_box, zoom_badge).move_to([3.55, 0.75, 0])

        self.play(Create(zoom_scope), FadeIn(
            zoom_card, shift=LEFT * 0.2), run_time=0.9)

        # Phóng đại mượt mà từ 1x lên 8.5x -> đường cong xanh duỗi thẳng trùng với tiếp tuyến vàng!
        self.play(
            zoom_tracker.animate.set_value(8.5),
            zoom_scope.animate.scale(1.25).set_stroke(TEAL_C),
            run_time=4.5,
            rate_func=smooth,
        )

        flat_lines = VGroup(
            Text("Local Linearity:", font_size=22, color=TEAL_C, weight=BOLD),
            Text("The curve flattens out and", font_size=19, color=WHITE),
            Text("merges with its tangent!", font_size=19,
                 color=GREEN_C, weight=BOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        flat_box = SurroundingRectangle(
            flat_lines, color=GREEN_C, buff=0.22, corner_radius=0.14,
            fill_color=CARD_BG, fill_opacity=0.92
        )
        flat_card = VGroup(flat_box, flat_lines).move_to([3.55, -1.1, 0])

        self.play(FadeIn(flat_card, shift=UP * 0.15), run_time=1.0)
        # Chờ đọc hết câu: "...until it looks almost indistinguishable from a straight line — its tangent."
        self.wait(5.0)

        # =====================================================================
        # PHẦN 3: SO SÁNH Δy (ĐƯỜNG CONG) VS dy (TIẾP TUYẾN) & KHE ĐỎ (0:23.0 – 0:42.8 | 19.8s)
        # =====================================================================
        self.play(
            FadeOut(VGroup(zoom_scope, zoom_card, flat_card, anchor_ring)),
            zoom_tracker.animate.set_value(1.65),
            run_time=1.8,
            rate_func=smooth,
        )

        # Cố định hệ trục ở mức zoom 1.65 để dựng các đoạn thẳng đo đạc sắc nét
        fixed_ax = get_axes()
        fixed_curve = fixed_ax.plot(
            f, x_range=[0.0, 3.0], color=BLUE_C, stroke_width=3.8)
        fixed_tangent = fixed_ax.plot(
            L, x_range=[0.0, 3.0], color=YELLOW_C, stroke_width=3.2)

        self.remove(dyn_axes, dyn_curve, dyn_tangent)
        self.add(fixed_ax, fixed_curve, fixed_tangent, anchor_dot)

        b_val = 2.30  # a + Δx (với Δx = 0.80)
        pt_a = fixed_ax.c2p(a_val, fa_val)
        pt_b_base = fixed_ax.c2p(b_val, fa_val)
        pt_b_tan = fixed_ax.c2p(b_val, L(b_val))
        pt_b_curve = fixed_ax.c2p(b_val, f(b_val))

        # Đường đáy ngang Δx từ a đến a + Δx
        dx_line = Line(pt_a, pt_b_base, color=WHITE, stroke_width=2.8)
        dx_lbl = MathTex(r"\Delta x", font_size=24, color=WHITE).next_to(
            dx_line, DOWN, buff=0.12)
        vert_guide = DashedLine(
            fixed_ax.c2p(b_val, 0.95), pt_b_curve + UP * 0.25,
            color=GREY_B, stroke_width=1.6
        )
        tick_a_lbl = MathTex(r"a", font_size=22, color=GREY_A).move_to(
            [pt_a[0], -2.35, 0])
        tick_b_lbl = MathTex(r"a+\Delta x", font_size=22,
                             color=WHITE).move_to([pt_b_base[0], -2.35, 0])

        self.play(
            Create(dx_line),
            Write(dx_lbl),
            Create(vert_guide),
            FadeIn(tick_a_lbl),
            FadeIn(tick_b_lbl),
            run_time=1.5,
        )
        # Chờ đọc: "Now let's compare two rises when x shifts from a to a + Δx."
        self.wait(1.7)

        # --- 3A. Độ tăng thực Δy dọc theo đường cong (0:28.0 – 0:32.2 | 4.2s) ---
        curve_tracer = Dot(pt_a, color=TEAL_C, radius=0.08)
        dy_true_bar = Line(
            pt_b_base + RIGHT * 0.14,
            pt_b_curve + RIGHT * 0.14,
            color=TEAL_C,
            stroke_width=5,
        )
        dy_true_lbl = MathTex(r"\Delta y", font_size=25, color=TEAL_C).next_to(
            dy_true_bar, RIGHT, buff=0.12
        )

        card_delta_y = VGroup(
            SurroundingRectangle(
                Text("True Climb (Curve):  Δy = f(a+Δx) − f(a)", font_size=18),
                color=TEAL_C, buff=0.2, corner_radius=0.12, fill_color=CARD_BG, fill_opacity=0.92
            ),
            VGroup(
                Text("True Climb (Curve):", font_size=18,
                     color=TEAL_C, weight=BOLD),
                MathTex(r"\Delta y = f(a + \Delta x) - f(a)",
                        font_size=22, color=WHITE),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.1),
        ).move_to([3.65, 1.55, 0])

        self.play(
            MoveAlongPath(curve_tracer, fixed_ax.plot(
                f, x_range=[a_val, b_val])),
            GrowFromEdge(dy_true_bar, DOWN),
            Write(dy_true_lbl),
            FadeIn(card_delta_y, shift=LEFT * 0.2),
            run_time=1.5,
        )
        # Chờ đọc: "The true change in y is the increment Δy — that's the actual climb along the curve."
        self.wait(2.7)

        # --- 3B. Vi phân dy dọc theo tiếp tuyến (0:32.2 – 0:37.2 | 5.0s) ---
        tan_tracer = Dot(pt_a, color=YELLOW_C, radius=0.08)
        dy_diff_bar = Line(
            pt_b_base + LEFT * 0.14,
            pt_b_tan + LEFT * 0.14,
            color=YELLOW_C,
            stroke_width=5,
        )
        dy_diff_lbl = MathTex(r"dy", font_size=25, color=YELLOW_C).next_to(
            dy_diff_bar, LEFT, buff=0.12
        )

        card_dy = VGroup(
            SurroundingRectangle(
                Text("Tangent Climb (Diff):  dy = f'(a)·Δx", font_size=18),
                color=YELLOW_C, buff=0.2, corner_radius=0.12, fill_color=CARD_BG, fill_opacity=0.92
            ),
            VGroup(
                Text("Tangent Climb (Differential):",
                     font_size=18, color=YELLOW_C, weight=BOLD),
                MathTex(r"dy = f'(a)\,\Delta x", font_size=24, color=WHITE),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.1),
        ).move_to([3.65, 0.05, 0])

        self.play(
            MoveAlongPath(tan_tracer, fixed_ax.plot(
                L, x_range=[a_val, b_val])),
            GrowFromEdge(dy_diff_bar, DOWN),
            Write(dy_diff_lbl),
            FadeIn(card_dy, shift=LEFT * 0.2),
            run_time=1.5,
        )
        # Chờ đọc: "The differential dy = f'(a)Δx is the climb along the tangent line."
        self.wait(3.5)

        # --- 3C. Khe sai số màu đỏ giữa đường cong và tiếp tuyến (0:37.2 – 0:42.8 | 5.6s) ---
        red_gap_bar = Line(
            pt_b_tan, pt_b_curve, color=RED_C, stroke_width=7
        )
        gap_glow = SurroundingRectangle(
            red_gap_bar, color=RED_C, buff=0.08, corner_radius=0.06,
            fill_color=RED_C, fill_opacity=0.35
        )
        gap_ptr = Arrow(
            pt_b_curve + UP * 0.55 + LEFT * 0.95,
            red_gap_bar.get_center() + LEFT * 0.12,
            buff=0,
            color=RED_C,
            stroke_width=2.8,
            max_tip_length_to_length_ratio=0.25,
        )
        gap_tag = Text(
            "Approximation Error", font_size=18, color=RED_B, weight=BOLD
        ).next_to(gap_ptr.get_start(), UP, buff=0.08)

        card_gap = VGroup(
            SurroundingRectangle(
                Text("Red Gap = |Δy − dy| (Shortcut price)", font_size=18),
                color=RED_C, buff=0.2, corner_radius=0.12, fill_color=CARD_BG, fill_opacity=0.92
            ),
            VGroup(
                Text("Approximation Gap:", font_size=18,
                     color=RED_B, weight=BOLD),
                MathTex(r"\text{Error} = |\Delta y - dy|",
                        font_size=22, color=WHITE),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.1),
        ).move_to([3.65, -1.45, 0])

        self.play(
            GrowFromEdge(red_gap_bar, DOWN),
            FadeIn(gap_glow),
            GrowArrow(gap_ptr),
            FadeIn(gap_tag),
            FadeIn(card_gap, shift=LEFT * 0.2),
            run_time=1.5,
        )
        self.play(Indicate(gap_glow, color=RED_C,
                  scale_factor=1.25), run_time=0.9)
        # Chờ đọc: "That tiny red gap between them is the price we pay for using a straight-line shortcut."
        self.wait(3.2)

        # =====================================================================
        # PHẦN 4: CÔNG THỨC TUYẾN TÍNH HÓA & 3 GIẢ THIẾT AN TOÀN (0:42.8 – 0:56.0 | 13.2s)
        # =====================================================================
        self.play(
            FadeOut(VGroup(card_delta_y, card_dy, card_gap)),
            run_time=0.5,
        )

        # Thẻ công thức Linearization L(x)
        lin_lines = VGroup(
            Text("Linearization Formula:", font_size=19,
                 color=YELLOW_C, weight=BOLD),
            MathTex(
                r"L(x) = f(a) + f'(a)(x - a)",
                font_size=25,
                color=WHITE,
            ),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        lin_box = SurroundingRectangle(
            lin_lines, color=YELLOW_C, buff=0.22, corner_radius=0.14,
            fill_color=CARD_BG, fill_opacity=0.95
        )
        lin_card = VGroup(lin_box, lin_lines).move_to([3.65, 1.55, 0])

        self.play(FadeIn(lin_card, shift=DOWN * 0.15), run_time=1.0)
        # Chờ đọc: "That tangent line gives us our linearization: L(x) = f(a) + f'(a)(x - a)."
        self.wait(3.5)

        # 3 Giả thiết an toàn bật lên lần lượt đúng nhịp
        hyp_title = Text(
            "3 Hypotheses for Safe Use:", font_size=19, color=TEAL_C, weight=BOLD
        ).move_to([3.65, 0.35, 0], aligned_edge=LEFT).set_x(3.65)

        def make_hyp_pill(num_str, tex_str, accent_color):
            badge = Circle(radius=0.18, fill_color=accent_color,
                           fill_opacity=1, stroke_width=0)
            num = Text(num_str, font_size=16, color="#0F172A",
                       weight=BOLD).move_to(badge.get_center())
            txt = MathTex(tex_str, font_size=21, color=WHITE)
            row = VGroup(VGroup(badge, num), txt).arrange(RIGHT, buff=0.2)
            bg = RoundedRectangle(
                width=5.1, height=0.58, corner_radius=0.1,
                fill_color=CARD_BG, fill_opacity=0.92, stroke_color=accent_color, stroke_width=1.5
            )
            row.align_to(bg, LEFT).shift(RIGHT * 0.2)
            return VGroup(bg, row)

        h1 = make_hyp_pill(
            "1", r"f \text{ is differentiable near } a", TEAL_C).move_to([3.65, -0.3, 0])
        h2 = make_hyp_pill(
            "2", r"\Delta x \text{ is sufficiently small}", BLUE_C).move_to([3.65, -1.05, 0])
        h3 = make_hyp_pill(
            "3", r"f(a) \neq 0 \text{ (for relative error)}", ORANGE).move_to([3.65, -1.8, 0])

        self.play(FadeIn(hyp_title), run_time=0.6)
        self.play(FadeIn(h1, shift=LEFT * 0.2), run_time=0.9)
        self.wait(1.1)
        self.play(FadeIn(h2, shift=LEFT * 0.2), run_time=0.9)
        self.wait(1.1)
        self.play(FadeIn(h3, shift=LEFT * 0.2), run_time=0.9)
        # Chờ đọc hết câu cuối cùng
        self.wait(2.7)
