from collections import deque
import random
import math


class SPRM:
    def __init__(self, configspace, workspace):
        # all edges between two config are stored
        edge_data_structure = deque("abcde")
        # stores all configuration s
        self.vertex = []

        self.vertex_no_colission = []
        self.vertex_in_colission = []

        self.configspace = configspace
        self.workspace = workspace

        self.compute_samples(100, 1350, 980)

        self.collission_segments = self.compute_neares_neighbours(self.vertex_in_colission, 80)
        self.draw_lines(self.collission_segments, "blue")
        self.no_collission_segments = self.compute_neares_neighbours(self.vertex_no_colission, 80)

        testA = (10, 10)
        testB = (20, 20)
        configspace.drawConfiguration(10, 10, "red")
        configspace.drawConfiguration(20, 20, "red")
        configspace.draw_line(testA, testB, "red")
        self.validate_edge([testA, testB], 20)

        # self.free_samples = self.draw_free_graph(self.no_collission_segments, self.collission_segments)
        # self.draw_lines(self.free_samples, "black")

    def add_start_goal_configurations(self):
        self.vertex.append([self.configspace.initConfig, self.configspace.goalConfig])
        self.configspace.drawConfiguration(self.configspace.initConfig[0], self.configspace.initConfig[1], 'red')

    def compute_samples(self, number_of_samples, x_range, y_range):
        x_range -= 1
        y_range -= 1

        for x in range(number_of_samples):
            sample = (random.randint(0, x_range), random.randint(0, y_range))
            if self.workspace.isInCollision(sample[0], sample[1]):
                self.vertex_no_colission.append(sample)
            else:
                self.vertex_in_colission.append(sample)

        # Only debugging
        self.color_points(self.vertex_no_colission, "yellow")
        self.color_points(self.vertex_in_colission, "black")

    def color_points(self, point_array, color):
        for point in point_array:
            self.configspace.drawConfiguration(point[0], point[1], color)

    def draw_lines(self, point_array, color):
        for point in point_array:
            self.configspace.draw_line(point[0], point[1], color)

    # Source?
    def is_nearest_neighbour(self, center_x, center_y, radius, x, y):
        dist = math.sqrt((center_x - x) ** 2 + (center_y - y) ** 2)
        return dist <= radius

    def compute_neares_neighbours(self, samples, radius):
        result = []
        for center_sample in samples:
            for sample in samples:
                if self.is_nearest_neighbour(center_sample[0], center_sample[1], radius, sample[0], sample[1]):
                    result.append([center_sample, sample])

        return result

    def validate_edge(self, no_collission_samples, n):
        segment_start = no_collission_samples[0]
        segment_end = no_collission_samples[1]

        def create_linear_interpolation(n):
            cx = segment_start[0] + (segment_end[0] - segment_start[0]) / n
            cy = segment_start[1] + (segment_end[1] - segment_start[1]) / n

            if self.workspace.isInCollision(round(cx), round(cy)):
                return True
            elif segment_start[0] == segment_end[0] & segment_start[1] == segment_end[1]:
                return False
            else:
                # del segment_start
                # segment_start = [(cx, cy)]

        create_linear_interpolation(n)


    def draw_free_graph(self, no_coll_samples, in_coll_samples):
        free_samples = []
        for sample in no_coll_samples:
            for sample2 in in_coll_samples:
                if self.line_intersection(sample, sample2):
                    free_samples.append(sample)
        return free_samples
