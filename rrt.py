import math
from workspace import Workspace
from configspace import Configspace
import numpy as np
import time
import random
from collections import defaultdict


class RRT:
    def __init__(self, configspace, workspace):
        print("RRT begins")
        self.workspace = workspace
        self.configspace = configspace
        self.init_pt = []
        self.goal_pt = []
        self.vertex = []
        self.add_start_goal_configurations()
        self.c_new = []
        self.range_max = 30
        self.time_max = 10
        self.c_new = self.init_pt
        self.rrt_alg(self.c_new, self.goal_pt, self.range_max)


    #Initial and goal points set
    def add_start_goal_configurations(self):
        self.init_pt = self.configspace.initConfig
        self.goal_pt = self.configspace.goalConfig
        self.vertex.append(self.init_pt)
        # Adding initial configuration to tree
        self.configspace.drawConfiguration(self.init_pt[0], self.init_pt[1], 'red')
        self.configspace.drawConfiguration(self.goal_pt[0], self.goal_pt[1], 'red')

    #RRT algorithm implementation
    def rrt_alg(self, c_new, goal, range_max):

        while c_new != self.goal_pt:
            #Generating random state

            self.c_rand = (random.randint(0, 1079), random.randint(0, 699))

            #Checking for random configurations with no collisions

            if (not self.workspace.isInCollision(self.c_rand[0], self.c_rand[1])):
                self.configspace.drawConfiguration(self.c_rand[0], self.c_rand[1], 'yellow')
                c_new = self.compute_nearest_neighbour(self.vertex, self.c_rand)

            #Generating c_near configurations

                if(self.edge_distance(self.c_rand, c_new) <= range_max):
                    self.c_near = self.c_rand
                else:
                    edge_distance_x = self.c_rand[0] - c_new[0]
                    edge_distance_y = self.c_rand[1] - c_new[1]
                    theta = math.atan2(edge_distance_y, edge_distance_x)
                    self.c_near = (int(c_new[0] + (range_max * math.cos(theta))), int(c_new[1] + (range_max * math.sin(theta))))

            #Validating Edges and adding c_new

                if (self.validate_edge(c_new, self.c_near)):
                    self.configspace.drawConfiguration(self.c_near[0], self.c_near[1], 'green')
                    self.configspace.draw_line(c_new, self.c_near, 'black')
                    c_new = self.c_near
                    self.vertex.append(c_new)

                    if(self.validate_edge(c_new, self.goal_pt)):
                        self.configspace.draw_line(c_new, self.goal_pt, 'black')
                        self.vertex.append(self.goal_pt)
                        break
        #Nodes of the Tree
        print(self.vertex)

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
            elif t > 0.9:
                # self.configspace.draw_line(segment_start, segment_end, "black")
                return True
            else:
                # self.configspace.drawConfiguration(round(cx), round(cy), "green")
                t +=0.1


    def color_points(self, point_array, color):
        for point in point_array:
            self.configspace.drawConfiguration(point[0], point[1], color)

    def compute_nearest_neighbour(self, vertices, c_rand):
        min_distance = self.edge_distance(self.init_pt, c_rand)
        nearest_neighbour = self.init_pt
        for vertex in vertices:
            distance = self.edge_distance(vertex, c_rand)
            if (min_distance > distance):
                nearest_neighbour = vertex
        return nearest_neighbour

    def edge_distance(self, point_a, point_b):
        point_a = np.array(point_a)
        point_b = np.array(point_b)
        distance = np.linalg.norm(point_a - point_b)
        return distance












