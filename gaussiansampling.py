import math

import workspace
import numpy


class GaussianSampling:
    def __init__(self, configspace, workspace):
        self.configspace = configspace
        self.workspace = workspace

        self.gaussian_sampling2(60000)

    def gaussian_sampling2(self, n):
        graph = []

        for x in range(0, n + 1, 1):
            c1 = self.get_random_config()
            ct = c1[0]
            cr = c1[1]

            d = 20

            if ct + d < 1350 and cr < 980:
                ct_ = ct + d

                c2 = ct_, cr

                c1_in_c_free = not self.workspace.isInCollision(ct, cr)
                c2_in_c_free = not self.workspace.isInCollision(c2[0], c2[1])

                if not c1_in_c_free and not c2_in_c_free:
                    graph.append(c1)
                elif not c2_in_c_free and not c1_in_c_free:
                    graph.append(c2)
                else:
                    c1 = None
                    c2 = None

        self.draw_point_of_array(graph)

    def get_random_config(self):
        # forbidden config
        random_sample = numpy.random.randint(0, 1349), numpy.random.randint(0, 979)
        return random_sample

    def get_forbidden_config(self):
        # forbidden config
        forbidden_sample = numpy.random.randint(0, 1349), numpy.random.randint(0, 979)
        x = forbidden_sample[0]
        y = forbidden_sample[1]

        if not self.workspace.isInCollision(x, y):
            self.get_forbidden_config()
        else:
            return forbidden_sample

    def points_in_circum(self, radius, x_coordinate, y_coordinate):
        pi = math.pi
        n = round(radius / 2) + 1
        circum_points = []

        if x_coordinate + radius < 1350 and y_coordinate + radius < 980:
            for x in range(0, n + 1):
                single_circum_point = round((math.cos(2 * pi / n * x) * radius) + x_coordinate), round(
                    (math.sin(2 * pi / n * x) * radius) + y_coordinate)
                circum_points.insert(x, single_circum_point)
        return circum_points

    def draw_point_of_array(self, array):
        if array is not None:
            for x in array:
                self.configspace.drawConfiguration(x[0], x[1], "Yellow")

    def gaussian_sampling(self, n):
        gaussian_sample_points = []

        for x in range(0, n + 1, 1):
            forbidden_sample = self.get_me_a_forbidden_config()

            if forbidden_sample is not None:
                cr = forbidden_sample[0]
                ct = forbidden_sample[1]

            d = 20

            points_in_circle = self.points_in_circum(d, cr, ct)

            for t in points_in_circle:
                x = t[0]
                y = t[1]
                if self.workspace.envArray[y][x]:
                    gaussian_sample_points.insert(x, t)
                    break

        self.draw_point_of_array(gaussian_sample_points)
        #self.draw_point_of_array(points_in_circle)
        return gaussian_sample_points