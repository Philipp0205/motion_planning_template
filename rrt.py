import math
from workspace import Workspace
from configspace import Configspace
import time


class RRT:
    def __init__(self, configspace, workspace):
        print("RRT begins")
        self.workspace = workspace
        self.configspace = configspace
        self.init_pt = []
        self.goal_pt = []
        self.vertex = []
        self.add_start_goal_configurations()
        self.range_max = 50
        #self.c_near = self.init_pt
        self.rrt_alg(self.init_pt, self.range_max, 5)

    #Initial and goal points set
    def add_start_goal_configurations(self):
        self.init_pt = self.configspace.initConfig
        self.goal_pt = self.configspace.goalConfig

    #RRT algorithm implementation
    def rrt_alg(self, c_near, range_max, t_max):
        #Adding inital configuration to tree
        self.vertex.append(self.init_pt)

        #All configurations within distance rangemax
        self.sample_arr = self.get_x_y_co(c_near, range_max)

        #Setting the time element based on current time
        t_end = time.time() + t_max

        #RRT timeout check
        while time.time() < t_end:

            #Check for configurations with no collisions, must include condition to check for valid edges
            for c_rand in self.sample_arr:
                if(not self.workspace.isInCollision(c_rand[0], c_rand[1]) )and (not self.validate_edge(c_near, c_rand, 10)):
                    print("c_near found")
                    c_near = c_rand
                    self.vertex.append(c_near)
                    break

            #Checking if goal reached before time out
            if (c_near != self.goal_pt):
                print("neighbour not goal")
                print(c_near)
                self.rrt_alg(c_near, self.range_max, t_max-1)
            else:
                print("Neighbour is goal")
            break
        #vertex contains all valid configurations within timeout along with initial and goal configurations
        #Must add logic
        # 1. to draw configurations and lines obtained
        # 2. to find path from init to goal using vertex
        # 3. Maybe instead of taking samples along the circumference of range_max, can use gaussian sampling

        self.vertex.append(self.goal_pt)
        print(self.vertex)
        print(self.init_pt, self.goal_pt)
        print("RRT Timeout")
        #self.color_points(self.vertex, "red")
        return self.vertex

    #Computes all points along the circumference of range_max distance of RRT
    def get_x_y_co(self, c_near, range_max):
        self.xc = c_near[0]  # x-co of circle (center)
        self.yc = c_near[1]  # y-co of circle (center)
        self.r = range_max  # radius of circle
        self.sample = []
        for i in range(360):
            self.y = self.yc + self.r * math.cos(i)
            self.x = self.xc + self.r * math.cos(i)
            self.x = int(self.x)
            self.y = int(self.y)
            # Create array with all the x-co and y-co of the circle
            self.sample.append([self.x, self.y])
        return self.sample


    def validate_edge(self, sampleA, sampleB, n):
        segment_start = sampleA
        segment_end = sampleB
        def create_linear_interpolation(n):
            cx = segment_start[0] + (segment_end[0] - segment_start[0]) / n
            cy = segment_start[1] + (segment_end[1] - segment_start[1]) / n

            if self.workspace.isInCollision(round(cx), round(cy)):
                self.configspace.draw_line(segment_start, segment_end, "red")
                return True
            elif segment_start[0] == segment_end[0] & segment_start[1] == segment_end[1]:
                self.configspace.draw_line(segment_start, segment_end, "green")
                return False

    # while (self.distance == range_max) or (self.collision_status):
    # print("In collision sample")
    # self.crand = (random.randint(self.rangexmin, self.rangeymin), random.randint(self.rangexmax, self.rangeymax))
    # self.crand = (random.randint(763, 1079), random.randint(963, 699))
    # point_a = np.array(self.cnear)
    # point_b = np.array(self.crand)
    # self.distance = np.linalg.norm(point_a - point_b)
    # print(self.distance)
    # self.collision_status = self.workspace.isInCollision(self.crand[0], self.crand[1])
    # print(self.collision_status)
    # print("neighbour with distance d found")









