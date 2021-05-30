from manim import *
from utils import Equations
import numpy as np


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


class Test(Scene):

    def __init__(self, **kwargs):
        Scene.__init__(self, **kwargs)

        self.cartHighlightColour = ORANGE
        self.suspendedMassHighlightColour = BLUE
        self.operatorColour = '#fcc088'
        self.accelerationHighlightColour = GREEN_A

        self.texToColourMap = {
            '=': self.operatorColour,
            '+': self.operatorColour,
            '-': self.operatorColour,
            r'\Rightarrow': self.operatorColour,
            '_{c}': self.cartHighlightColour,
            '_{cx}': self.cartHighlightColour,
            '_{s}': self.suspendedMassHighlightColour,
            '_{sy}': self.suspendedMassHighlightColour
        }

    def construct(self):
        equations2 = MathTex('-m_{s}a_{cx}', r'+m_{s}g-m_{c}gsin\theta&=m_{c}a_{cx}\\',
                               r'\Rightarrow a_{cx}(m_{c}+m_{s})&=g(m_{s}-m_{c}sin\theta)\\',
                               r'\Rightarrow a_{cx}&={g(m_{s}-m_{c}sin\theta) \over m_{c}+m_{s}}',
                               tex_to_color_map=self.texToColourMap).shift(RIGHT)
        self.play(Write(equations2), run_time=2)


class FBDs(Scene):
    TOP_RIGHT_CORNER = UP * 3.5 + RIGHT * 6.5
    TOP_LEFT_CORNER = UP * 4 + LEFT * 6.5

    FBD_SCALE_FACTOR = 1.3

    def __init__(self, **kwargs):
        Scene.__init__(self, **kwargs)
        self.inclineAngle = FBDs.degToRad(15)  # exaggerated for FBD
        self.cartFBDGroup = None
        self.suspendedMassFBDGroup = None

        self.cartHighlightColour = ORANGE
        self.suspendedMassHighlightColour = BLUE
        self.operatorColour = '#fcc088'
        self.accelerationHighlightColour = GREEN_A

        self.texToColourMap = {
            '=': self.operatorColour,
            '+': self.operatorColour,
            '-': self.operatorColour,
            r'\Rightarrow': self.operatorColour,
            '_{c}': self.cartHighlightColour,
            '_{cx}': self.cartHighlightColour,
            '_{s}': self.suspendedMassHighlightColour,
            '_{sy}': self.suspendedMassHighlightColour
        }

        self.accelerationConstraintEquation = None
        self.tensionEquation = None

    @staticmethod
    def degToRad(degrees: float) -> float:
        return degrees * PI / 180

    @staticmethod
    def generateCS() -> VGroup:
        x = Arrow(start=ORIGIN, end=RIGHT, buff=0)
        y = Arrow(start=ORIGIN, end=UP, buff=0)
        xLabel = Tex("x").scale(0.8).next_to(x, RIGHT)
        yLabel = Tex("y").scale(0.8).next_to(y, UP)

        return VGroup(x, y, xLabel, yLabel)

    @staticmethod
    def createEquationNumber(number: float, colour: str = WHITE) -> VGroup:
        circle = Circle(radius=0.2, color=colour)
        number = Tex(str(number)).scale(0.6).move_to(circle.get_center())
        return VGroup(circle, number)

    @staticmethod
    def getRightAlignShift(referenceElement: Mobject, shiftingElement: Mobject) -> np.ndarray:
        return referenceElement.get_corner(DOWN + RIGHT) - shiftingElement.get_corner(UP + RIGHT) + DOWN * 0.1

    @staticmethod
    def getRightAlignShiftToPoint(referencePoint: np.ndarray, shiftingElement: Mobject) -> np.ndarray:
        return referencePoint - shiftingElement.get_corner(UP + RIGHT)

    def displayNumberPlane(self):
        numberPlane = NumberPlane()
        self.add(numberPlane)

    def suspendedMassFBD(self):
        square = Square(radius=1)
        # Buff is the distance of the arrow from its start and end points,
        # for example if you didn't want it directly against that
        weightForce = Arrow(start=ORIGIN, end=DOWN * 2, color=self.suspendedMassHighlightColour)
        tensionForce = Arrow(start=ORIGIN, end=UP * 2, color=self.suspendedMassHighlightColour)
        # self.add(square) #Adds the square to the scene
        weightLabel = MathTex('m_{s}g', color=self.suspendedMassHighlightColour).next_to(weightForce, DOWN)
        tensionLabel = Tex('T', color=self.suspendedMassHighlightColour).next_to(tensionForce, UP)

        cs = FBDs.generateCS().next_to(square, LEFT)

        title = Tex("FBD of Suspended Mass").next_to(tensionLabel, UP)

        self.suspendedMassFBDGroup = Group(title, square, weightForce, tensionForce, weightLabel, tensionLabel, cs)

        self.play(Write(title), GrowFromCenter(square))
        self.play(FadeIn(weightForce), FadeIn(tensionForce), FadeIn(cs))
        self.play(Write(weightLabel), Write(tensionLabel))
        self.wait(2)
        self.play(self.suspendedMassFBDGroup.animate.scale(0.4))
        self.play(self.suspendedMassFBDGroup.animate.shift(LEFT * 5.1 + DOWN * 1.5))

    def cartFBD(self):
        cart = Rectangle(height=1.5, width=2).rotate(self.inclineAngle, about_point=ORIGIN)

        normalForce = Arrow(
            start=ORIGIN, end=UP * 2, color=self.cartHighlightColour
        ).rotate(self.inclineAngle, about_point=ORIGIN)
        weightForce = Arrow(start=ORIGIN, end=DOWN * 2, color=self.cartHighlightColour)
        tensionForce = Arrow(
            start=ORIGIN, end=RIGHT * 2, color=self.cartHighlightColour
        ).rotate(self.inclineAngle, about_point=ORIGIN)

        normalLabel = Tex("N", color=self.cartHighlightColour).next_to(normalForce, UP)
        weightLabel = MathTex("m_{c}g", color=self.cartHighlightColour).next_to(weightForce, DOWN)
        tensionLabel = Tex("T", color=self.cartHighlightColour).next_to(tensionForce, RIGHT)

        surfaceLine = Line(start=LEFT * 2, end=RIGHT * 2).rotate(self.inclineAngle).shift(DOWN * 0.78)
        referenceLine = Line(start=surfaceLine.get_start(), end=surfaceLine.get_start() + RIGHT * 1.7)
        angle = Angle(referenceLine, surfaceLine, radius=1.3, other_angle=False)
        theta = MathTex(r"\theta").next_to(angle, RIGHT).scale(0.7)

        angleGroup = VGroup(surfaceLine, referenceLine, angle, theta)

        cs = FBDs.generateCS().next_to(cart, LEFT).rotate(self.inclineAngle)

        title = Tex("FBD of Cart").next_to(normalLabel, UP)

        self.cartFBDGroup = VGroup(title, cart, normalForce, weightForce, tensionForce, normalLabel, weightLabel,
                                   tensionLabel, cs, angleGroup)
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
        self.play(self.cartFBDGroup.animate.scale(0.4))
        self.play(self.cartFBDGroup.animate.shift(LEFT * 5 + UP * 1.5))

    def suspendedMassCalculations(self):
        equations = MathTex(
            r'\sum F', '_{sy}', '=', 'm', '_{s}', 'a', '_{sy}', r'\Rightarrow', 'T', '-', 'm', '_{s}', 'g', '=', 'm',
            '_{s}',
            'a', '_{sy}', r'\\', r'\Rightarrow', 'T', '=', 'm', '_{s}', 'a', '_{sy}', '+', 'm', '_{s}', 'g',
            tex_to_color_map=self.texToColourMap
        ).move_to(RIGHT)

        equationNumber = FBDs.createEquationNumber(2).next_to(equations[19:], RIGHT)
        self.tensionEquation = VGroup(equations[20:], equationNumber)

        equationSurroundingBox1 = SurroundingRectangle(equations[0:7])
        equationSurroundingBox2 = SurroundingRectangle(self.tensionEquation, color=self.suspendedMassHighlightColour)

        self.play(self.suspendedMassFBDGroup.animate.scale(self.FBD_SCALE_FACTOR))
        self.play(FadeIn(equations[0:7]))
        self.play(Create(equationSurroundingBox1))
        self.wait(0.2)
        self.play(Write(equations[7:19]), run_time=2)
        self.play(FadeOut(equationSurroundingBox1))
        self.wait(0.2)
        self.play(Write(equations[19:]), run_time=2)
        self.play(Create(equationNumber))
        self.play(FadeOut(equations[0:20]), Create(equationSurroundingBox2))
        self.play(
            (self.tensionEquation + equationSurroundingBox2).animate.shift(
                FBDs.getRightAlignShift(self.accelerationConstraintEquation, self.tensionEquation))
        )
        self.play(FadeOut(equationSurroundingBox2), self.suspendedMassFBDGroup.animate.scale(1 / self.FBD_SCALE_FACTOR))

    def cartCalculations(self):
        sumForcesX = MathTex(r'\sum F', '_{cx}', '=', 'm', '_{c}', 'a', '_{cx}', r'\Rightarrow', 'T', '-', 'm', '_{c}',
                             r'gsin\theta', '=', 'm', '_{c}', 'a', '_{cx}', tex_to_color_map=self.texToColourMap
                             ).shift(RIGHT)
        substitutedEquation = MathTex('m', '_{s}', 'a', '_{sy}', '+', 'm', '_{s}', 'g', '-', 'm', '_{c}', r'gsin\theta',
                                      '=', 'm', '_{c}', 'a', '_{cx}', tex_to_color_map=self.texToColourMap).shift(RIGHT)
        equations2 = Equations('-m_{s}a_{cx}', r'+m_{s}g-m_{c}gsin\theta=m_{c}a_{cx}',
                               r'\\ \Rightarrow a_{cx}(m_{c}+m_{s})=g(m_{s}-m_{c}sin\theta)',
                               r'\\\Rightarrow a_{cx}={ g(m_{s}-m_{c}sin\theta)\over m_{c}+m_{s} }',
                               tex_to_color_map=self.texToColourMap).shift(RIGHT)

        equationSurroundingBox1 = SurroundingRectangle(sumForcesX[0:7])
        equationSurroundingBox2 = SurroundingRectangle(sumForcesX[8], color=self.suspendedMassHighlightColour)
        equationSurroundingBox3 = SurroundingRectangle(substitutedEquation[0:8], color=self.suspendedMassHighlightColour)
        equationSurroundingBox4 = SurroundingRectangle(self.tensionEquation, color=self.suspendedMassHighlightColour)
        equationSurroundingBox5 = SurroundingRectangle(self.accelerationConstraintEquation, color=self.accelerationHighlightColour)
        equationSurroundingBox6 = SurroundingRectangle(substitutedEquation[0:4], self.accelerationHighlightColour)
        equationSurroundingBox7 = SurroundingRectangle(equations2[0], self.accelerationHighlightColour)

        self.play(Write(sumForcesX[0:7]))
        self.wait()
        self.play(Create(equationSurroundingBox1), Write(sumForcesX[7:]))
        self.play(ReplacementTransform(equationSurroundingBox1, equationSurroundingBox2),
                  FadeIn(equationSurroundingBox4))
        self.play(FadeOut(sumForcesX[0:8]))
        self.play(ReplacementTransform(sumForcesX[8:], substitutedEquation),
                  ReplacementTransform(equationSurroundingBox2, equationSurroundingBox3))
        self.play(FadeOut(equationSurroundingBox4))
        self.play(FadeIn(equationSurroundingBox5),
                  ReplacementTransform(equationSurroundingBox3, equationSurroundingBox6))
        self.play(ReplacementTransform(substitutedEquation, equations2[0:2]),
                  ReplacementTransform(equationSurroundingBox6, equationSurroundingBox7))
        self.play(FadeOut(equationSurroundingBox7), Write(equations2[2:]), run_time=2.5)

    def kinematicConstraints(self):
        equations = Equations(r'length&=l_{1}+l_{2}+constant', r'\\ 0&=a_{1}+a_{2}',
                              tex_to_color_map=self.texToColourMap).shift(RIGHT + UP)

        acceleration1 = MathTex('a_{1}', '=', '-', 'a', '_{cx}', tex_to_color_map=self.texToColourMap)
        acceleration2 = MathTex('a_{2}', '=', '-', 'a', '_{sy}',
                                tex_to_color_map=self.texToColourMap).next_to(acceleration1, RIGHT * 2)

        accelerations = VGroup(acceleration1, acceleration2).next_to(equations[1], DOWN * 2)

        kinematicConstraints = MathTex('-', 'a', '_{sy}', '-', 'a', '_{cx}', '=', '0', r'\Rightarrow',
                                       'a', '_{cx}', '=', '-', 'a', '_{sy}',
                                       tex_to_color_map=self.texToColourMap).next_to(accelerations, DOWN * 2)
        title = Tex("Kinematic Constraints").next_to(equations[0], UP * 3)

        equationNumber = FBDs.createEquationNumber(1).next_to(kinematicConstraints, RIGHT)
        self.accelerationConstraintEquation = VGroup(kinematicConstraints[9:], equationNumber)

        surroundingBox = SurroundingRectangle(self.accelerationConstraintEquation, color=self.accelerationHighlightColour)

        self.play(Write(title))
        self.play(Write(equations[0]), run_time=2)
        self.play(Write(equations[1]))
        self.play(Write(accelerations), run_time=1.5)
        self.wait(1.5)
        self.play(Write(kinematicConstraints))
        self.play(Create(equationNumber), Create(surroundingBox))
        self.play(FadeOut(title), FadeOut(equations),
                  FadeOut(accelerations), FadeOut(kinematicConstraints[0:9]))
        self.play(
            (self.accelerationConstraintEquation + surroundingBox).animate.shift(
                FBDs.getRightAlignShiftToPoint(self.TOP_RIGHT_CORNER, self.accelerationConstraintEquation))
        )
        self.play(FadeOut(surroundingBox))

    def construct(self):
        # self.displayNumberPlane()
        self.cartFBD()
        self.suspendedMassFBD()
        self.kinematicConstraints()
        self.suspendedMassCalculations()
        self.cartCalculations()
