from manim import *

class GenerateSphere(Scene):
    def construct(self):
        circle = Circle()
        circle.set_fill(PINK, opacity=0.5)

        square = Square()
        square.flip(RIGHT)
        square.rotate(-3 * TAU / 8)

        self.play(Create(square))
        self.play(Transform(square, circle))
        self.play(FadeOut(square))

class Task2Dot4(Scene):
    def construct(self):
        equation = MathTex(r'\sum F_{sy} = m_{s}a_{sy}', r'\Rightarrow T - m_{s}g = m_{s}a_{sy}\\',
                           r'\Rightarrow T = m_{s}a_{sy} + m_{s}g')

        title = Tex("Forces on Suspended Mass").next_to(equation, 4 * UP).scale(1.5)

        frameBox = SurroundingRectangle(equation[0], buff=0.1)

        self.play(Write(title))
        self.play(FadeIn(equation[0]))
        self.play(Create(frameBox))
        self.wait(0.2)
        self.play(Write(equation[1]), run_time=2)
        self.play(FadeOut(frameBox))
        self.wait(0.2)
        self.play(Write(equation[2]), run_time=2)

class MovingAngle(Scene):
    def construct(self):
        rotation_center = LEFT

        theta_tracker = ValueTracker(110)
        line1 = Line(LEFT, RIGHT)
        line_moving = Line(LEFT, RIGHT)
        line_ref = line_moving.copy()
        line_moving.rotate(
            theta_tracker.get_value() * DEGREES, about_point=rotation_center
        )
        a = Angle(line1, line_moving, radius=0.5, other_angle=False)
        te = MathTex(r"\theta").next_to(a, RIGHT)

        self.add(line1, line_moving, a, te)
        self.wait()

        line_moving.add_updater(
            lambda x: x.become(line_ref.copy()).rotate(
                theta_tracker.get_value() * DEGREES, about_point=rotation_center
            )
        )

        a.add_updater(
            lambda x: x.become(Angle(line1, line_moving, radius=0.5, other_angle=False))
        )
        te.add_updater(
            lambda x: x.move_to(
                Angle(
                    line1, line_moving, radius=0.5 + 3 * SMALL_BUFF, other_angle=False
                ).point_from_proportion(0.5)
            )
        )

        self.play(theta_tracker.animate.set_value(40))
        self.play(theta_tracker.animate.increment_value(140))
        self.play(te.animate.set_color(RED), run_time=0.5)
        self.play(theta_tracker.animate.set_value(350))

class FBDs(Scene):

    def __init__(self, **kwargs):
        Scene.__init__(self, **kwargs)
        self.inclineAngle = self.degToRad(15) #exaggerated for FBD

    def degToRad(self, degrees: float) -> float:
        return degrees * PI / 180

    def generateCS(self) -> Group:
        x = Arrow(start=ORIGIN, end=RIGHT, buff=0)
        y = Arrow(start=ORIGIN, end=UP, buff=0)
        xLabel = Tex("x").scale(0.8).next_to(x, RIGHT)
        yLabel = Tex("y").scale(0.8).next_to(y, UP)

        return Group(x, y, xLabel, yLabel)

    def displayNumberPlane(self):
        numberPlane = NumberPlane()
        self.add(numberPlane)

    def suspendedMassFBD(self):
        square = Square(radius=1)
        # Buff is the distance of the arrow from its start and end points, for example if you didn't want it directly against that
        weightForce = Arrow(start=ORIGIN, end=DOWN * 2, color=BLUE)
        tensionForce = Arrow(start=ORIGIN, end=UP * 2, color=BLUE)
        # self.add(square) #Adds the square to the scene
        weightLabel = MathTex("m_{s}g", color=BLUE).next_to(weightForce, DOWN)
        tensionLabel = Tex("T", color=BLUE).next_to(tensionForce, UP)

        cs = self.generateCS().next_to(square, LEFT)

        title = Tex("FBD of Suspended Mass").next_to(tensionLabel, UP)

        group = Group(title, square, weightForce, tensionForce, weightLabel, tensionLabel, cs)

        self.play(Write(title), GrowFromCenter(square))
        self.play(FadeIn(weightForce), FadeIn(tensionForce), FadeIn(cs))
        self.play(Write(weightLabel), Write(tensionLabel))
        self.wait(2)
        self.play(group.animate.scale(0.4))
        self.play(group.animate.shift(LEFT * 5.1 + DOWN * 1.5))

    def cartFBD(self):
        cart = Rectangle(height=1.5, width=2).rotate(self.inclineAngle, about_point=ORIGIN)

        normalForce = Arrow(start=ORIGIN, end=UP*2, color=ORANGE).rotate(self.inclineAngle, about_point=ORIGIN)
        weightForce = Arrow(start=ORIGIN, end=DOWN*2, color=ORANGE)
        tensionForce = Arrow(start=ORIGIN, end=RIGHT * 2, color=ORANGE).rotate(self.inclineAngle, about_point=ORIGIN)

        normalLabel = Tex("N", color=ORANGE).next_to(normalForce, UP)
        weightLabel = MathTex("m_{c}g", color=ORANGE).next_to(weightForce, DOWN)
        tensionLabel = Tex("T", color=ORANGE).next_to(tensionForce, RIGHT)

        surfaceLine = Line(start=LEFT * 2, end=RIGHT * 2).rotate(self.inclineAngle).shift(DOWN * 0.78)
        referenceLine = Line(start=surfaceLine.get_start(), end=surfaceLine.get_start() + RIGHT * 1.7)
        angle = Angle(referenceLine, surfaceLine, radius=1.3, other_angle=False)
        theta =  MathTex(r"\theta").next_to(angle, RIGHT).scale(0.7)

        angleGroup = Group(surfaceLine, referenceLine, angle, theta)

        cs = self.generateCS().next_to(cart, LEFT).rotate(self.inclineAngle)

        title = Tex("FBD of Cart").next_to(normalLabel, UP)

        fbdGroup = Group(title, cart, normalForce, weightForce, tensionForce, normalLabel, weightLabel, tensionLabel, cs,
                      angleGroup)
        self.play(
            Write(title), Write(theta), FadeIn(angle), Create(surfaceLine), Create(referenceLine), GrowFromCenter(cart)
        )
        self.play(
            Create(normalForce), Create(weightForce), Create(tensionForce), FadeIn(cs)
        )
        self.play(
            Write(normalLabel), Write(weightLabel), Write(tensionLabel)
        )
        self.wait(2)
        self.play(fbdGroup.animate.scale(0.4))
        self.play(fbdGroup.animate.shift(LEFT * 5 + UP * 1.5))

    def construct(self):
        self.cartFBD()
        self.suspendedMassFBD()


