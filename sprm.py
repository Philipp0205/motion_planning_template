import math
import time
from collections import deque
import random
import itertools
import networkx as nx

import numpy
from scipy import interpolate

import multiprocessing
from joblib import Parallel, delayed

from dijkstra import Graph, dijkstra, DijkstraSPF


class SPRM:
    def __init__(self, configspace, workspace):
        # stores all configuration s
        self.vertex = []
        self.graph = Graph()
        self.nodes = []

        self.vertex_no_colission = []
        self.vertex_in_colission = []

        self.configspace = configspace
        self.workspace = workspace

        self.add_start_goal_configurations()

        self.compute_samples(500, 1350, 980)

        samples = self.add_ids_to_samples(self.vertex_no_colission)

        neighbours_lengths = self.compute_nearest_neighbours(samples, 700)

        self.draw_free_graph(neighbours_lengths, samples)

        shortest_path = self.compute_shortest_path2(neighbours_lengths, samples)

        self.draw_path(shortest_path, samples)

    def draw_path(self, path, samples):
        shortest_path_samples = []
        for count in range(len(path)):
            if count + 1 < len(path):
                print(path[count] + " -> " + path[count + 1])
                self.configspace.draw_line(samples[int(path[count])][1], samples[int(path[count + 1])][1], "purple", 5)
                shortest_path_samples.append(samples[int(path[count])][1])
            else:
                shortest_path_samples.append(samples[int(path[count])][1])

        self.configspace.setIntialSolutionPath2(shortest_path_samples)

    def add_ids_to_samples(self, samples):
        result = []
        i = 0
        for s in samples:
            result.append([str(i), s])
            i += 1

        return result

    def get_samples_from_id(self, samples, id):
        return samples[int(id)]

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

        config_array = self.configspace.initConfig, self.configspace.goalConfig
        self.color_points(config_array, "red")

    def color_points(self, point_array, color):
        for point in point_array:
            self.configspace.drawConfiguration(point[0], point[1], color)

    def draw_lines(self, point_array, color):
        for point in point_array:
            self.configspace.draw_line(point[0], point[1], color)



    def add_start_goal_configurations(self):
        self.vertex_no_colission.append(self.configspace.initConfig)
        self.vertex_no_colission.append(self.configspace.goalConfig)

        print("Vertex after init : ")
        print(self.vertex_no_colission)

    def compute_length_of_two_points(self, sample_a, sample_b):
        center_x = sample_a[0]
        center_y = sample_a[1]
        x = sample_b[0]
        y = sample_b[1]

        return (x - center_x) ** 2 + (y - center_y) ** 2

    def create_nodes(self, neighbours):
        nodes = []
        i = 0

        for n in neighbours:
            nodes.append([i, i + 1, n[0], n[1], n[2]])
            i += 2

        return nodes

    def compute_nearest_neighbours(self, samples, radius):

        neighbour_lengths = []

        def compare(center_sample, sample, radius):
            length = self.compute_length_of_two_points(center_sample[1], sample[1])
            if length <= radius ** 2:
                if self.validate_edge(center_sample[1], sample[1]):
                    print("valid edge found")
                    # self.configspace.draw_line(center_sample[1], sample[1], "black")
                    neighbour_lengths.append([center_sample[0], sample[0], length])

        for center_sample, sample in itertools.combinations(samples, 2):
            compare(center_sample, sample, radius)

        return neighbour_lengths

    def validate_edge(self, segment_start, segment_end):
        # Quick and dirty

        t = 0
        range_t = 1
        while t <= range_t+0.1:
            cx = segment_start[0] + t * (segment_end[0] - segment_start[0])
            cy = segment_start[1] + t * (segment_end[1] - segment_start[1])
            if self.workspace.isRobotInCollision(round(cx), round(cy)):
                # self.configspace.drawConfiguration(round(cx), round(cy), "black")
                return False
            elif t > 0.99:
                # self.configspace.draw_line(segment_start, segment_end, "black")
                return True
            else:
                # self.configspace.drawConfiguration(round(cx), round(cy), "green")
                t +=0.1




            # print("CX: ", segment_start[0], " + ", segment_end[0], " - ", segment_start[0], " / ", n, " = ", cx)
            # print("CY: ", segment_start[1], " + ", segment_end[1], " - ", segment_start[1], " / ", n, " = ", cy)

            # if self.workspace.isInCollision(round(cx), round(cy)):
            #     self.configspace.draw_line(segment_start, (round(cx), round(cy)), "red")
            #     return False
            # elif n == 0:
            #     self.configspace.draw_line(segment_start, (cx,cy), "red")
            # else:
            #     n -= 17
            #     print(n)
            #     self.configspace.draw_line(segment_start, (cx,cy), "purple")
            #     create_linear_interpolation((cx, cy), n)


    def draw_free_graph(self, neighbours, samples):
        # Parallel(n_jobs=self.num_cores(delayed(self.draw_sample)(s, samples) for s in neighbours))

        def draw_sample(s, samples):
            sample1 = samples[int(s[0])]
            sample2 = samples[int(s[1])]
            self.configspace.draw_line(sample1[1], sample2[1], "black")
            self.configspace.draw_text(sample1[1], sample1[0])
            self.configspace.draw_text(sample2[1], sample2[0])

        for s in neighbours:
            sample1 = samples[int(s[0])]
            sample2 = samples[int(s[1])]
            self.configspace.draw_line(sample1[1], sample2[1], "blue")
            self.configspace.draw_text(sample1[1], sample1[0])
            self.configspace.draw_text(sample2[1], sample2[0])

            # for sample2 in neighbours:
            #  self.validate_edge(sample1, sample2, 10)

    def compute_shortest_path(self, neighbours_lengths, samples):

        graph = Graph()
        for n in neighbours_lengths:
            graph.add_edge(n[0], n[1], n[2])

        start = samples[0][0]
        end = samples [1][0]

        dijkstra = DijkstraSPF(graph, start)

        print("%-5s %-5s" % ("label", "distance"))
        for u in neighbours_lengths:
            print("%-5s %8d" % (u[0], dijkstra.get_distance(u[0])))

        print(" -> ".join(dijkstra.get_path(end)))

        return dijkstra.get_path(end)

    def compute_shortest_path2(self, neighbours_lengths, samples):
        G = nx.Graph()
        for n in neighbours_lengths:
            G.add_edge(n[0], n[1], weight=n[2])

        return nx.shortest_path(G, samples[0][0], samples[1][0], weight='weight')



