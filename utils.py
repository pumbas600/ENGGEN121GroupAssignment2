from manim import *
from typing import Tuple


class Equations(MathTex):

    def __init__(self, *equations: str, **kwargs):
        MathTex.__init__(self, *equations, **kwargs)
        self.__equationIndices = []

        for i in range(len(equations)):
            equation = MathTex(equations[i], **kwargs)

            start = 0 if i == 0 else self.__equationIndices[i - 1][1]
            stop = start + len(equation)
            
            self.__equationIndices.append((start, stop))

        #self.__mathTexEquations = MathTex(*equations, **kwargs)

    def getEquationIndices(self, index: int or slice) -> Tuple[int, int]:
        if isinstance(index, slice):
            indices = self.__equationIndices[index]
            start = indices[0][0]
            stop = indices[len(indices) - 1][1]
            return start, stop
        else:
            return self.__equationIndices[index]

    def __getitem__(self, index: int or slice) -> VGroup:
        indices = self.getEquationIndices(index)
        return MathTex.__getitem__(self, slice(indices[0], indices[1]))

