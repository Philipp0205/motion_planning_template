import workspace
import numpy


class GaussianSampling:
    def __init__(self, configspace, workspace):
        self.configspace = configspace
        self.workspace = workspace

        self.gaussianSampling(500000)

    def gaussianSampling(self, n):
        gaussianSamplePoints = []

        for x in range(0, n + 1, 1):
            ct = numpy.random.randint(0, 1349)
            cr = numpy.random.randint(0, 979)

            if not self.workspace.envArray[cr][ct]:
                #print("BLACK POINT")
                d = 5
                c1 = (ct, cr)
                gaussianSamplePoints.insert(x, self.iterateThroughCircleOfC1(d, ct, cr))

        self.drawPointOfArray(gaussianSamplePoints)
        return gaussianSamplePoints

    def iterateThroughCircleOfC1(self, d, x_0, y_0):
        t = 0
        while t < 2 * numpy.pi:
            x = round(d * numpy.cos(t) + x_0)
            y = round(d * numpy.sin(t) + y_0)

            if self.workspace.envArray[round(y)][round(x)]:
                valid = int(x), int(y)
                return valid
            else:
                t = t + 0.10

    def drawPointOfArray(self, array):
        for x in array:
            if x is not None:
                self.configspace.drawConfiguration(x[0], x[1], "Blue")
