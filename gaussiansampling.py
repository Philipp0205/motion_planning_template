import math

import workspace
import numpy


class GaussianSampling:
    def __init__(self, configspace, workspace):
        self.configspace = configspace
        self.workspace = workspace

        self.gaussianSampling(10000)

    def gaussianSampling(self, n):
        gaussianSamplePoints = []

        for x in range(0, n + 1, 1):
            # forbbiden config
            ct = numpy.random.randint(0, 1349)
            cr = numpy.random.randint(0, 979)

            if self.workspace.envArray[cr][ct]:
                #print("BLACK POINT")
                d = 25

                pointsincircle = self.pointsInCircum(d, ct, cr)

                for t in pointsincircle:
                    if self.workspace.envArray[t[1]][t[0]]:
                        gaussianSamplePoints.insert(x, t)
                        break

        self.drawPointOfArray(gaussianSamplePoints)
        return gaussianSamplePoints

    def pointsInCircum(self, radius, x_coordinate, y_coordinate):
        pi = math.pi
        n = radius

        circumpoints = []

        if x_coordinate + radius < 1350 and y_coordinate + radius < 980:
            for x in range(0, n + 1):
                singlecircumpoint = round((math.cos(2 * pi / n * x) * radius) + x_coordinate), round((math.sin(2 * pi / n * x) * radius) + y_coordinate)
                circumpoints.insert(x, singlecircumpoint)
        return circumpoints

    def drawPointOfArray(self, array):
        if array is not None:
            for x in array:
                self.configspace.drawConfiguration(x[0], x[1], "Yellow")
