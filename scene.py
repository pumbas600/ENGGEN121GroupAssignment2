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
        self.inclineAngle = self.degToRad(15)  # exaggerated for FBD
        self.cartFBDGroup = None
        self.suspendedMassFBDGroup = None

        self.cartHighlightColour = ORANGE
        self.suspendedMassHighlightColour = BLUE
        self.operatorColour = '#fcc088'

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

    def degToRad(self, degrees: float) -> float:
        return degrees * PI / 180

    def generateCS(self) -> VGroup:
        x = Arrow(start=ORIGIN, end=RIGHT, buff=0)
        y = Arrow(start=ORIGIN, end=UP, buff=0)
        xLabel = Tex("x").scale(0.8).next_to(x, RIGHT)
        yLabel = Tex("y").scale(0.8).next_to(y, UP)

        return VGroup(x, y, xLabel, yLabel)

    def createEquationNumber(self, number, colour=WHITE) -> VGroup:
        circle = Circle(radius=0.2, color=colour)
        number = Tex(str(number)).scale(0.6).move_to(circle.get_center())
        return VGroup(circle, number)

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

        cs = self.generateCS().next_to(square, LEFT)

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

        cs = self.generateCS().next_to(cart, LEFT).rotate(self.inclineAngle)

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

    def suspendedCartCalculations(self):
        equations = MathTex(
            r'\sum F', '_{sy}', '=', 'm', '_{s}', 'a', '_{sy}', r'\Rightarrow', 'T', '-', 'm', '_{s}', 'g', '=', 'm', '_{s}',
            'a', '_{sy}', r'\\', r'\Rightarrow', 'T', '=', 'm', '_{s}', 'a', '_{sy}', '+', 'm', '_{s}', 'g',
            tex_to_color_map=self.texToColourMap
        ).move_to(RIGHT)

        equationNumber = self.createEquationNumber(2).next_to(equations[19:], RIGHT)
        self.tensionEquation = VGroup(equations[19:], equationNumber)

        equationSurroundingBox1 = SurroundingRectangle(equations[0:7])
        equationSurroundingBox2 = SurroundingRectangle(self.tensionEquation, color=self.suspendedMassHighlightColour)

        self.play(self.suspendedMassFBDGroup.animate.scale(1.3))
        self.play(FadeIn(equations[0:7]))
        self.play(Create(equationSurroundingBox1))
        self.wait(0.2)
        self.play(Write(equations[7:19]), run_time=2)
        self.play(FadeOut(equationSurroundingBox1))
        self.wait(0.2)
        self.play(Write(equations[19:]), run_time=2)
        self.play(Create(equationNumber))
        self.play(FadeOut(equations[0:19]), Create(equationSurroundingBox2))
        self.play((self.tensionEquation + equationSurroundingBox2).animate.shift(UP * 4))
        self.play(FadeOut(equationSurroundingBox2))

    def cartCalculations(self):
        equations = MathTex(r'\sum F', '_{cx}', '=', 'm', '_{c}', 'a', '_{cx}', r'\Rightarrow', 'T', '-', 'm', '_{c}',
                            r'gsin\theta', '=', 'm', '_{c}', 'a', '_{cx}',
                            tex_to_color_map=self.texToColourMap)
        equationNumber = self.createEquationNumber(1).next_to(equations, RIGHT)
        self.play(Write(equations[0:7]))
        self.wait()
        self.play(Write(equations[7:]))

    def kinematicConstraints(self):
        pulleyLength = MathTex('l_{1}', '+', 'l_{2}', '+', 'constant', '=', 'Length', r'\\',
                               tex_to_color_map=self.texToColourMap).shift(RIGHT)
        pulleyAcceleration = MathTex(r'\Rightarrow', 'a_{1}', '+', 'a_{2}', '=', '0',
                                     tex_to_color_map=self.texToColourMap).next_to(pulleyLength, DOWN)
        acceleration1 = MathTex('a_{1}', '=', '-', 'a', '_{cx}', tex_to_color_map=self.texToColourMap)
        acceleration2 = MathTex('a_{2}', '=', '-', 'a', '_{sy}',
                                tex_to_color_map=self.texToColourMap).next_to(acceleration1, RIGHT)

        accelerations = VGroup(acceleration1, acceleration2).next_to(pulleyAcceleration, DOWN)

        kinematicConstraints = MathTex(r'\Rightarrow', '-', 'a', '_{sy}', '-', 'a', '_{cx}', '=', '0', r'\Rightarrow',
                                       'a', '_{cx}', '=', '-', 'a', '_{sy}',
                                       tex_to_color_map=self.texToColourMap).next_to(accelerations, DOWN)
        title = Tex("Kinematic Constraints").next_to(pulleyLength, UP)

        equationNumber = self.createEquationNumber(1).next_to(kinematicConstraints, RIGHT)
        self.accelerationConstraintEquation = VGroup(kinematicConstraints[10:], equationNumber)

        surroundingBox = SurroundingRectangle(self.accelerationConstraintEquation, color=GREEN_A)

        self.play(Write(title))
        self.play(Write(pulleyLength), run_time=2)
        self.play(Write(pulleyAcceleration))
        self.play(Write(accelerations), run_time=1.5)
        self.play(Write(kinematicConstraints))
        self.play(Create(equationNumber), Create(surroundingBox))
        self.play(FadeOut(title), FadeOut(pulleyLength), FadeOut(pulleyAcceleration),
                  FadeOut(accelerations), FadeOut(kinematicConstraints[0:10]))
        self.play((self.accelerationConstraintEquation + surroundingBox).animate.shift(4.2 * UP))
        self.play(FadeOut(surroundingBox))

    def construct(self):
        self.cartFBD() #TODO: Fix error with this
        self.suspendedMassFBD()
        self.kinematicConstraints()
        self.suspendedCartCalculations()

        #self.cartCalculations()

        pass
