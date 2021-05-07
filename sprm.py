from collections import deque
import random
import math


class SPRM:
    def __init__(self, configspace, workspace):
        # all edges between two config are stored
        edge_data_structure = deque("abcde")
        # stores all configuration s
        self.vertex = []
        self.samples = []
        self.configspace = configspace
        self.workspace = workspace

        self.compute_samples(6000, 1350, 980)

    def add_start_goal_configurations(self):
        self.vertex.append([self.configspace.initConfig, self.configspace.goalConfig])
        self.configspace.drawConfiguration(self.configspace.initConfig[0], self.configspace.initConfig[1], 'red')

    def compute_samples(self, number_of_samples, x_range, y_range):
        x_range -= 1
        y_range -= 1
        for x in range(number_of_samples):
            sample = (random.randint(0, x_range), random.randint(0, y_range))
            if self.workspace.isInCollision(sample[0], sample[1]):
                self.vertex.append(sample)
                self.samples.append(sample)

                if self.compute_nearest_neighbours(500, 500, 100, sample[0], sample[1]):
                    self.configspace.drawConfiguration(sample[0], sample[1], 'green')
                else:
                    self.configspace.drawConfiguration(sample[0], sample[1], 'yellow')
                self.configspace.drawConfiguration(500, 500, 'red')
            else:
                self.configspace.drawConfiguration(sample[0], sample[1], 'black')

    def compute_nearest_neighbours(self, center_x, center_y, radius, x, y):
        dist = math.sqrt((center_x - x) ** 2 + (center_y - y) ** 2)
        return dist <= radius




