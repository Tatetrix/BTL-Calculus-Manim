"""
Calculus 1 - Group 4 CC01
Differential, Linearization and Error Propagation in Measurement
Manim Community Edition (v0.18+). Case study 2 (ruler drop) is removed.

Render a single scene (preview, low quality):
    manim -pql calculus_manim.py S02_Differential
Render everything in high quality (1080p):
    manim -qh calculus_manim.py S01_Intro S02_Differential S03_AbsoluteError \
        S04_RelativeError S05_Remainder S06_Counterexamples S07_GlassTable \
        S08_CliffJump S09_Verification S10_Conclusion
Then join the clips + add voice-over in CapCut / DaVinci / ffmpeg.
"""
from manim import *
import numpy as np

BG = "#0f1117"


class Base(Scene):
    def setup(self):
        self.camera.background_color = BG

    def heading(self, text, color=YELLOW):
        h = Text(text, font_size=36, color=color).to_edge(UP, buff=0.4)
        self.play(FadeIn(h, shift=DOWN * 0.3))
        return h

    def clear(self):
        self.play(*[FadeOut(m) for m in self.mobjects])


# --------------------------------------------------------------------------
# 1. INTRO  (~45 s)
# --------------------------------------------------------------------------
class S01_Intro(Base):
    def construct(self):
        title = Text(
            "Differentials, Linearization\nand Error Propagation", font_size=52)
        sub = Text("Calculus 1  ·  Group 4 – CC01", font_size=28, color=GREY_B)
        sub.next_to(title, DOWN, buff=0.5)
        self.play(Write(title), run_time=2)
        self.play(FadeIn(sub))
        self.wait(1.5)
        self.clear()

        # measurement -> formula -> propagated error
        x = MathTex(r"x = a \pm \Delta x", font_size=60)
        arrow = MathTex(r"\xrightarrow{\;y=f(x)\;}", font_size=60)
        y = MathTex(r"y = f(x) \;\Rightarrow\; \Delta y = {?}", font_size=60)
        row = VGroup(x, arrow, y).arrange(RIGHT, buff=0.4).scale(0.8)
        self.play(Write(x))
        self.play(GrowFromCenter(arrow))
        self.play(Write(y))
        q = Text("How large can the error in y be, in absolute and relative terms?",
                 font_size=28, color=YELLOW).next_to(row, DOWN, buff=1)
        self.play(FadeIn(q, shift=UP * 0.3))
        self.wait(1.5)
        ans = MathTex(r"dy = f'(a)\,\Delta x", font_size=64,
                      color=GREEN).next_to(q, DOWN, buff=0.8)
        self.play(Write(ans))
        self.wait(2)
        self.clear()


# --------------------------------------------------------------------------
# 2. DEFINITIONS + LEMMA  (~1 min 15 s)
# --------------------------------------------------------------------------
class S02_Differential(Base):
    def construct(self):
        self.heading("Increment  Δy  vs  Differential  dy")
        def f(t): return t ** 2
        def fp(t): return 2 * t
        a = 1.0

        ax = Axes(x_range=[0, 3, 1], y_range=[0, 9, 3], x_length=6, y_length=4.6,
                  tips=False, axis_config={"include_numbers": True, "font_size": 22})
        ax.to_edge(LEFT, buff=0.7).shift(DOWN * 0.4)
        curve = ax.plot(f, x_range=[0, 3], color=BLUE)
        tangent = ax.plot(lambda t: f(a) + fp(a) * (t - a),
                          x_range=[0.2, 2.9], color=YELLOW)
        c_lab = MathTex("f(x)=x^2", color=BLUE, font_size=30).next_to(
            ax.c2p(2.5, 6.25), LEFT)
        t_lab = MathTex("L(x)=f(a)+f'(a)(x-a)", color=YELLOW,
                        font_size=26).next_to(ax.c2p(2.0, 3), DR, buff=0.1)
        self.play(Create(ax), Create(curve), FadeIn(c_lab))
        self.play(Create(tangent), FadeIn(t_lab))

        dx = ValueTracker(1.0)

        def geometry():
            x1 = a + dx.get_value()
            p = ax.c2p(a, f(a))
            base = ax.c2p(x1, f(a))
            on_tan = ax.c2p(x1, f(a) + fp(a) * (x1 - a))
            on_curve = ax.c2p(x1, f(x1))
            return VGroup(
                Line(p, on_curve, color=GREEN,
                     stroke_width=3),           # secant
                DashedLine(p, base, color=GREY),
                Line(base, on_tan, color=YELLOW, stroke_width=7),         # dy
                Line(on_tan, on_curve, color=RED, stroke_width=7),        # gap
                Dot(p, radius=0.07), Dot(on_curve, color=RED, radius=0.07),
            )

        geo = always_redraw(geometry)
        self.play(FadeIn(geo))

        legend = VGroup(
            MathTex(r"dy = f'(a)\,dx", color=YELLOW),
            MathTex(r"\Delta y = f(a+\Delta x)-f(a)", color=RED),
            MathTex(r"\Delta y = dy + \varepsilon\,\Delta x", color=WHITE),
            MathTex(
                r"\varepsilon \to 0 \ \text{as}\ \Delta x \to 0", color=GREEN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).scale(0.85).to_edge(RIGHT, buff=0.6).shift(UP * 0.5)
        for line in legend:
            self.play(Write(line), run_time=1.2)
        self.wait(0.5)

        # secant -> tangent, gap shrinks
        self.play(dx.animate.set_value(0.1), run_time=5, rate_func=smooth)
        note = Text("The gap shrinks faster than Δx", font_size=26, color=RED)
        note.next_to(legend, DOWN, buff=0.6)
        self.play(FadeIn(note))
        self.wait(1.5)

        # numeric example from the report
        self.clear()
        ex = MathTex(r"f(x)=\ln(x^2+3),\quad x: 4 \to 4.01", font_size=40)
        l1 = MathTex(
            r"\Delta y = \ln 19.0801 - \ln 19 \approx 0.004207", font_size=40)
        l2 = MathTex(
            r"dy = \tfrac{8}{19}(0.01) \approx 0.004211", font_size=40, color=YELLOW)
        l3 = Text("Only ~0.1% apart - and dy needs one derivative only.",
                  font_size=28, color=GREEN)
        VGroup(ex, l1, l2, l3).arrange(DOWN, buff=0.5)
        for m in (ex, l1, l2, l3):
            self.play(Write(m) if not isinstance(m, Text) else FadeIn(m))
        self.wait(2)
        self.clear()


# --------------------------------------------------------------------------
# 3. THEOREM 1 - ABSOLUTE ERROR  (~1 min 15 s)
# --------------------------------------------------------------------------
class S03_AbsoluteError(Base):
    def construct(self):
        self.heading("Theorem 1 - Absolute-error law")
        law = MathTex(r"\Delta y \approx |f'(a)|\cdot \Delta x",
                      font_size=72, color=GREEN)
        box = SurroundingRectangle(law, color=GREEN, buff=0.25)
        self.play(Write(law))
        self.play(Create(box))
        self.play(VGroup(law, box).animate.scale(0.6).to_edge(UP, buff=1.3))

        steps = VGroup(
            MathTex(
                r"1.\ \ \text{Actual error: } \Delta y = f(a\pm\Delta x)-f(a)"),
            MathTex(
                r"2.\ \ \text{Lemma: } \Delta y \approx dy = f'(a)\,(\pm\Delta x)"),
            MathTex(r"3.\ \ \text{Worst case} = \text{largest magnitude}"),
            MathTex(
                r"4.\ \ \Delta x>0 \Rightarrow \Delta y \approx |f'(a)|\,\Delta x \quad\blacksquare"),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).scale(0.75).next_to(law, DOWN, buff=0.6)
        for s in steps:
            self.play(Write(s), run_time=1.5)
            self.wait(0.6)
        self.wait(1)
        self.clear()

        self.heading("Example", color=BLUE)
        ex = VGroup(
            MathTex(r"f(x)=x^4-2x^2+5,\quad a=2.00,\quad \Delta x=0.02"),
            MathTex(
                r"\delta x = 1\%\ \text{(small)},\ f \text{ differentiable}"),
            MathTex(r"f'(x)=4x^3-4x \Rightarrow f'(2)=24"),
            MathTex(r"\Delta y \approx 24 \times 0.02 = 0.48", color=YELLOW),
            MathTex(
                r"\text{Exact: } f(2.02)-f(2)\approx 0.4889", color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).scale(0.9)
        for m in ex:
            self.play(Write(m), run_time=1.3)
        self.wait(2)
        self.clear()


# --------------------------------------------------------------------------
# 4. THEOREM 2 - RELATIVE ERROR + POWER LAW  (~1 min 15 s)
# --------------------------------------------------------------------------
class S04_RelativeError(Base):
    def construct(self):
        self.heading("Theorem 2 - Relative-error law")
        law = MathTex(r"\delta y \approx \big|d(\ln|y|)\big| = \left|\frac{f'(a)}{f(a)}\right|\Delta x",
                      font_size=60, color=GREEN)
        self.play(Write(law))
        self.play(law.animate.scale(0.75).shift(UP * 1.2))

        why = VGroup(
            MathTex(r"\delta y = \Delta y / |f(a)| \quad (f(a)\neq 0)"),
            MathTex(
                r"\tfrac{d}{dx}\ln|f(x)| = \tfrac{f'(x)}{f(x)} \;\Rightarrow\; d(\ln|y|)=\tfrac{f'(a)}{f(a)}dx"),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).scale(0.8).next_to(law, DOWN, buff=0.6)
        for w in why:
            self.play(Write(w))
        self.wait(1.5)
        self.clear()

        self.heading("Corollary - power law", color=BLUE)
        pw = MathTex(r"y=kx^n \;\Rightarrow\; \ln y=\ln k + n\ln x \;\Rightarrow\; \delta y \approx |n|\,\delta x",
                     font_size=48, color=YELLOW)
        self.play(Write(pw))
        self.wait(1)

        ex1 = VGroup(
            MathTex(r"y=5x^3,\ x=4.00,\ \delta x=1.5\%"),
            MathTex(r"\delta y \approx 3\times 1.5\% = 4.5\%", color=YELLOW),
        ).arrange(DOWN, buff=0.35).scale(0.9)
        ex2 = VGroup(
            MathTex(r"y=x^3,\ x=2,\ \Delta x=0.01"),
            MathTex(r"\text{Differential: } 3(0.01)/2 = 1.5\%", color=YELLOW),
            MathTex(r"\text{Exact: } 0.120601/8 \approx 1.51\%", color=GREY_B),
        ).arrange(DOWN, buff=0.3).scale(0.9)
        VGroup(ex1, ex2).arrange(RIGHT, buff=1.2).next_to(pw, DOWN, buff=1)
        self.play(FadeIn(ex1, shift=UP * 0.2))
        self.play(FadeIn(ex2, shift=UP * 0.2))
        rule = Text("Area ~ r²  →  the relative error doubles",
                    font_size=28, color=GREEN)
        rule.to_edge(DOWN, buff=0.7)
        self.play(FadeIn(rule))
        self.wait(2)
        self.clear()


# --------------------------------------------------------------------------
# 5. THEOREM 3 - REMAINDER BOUND  (~1 min 15 s)
# --------------------------------------------------------------------------
class S05_Remainder(Base):
    def construct(self):
        self.heading("Theorem 3 - How big is the neglected term?")
        thm = MathTex(r"|f''|\le M \text{ on } I \;\Rightarrow\; |\Delta y - dy| \le \frac{M}{2}(\Delta x)^2",
                      font_size=52, color=GREEN)
        self.play(Write(thm))
        self.play(thm.animate.scale(0.8).shift(UP * 1.4))

        proof = VGroup(
            MathTex(
                r"R(h)=f(a+h)-f(a)-f'(a)h,\quad R(0)=0,\ R(\Delta x)=\Delta y - dy"),
            MathTex(r"g(h)=(\Delta x)^2R(h)-h^2R(\Delta x),\quad g(0)=g(\Delta x)=0"),
            MathTex(
                r"\text{Rolle: } \exists c_1:\ (\Delta x)^2R'(c_1)=2c_1R(\Delta x)"),
            MathTex(r"\text{MVT: } R'(c_1)=f''(a+c_2)\,c_1"),
            MathTex(
                r"R(\Delta x)=\tfrac12 f''(a+c_2)(\Delta x)^2 \quad\blacksquare", color=YELLOW),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).scale(0.62).next_to(thm, DOWN, buff=0.5)
        for p in proof:
            self.play(Write(p), run_time=1.4)
        self.wait(1.5)
        self.clear()

        # table for f(x)=x^2, a=1
        self.heading(
            "Linearization:  f(x)=x²  at  a=1,   L(x)=2x−1", color=BLUE)
        tab = MathTable(
            [["0.8", "0.9", "0.98", "1", "1.05", "1.1", "1.2"],
             ["0.6", "0.8", "0.96", "1", "1.1", "1.2", "1.4"],
             ["0.64", "0.81", "0.9604", "1", "1.1025", "1.21", "1.44"],
             ["0.04", "0.01", "0.0004", "0", "0.0025", "0.01", "0.04"]],
            row_labels=[MathTex("x"), MathTex("L(x)"), MathTex(
                "f(x)"), MathTex(r"|f-L|=(x-1)^2")],
            include_outer_lines=True,
        ).scale(0.5).shift(UP * 0.3)
        self.play(Create(tab), run_time=3)
        t = Text("f is convex → the tangent lies below the curve; error ~ (x−a)²",
                 font_size=26, color=YELLOW).next_to(tab, DOWN, buff=0.6)
        self.play(FadeIn(t))
        self.wait(1.5)
        self.clear()

        # sqrt example
        ex = VGroup(
            MathTex(r"f(x)=\sqrt{x},\ a=4,\ \Delta x=0.1,\ M=\tfrac1{32}"),
            MathTex(
                r"\text{Bound: } \tfrac1{64}(0.1)^2 \approx 1.563\times10^{-4}", color=YELLOW),
            MathTex(
                r"\text{Actual: } |\Delta y-dy| \approx 1.543\times10^{-4}\ \ \checkmark", color=GREEN),
            MathTex(
                r"\Delta x \to \Delta x/2 \;\Rightarrow\; \text{error} \to \text{error}/4", color=BLUE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).scale(0.9)
        for e in ex:
            self.play(Write(e), run_time=1.4)
        self.wait(2)
        self.clear()


# --------------------------------------------------------------------------
# 6. COUNTEREXAMPLES  (~1 min 15 s)
# --------------------------------------------------------------------------
class S06_Counterexamples(Base):
    def construct(self):
        self.heading("No hypothesis can be dropped", color=RED)

        # C1: sin x, small Δx
        sub = Text("C1 - (H2) fails: Δx not small", font_size=28,
                   color=ORANGE).next_to(self.mobjects[0], DOWN, buff=0.3)
        self.play(FadeIn(sub))
        ax = Axes(x_range=[-0.3, 1.5, 0.5], y_range=[-0.3, 1.3, 0.5], x_length=6, y_length=4,
                  tips=False, axis_config={"include_numbers": True, "font_size": 20}).shift(LEFT * 3 + DOWN * 0.8)
        s = ax.plot(np.sin, x_range=[-0.2, 1.5], color=BLUE)
        tan = ax.plot(lambda t: t, x_range=[-0.2, 1.3], color=YELLOW)
        self.play(Create(ax), Create(s), Create(tan))
        gap1 = Line(ax.c2p(0.1, np.sin(0.1)), ax.c2p(
            0.1, 0.1), color=RED, stroke_width=6)
        gap2 = Line(ax.c2p(1, np.sin(1)), ax.c2p(
            1, 1), color=RED, stroke_width=6)
        txt = VGroup(
            MathTex(
                r"\Delta x=0.1:\ dy=0.1,\ \Delta y\approx0.0998\ \ (0.17\%)", color=GREEN),
            MathTex(
                r"\Delta x=1:\ dy=1,\ \Delta y\approx0.8415\ \ (\approx19\%)", color=RED),
            MathTex(
                r"|\Delta y - dy|\le \tfrac12(\Delta x)^2:\ 0.005 \text{ vs } 0.5"),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).scale(0.65).to_edge(RIGHT, buff=0.4)
        self.play(Create(gap1), Write(txt[0]))
        self.play(Create(gap2), Write(txt[1]))
        self.play(Write(txt[2]))
        self.wait(2)
        self.play(*[FadeOut(m)
                  for m in self.mobjects if m is not self.mobjects[0]])

        # C2: |x|
        sub = Text("C2 - (H1) fails: not differentiable", font_size=28,
                   color=ORANGE).next_to(self.mobjects[0], DOWN, buff=0.3)
        self.play(FadeIn(sub))
        ax2 = Axes(x_range=[-2, 2, 1], y_range=[0, 2, 1], x_length=5,
                   y_length=3.2, tips=False).shift(LEFT * 3 + DOWN * 0.8)
        left = ax2.plot(lambda t: -t, x_range=[-2, 0], color=BLUE)
        right = ax2.plot(lambda t: t, x_range=[0, 2], color=YELLOW)
        self.play(Create(ax2), Create(left), Create(right))
        t2 = VGroup(
            MathTex(r"f(x)=|x|,\ a=0:\ \text{slopes } -1 \text{ and } +1"),
            MathTex(r"f'(0)\ \text{does not exist}", color=RED),
            MathTex(
                r"\Delta y = \Delta x \ \text{for every sign of } \Delta x"),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).scale(0.7).to_edge(RIGHT, buff=0.4)
        for m in t2:
            self.play(Write(m))
        self.wait(2)
        self.play(*[FadeOut(m)
                  for m in self.mobjects if m is not self.mobjects[0]])

        # C3: y = x^2 - 4 at a = 2
        sub = Text("C3 - (H3) fails: y = 0", font_size=28,
                   color=ORANGE).next_to(self.mobjects[0], DOWN, buff=0.3)
        self.play(FadeIn(sub))
        t3 = VGroup(
            MathTex(r"y=x^2-4,\quad a=2 \;\Rightarrow\; y=0"),
            MathTex(
                r"\Delta y \approx |f'(2)|\Delta x = 4\Delta x \quad\text{(finite)}", color=GREEN),
            MathTex(
                r"\delta y = \Delta y/|y| \quad\text{undefined}", color=RED),
        ).arrange(DOWN, buff=0.5).scale(0.9)
        for m in t3:
            self.play(Write(m))
        self.wait(2)
        self.clear()


# --------------------------------------------------------------------------
# 7. CASE STUDY 1 - GLASS TABLETOP  (~1 min 30 s)
# --------------------------------------------------------------------------
class S07_GlassTable(Base):
    def construct(self):
        self.heading("Case study 1 - Circular glass tabletop")
        info = VGroup(
            MathTex(r"A(r)=\pi r^2,\quad A'(r)=2\pi r"),
            MathTex(r"r_0=60.0\ \text{cm},\quad \Delta r=\pm0.2\ \text{cm}"),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).scale(0.8).to_edge(RIGHT, buff=0.5).shift(UP * 1.5)
        self.play(Write(info))

        # exaggerated ring
        R, dr = 1.8, 0.3
        disk = Circle(radius=R, color=BLUE, fill_opacity=0.35).shift(
            LEFT * 3.2 + DOWN * 0.3)
        ring = Annulus(inner_radius=R, outer_radius=R + dr,
                       color=YELLOW, fill_opacity=0.8).move_to(disk)
        r_line = Line(disk.get_center(), disk.get_center() +
                      R * RIGHT, color=WHITE)
        r_lab = MathTex("r").next_to(r_line, UP, buff=0.05)
        self.play(DrawBorderThenFill(disk))
        self.play(Create(r_line), Write(r_lab))
        self.play(FadeIn(ring))
        dr_lab = MathTex(r"\Delta r", color=YELLOW).next_to(
            disk.get_center() + (R + dr) * RIGHT, UR, buff=0.05)
        self.play(Write(dr_lab))

        # unroll the ring into a thin rectangle
        rect = Rectangle(width=2 * np.pi * R / 2.2, height=dr,
                         color=YELLOW, fill_opacity=0.8)
        rect.next_to(info, DOWN, buff=0.8).align_to(info, LEFT)
        rect_lab = MathTex(r"2\pi r \times \Delta r", color=YELLOW,
                           font_size=32).next_to(rect, DOWN, buff=0.1)
        self.play(TransformFromCopy(ring, rect))
        self.play(Write(rect_lab))
        approx = MathTex(r"\Delta A \approx 2\pi r\,\Delta r",
                         color=GREEN, font_size=44).next_to(rect_lab, DOWN, buff=0.4)
        self.play(Write(approx))
        self.wait(1.5)
        self.clear()

        self.heading("Case study 1 - results")
        res = VGroup(
            MathTex(r"A(60)=3600\pi\approx 11\,309.73\ \text{cm}^2"),
            MathTex(
                r"\Delta A\approx 120\pi\times0.2=24\pi\approx 75.40\ \text{cm}^2", color=YELLOW),
            MathTex(
                r"A\in[11\,234.33;\ 11\,385.13]\ \text{cm}^2", color=GREEN),
            MathTex(
                r"\delta r=0.33\%\ \Rightarrow\ \delta A\approx 2\delta r\approx 0.67\%", color=YELLOW),
            MathTex(
                r"\text{Exact: } 75.52\ \text{cm}^2,\ |\Delta A-dA|=\pi(\Delta r)^2\approx0.126\ (0.17\%)", color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).scale(0.75)
        for r in res:
            self.play(Write(r), run_time=1.4)
        self.wait(1)
        inv = VGroup(
            Text("Inverse tolerance", font_size=26, color=BLUE),
            MathTex(
                r"|\Delta A|\le 50 \Rightarrow \Delta r \le \tfrac{50}{2\pi\cdot 60}\approx 0.13\ \text{cm}"),
        ).arrange(DOWN, buff=0.2).scale(0.8).to_edge(DOWN, buff=0.5)
        self.play(FadeIn(inv))
        self.wait(2)
        self.clear()

        # validity limits
        self.heading("Validity limits", color=RED)
        lim = VGroup(
            Text("• Small perturbation: δr < 5%", font_size=28),
            Text("  1 cm button, Δr = 0.5 cm (δr = 50%): π(Δr)² is no longer negligible",
                 font_size=24, color=GREY_B),
            Text("• Geometry: ellipse A = πab needs the total differential", font_size=28),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        for l in lim:
            self.play(FadeIn(l, shift=RIGHT * 0.2))
        self.wait(2)
        self.clear()


# --------------------------------------------------------------------------
# 8. CASE STUDY 3 - CLIFF JUMP  (~2 min)
# --------------------------------------------------------------------------
class S08_CliffJump(Base):
    def construct(self):
        self.heading("Case study 2 - Cliff-jump height (rock-drop method)")
        # scene
        cliff = Polygon([-6.5, -3, 0], [-6.5, 1.4, 0], [-3.6, 1.4, 0], [-3.6, -3, 0],
                        color=GREY, fill_color=GREY_E, fill_opacity=1)
        water = Rectangle(width=3.6, height=0.8, color=BLUE,
                          fill_color=BLUE_E, fill_opacity=0.8)
        water.move_to([-1.8 - 0.0, -2.6, 0]).align_to(cliff, DOWN)
        surface_y = water.get_top()[1]
        rock = Dot([-3.3, 1.5, 0], color=WHITE, radius=0.1)
        h_arrow = DoubleArrow(
            [-2.5, 1.4, 0], [-2.5, surface_y, 0], buff=0, color=YELLOW, tip_length=0.15)
        h_lab = MathTex(r"h", color=YELLOW).next_to(h_arrow, RIGHT, buff=0.1)
        self.play(FadeIn(cliff), FadeIn(water), FadeIn(rock))
        self.play(GrowFromCenter(h_arrow), Write(h_lab))

        model = MathTex(r"T=t_1+t_2=\sqrt{\tfrac{2h}{g}}+\tfrac{h}{v}",
                        font_size=44).to_edge(RIGHT, buff=0.5).shift(UP * 1.8)
        self.play(Write(model))

        # fall (t1)
        t1 = MathTex(r"t_1\approx 2.022\ \text{s}\ \text{(fall)}", color=ORANGE, font_size=32).next_to(
            model, DOWN, buff=0.5)
        self.play(rock.animate.move_to(
            [-3.3, surface_y, 0]), run_time=2, rate_func=lambda t: t ** 2)
        self.play(Write(t1))
        splash = Circle(radius=0.1, color=WHITE).move_to([-3.3, surface_y, 0])
        self.play(splash.animate.scale(5).set_opacity(0), run_time=0.8)
        # sound back up (t2)
        snd = Arrow([-3.0, surface_y, 0], [-3.0, 1.4, 0], buff=0,
                    color=TEAL, stroke_width=3, tip_length=0.15)
        t2 = MathTex(r"t_2\approx 0.058\ \text{s}\ \text{(sound)}", color=TEAL, font_size=32).next_to(
            t1, DOWN, buff=0.3)
        self.play(GrowArrow(snd), run_time=0.5)
        self.play(Write(t2))
        tot = MathTex(r"T_0 = 2.08\ \text{s}", color=YELLOW, font_size=40).next_to(
            t2, DOWN, buff=0.4)
        self.play(Write(tot))
        self.wait(1.5)
        self.clear()

        # solving for h
        self.heading("Solving for h(T)", color=BLUE)
        derive = VGroup(
            MathTex(r"(T-h/v)^2=2h/g \;\Rightarrow\; \text{quadratic in } h"),
            MathTex(
                r"s(T)=\sqrt{1+\tfrac{2gT}{v}},\qquad \text{take the } {-}\text{ root}"),
            MathTex(r"h(T)=\frac{v^2}{2g}\big(s(T)-1\big)^2", color=GREEN),
            MathTex(r"h'(T)=v\Big(1-\frac1{s(T)}\Big)", color=YELLOW),
            MathTex(
                r"\delta h\approx\Big(1+\frac1s\Big)\delta T \ \ (\text{between } 1\times \text{ and } 2\times)", color=YELLOW),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).scale(0.8)
        for d in derive:
            self.play(Write(d), run_time=1.4)
        self.wait(1.5)
        self.clear()

        # nominal + naive
        self.heading("Nominal value", color=BLUE)
        nom = VGroup(
            MathTex(r"s_0=\sqrt{1+\tfrac{2(9.8)(2.08)}{343}}\approx1.05776"),
            MathTex(
                r"h_0=\tfrac{343^2}{2(9.8)}(s_0-1)^2\approx 20.03\ \text{m}", color=GREEN),
            MathTex(
                r"\text{Naive } h=\tfrac12 gT^2 = 21.20\ \text{m} \;(+5.9\%)", color=RED),
            MathTex(
                r"h'(T_0)=343\big(1-\tfrac{1}{1.05776}\big)\approx18.73\ \text{m/s}", color=YELLOW),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).scale(0.85)
        for n in nom:
            self.play(Write(n), run_time=1.3)
        self.wait(1.5)
        self.clear()

        # listener groups on a number line
        self.heading("Three listeners, three uncertainty bands")
        nl = NumberLine(x_range=[10, 30, 5], length=10,
                        include_numbers=True, font_size=24).shift(DOWN * 1.5)
        self.play(Create(nl))
        nominal = Line(nl.n2p(20.03) + DOWN * 0.3,
                       nl.n2p(20.03) + UP * 3.2, color=WHITE)
        nom_lab = MathTex(r"h_0=20.03", font_size=28).next_to(
            nominal, UP, buff=0.1)
        self.play(Create(nominal), Write(nom_lab))
        groups = [
            ("Professional", 0.100, 1.87, 18.15, 21.90, GREEN, 0.6),
            ("Normal adult", 0.150, 2.81, 17.22, 22.84, YELLOW, 1.5),
            ("Teenager", 0.340, 6.37, 13.66, 26.39, RED, 2.4),
        ]
        for name, dT, dh, lo, hi, col, yoff in groups:
            y = nl.n2p(20.03)[1] + yoff
            bar = Line([nl.n2p(lo)[0], y, 0], [nl.n2p(hi)[
                       0], y, 0], color=col, stroke_width=8)
            cap1 = Line(bar.get_start() + DOWN * 0.1,
                        bar.get_start() + UP * 0.1, color=col)
            cap2 = Line(bar.get_end() + DOWN * 0.1,
                        bar.get_end() + UP * 0.1, color=col)
            lab = MathTex(rf"\text{{{name}}}:\ \Delta T={dT:.3f}\ \text{{s}}\Rightarrow \pm{dh:.2f}\ \text{{m}}",
                          font_size=26, color=col).next_to(bar, UP, buff=0.1)
            self.play(Create(bar), Create(cap1), Create(cap2), FadeIn(lab))
            self.wait(0.6)
        self.wait(1.5)
        self.clear()

        # takeaways
        self.heading("What the differential tells us", color=GREEN)
        tk = VGroup(
            MathTex(
                r"\text{Required: } \Delta h\le1\ \text{m}\Rightarrow \Delta T\le \tfrac{1}{18.73}\approx0.053\ \text{s}"),
            Text("Best human reaction ≈ 0.10 s → listening by ear is not enough",
                 font_size=26, color=RED),
            Text("Electronic timer / audio recording (ΔT ≈ 0.01 s) → Δh ≈ 0.19 m",
                 font_size=26, color=GREEN),
            Text(
                "Can tell a 10 m ledge from a 20 m one, but not 18 m from 21 m", font_size=26),
            Text("Teenager: ΔT/T = 16%, linearization is weak: true error +6.84 m / −5.89 m",
                 font_size=24, color=ORANGE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).scale(0.9)
        for t in tk:
            self.play(FadeIn(t, shift=UP * 0.15))
        self.wait(2.5)
        self.clear()


# --------------------------------------------------------------------------
# 9. VERIFICATION  (~1 min)
# --------------------------------------------------------------------------
class S09_Verification(Base):
    def construct(self):
        self.heading("Numerical verification (Python)")
        code = Code(code_string="dA_exact = np.pi*((r0+dr)**2 - r0**2)\n"
                                "dA_diff  = 2*np.pi*r0*dr\n"
                                "err      = abs(dA_exact - dA_diff)",
                    language="python", background="window")
        code.scale(0.8).to_edge(LEFT, buff=0.6).shift(UP * 0.5)
        self.play(FadeIn(code))

        drs = np.array([1.0, 0.5, 0.2, 0.1, 0.02])
        errs = np.pi * drs ** 2
        ax = Axes(x_range=[-2, 0.5, 1], y_range=[-4, 1, 1], x_length=5.5, y_length=3.8, tips=False,
                  axis_config={"include_numbers": True, "font_size": 20}).to_edge(RIGHT, buff=0.6).shift(DOWN * 0.3)
        xl = ax.get_x_axis_label(
            MathTex(r"\log_{10}\Delta r", font_size=24), edge=DOWN, direction=DOWN)
        yl = ax.get_y_axis_label(
            MathTex(r"\log_{10}|\Delta A-dA|", font_size=24), edge=LEFT, direction=LEFT)
        self.play(Create(ax), Write(xl), Write(yl))
        dots = VGroup(*[Dot(ax.c2p(np.log10(d), np.log10(e)),
                      color=YELLOW, radius=0.07) for d, e in zip(drs, errs)])
        self.play(LaggedStart(*[FadeIn(d, scale=2)
                  for d in dots], lag_ratio=0.4))
        line = ax.plot(lambda t: np.log10(np.pi) + 2 * t,
                       x_range=[-1.8, 0.1], color=GREEN)
        self.play(Create(line))
        slope = MathTex(r"\text{slope}\approx 2",
                        color=GREEN).next_to(ax, UP, buff=0.2)
        self.play(Write(slope))

        obs = VGroup(
            MathTex(
                r"\Delta r:\ 1.0 \to 0.5 \quad |\Delta A-dA|:\ 3.1416 \to 0.7854\ (\div4)"),
            Text("Relative discrepancy < 1.3% in every case study → (H2) holds",
                 font_size=24, color=YELLOW),
        ).arrange(DOWN, buff=0.3).scale(0.8).to_edge(DOWN, buff=0.4)
        self.play(FadeIn(obs))
        self.wait(3)
        self.clear()


# --------------------------------------------------------------------------
# 10. CONCLUSION  (~45 s)
# --------------------------------------------------------------------------
class S10_Conclusion(Base):
    def construct(self):
        self.heading("Conclusions", color=GREEN)
        pts = VGroup(
            MathTex(
                r"\Delta y\approx |f'(a)|\,\Delta x \qquad \delta y\approx\big|d(\ln|y|)\big|", color=YELLOW),
            Text("Remainder ≤ (M/2)(Δx)² → quadratic convergence", font_size=28),
            Text("Each hypothesis (H1)-(H3) is necessary (counterexamples)", font_size=28),
            Text("Power law δy ≈ |n|·δx: instant on-site estimates", font_size=28),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.5)
        for p in pts:
            self.play(FadeIn(p, shift=UP * 0.2))
            self.wait(0.8)
        self.wait(1)
        fw = Text("Further work: total differential · root-sum-square errors · Taylor corrections",
                  font_size=24, color=BLUE).to_edge(DOWN, buff=0.8)
        self.play(FadeIn(fw))
        self.wait(2)
        self.clear()
        thanks = Text("Thank you for watching", font_size=52)
        team = Text("Trần Nhật Duy · Phạm Lâm Nhật Khoa · Trần Việt Quốc Toàn · Nguyễn Minh Trang",
                    font_size=22, color=GREY_B).next_to(thanks, DOWN, buff=0.6)
        self.play(Write(thanks))
        self.play(FadeIn(team))
        self.wait(3)
