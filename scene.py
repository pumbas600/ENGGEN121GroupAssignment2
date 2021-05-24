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
        weightLabel = MathTex("m_{s}g", color=ORANGE).next_to(weightForce, DOWN)
        tensionLabel = Tex("T", color=ORANGE).next_to(tensionForce, RIGHT)

        cs = self.generateCS().next_to(cart, LEFT).rotate(self.inclineAngle)

        title = Tex("FBD of Cart").next_to(normalLabel, UP)

        group = Group(title, cart, normalForce, weightForce, tensionForce, normalLabel, weightLabel, tensionLabel, cs)

        self.play(Write(title), GrowFromCenter(cart))
        self.play(FadeIn(normalForce), FadeIn(weightForce), FadeIn(tensionForce), FadeIn(cs))
        self.play(Write(normalLabel), Write(weightLabel), Write(tensionLabel))
        self.wait(2)
        self.play(group.animate.scale(0.4))
        self.play(group.animate.shift(LEFT * 5 + UP * 1.5))

    def construct(self):
        self.cartFBD()
        self.suspendedMassFBD()


