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
        self.c_near = self.init_pt
        self.rrt_alg(200, 5)

    #Initial and goal points set
    def add_start_goal_configurations(self):
        self.init_pt = self.configspace.initConfig
        self.goal_pt = self.configspace.goalConfig

    #RRT algorithm implementation
    def rrt_alg(self, range_max, t_max):
        #Adding inital configuration to tree
        self.vertex.append(self.init_pt)

        #All configurations within distance rangemax
        self.sample_arr = self.get_x_y_co(self.c_near, range_max)

        #Setting the time element based on current time
        t_end = time.time() + t_max

        #RRT timeout check
        while time.time() < t_end:

            #Check for configurations with no collisions, must include condition to check for valid edges
            for c_rand in self.sample_arr:
                if(not self.workspace.isInCollision(c_rand[0], c_rand[1])):
                    print("c_near found")
                    self.c_near=c_rand
                    print(self.c_near)
                    self.vertex.append(self.c_near)
                    break

            #Checking if goal reached before time out
            if (self.c_near != self.goal_pt):
                print("neighbour not goal")
                self.rrt_alg(range_max,t_max-1)
            else:
                print("Neighbour is goal")
                print(self.vertex)
                break
        #vertex contains all valid configurations within timeout along with initial and goal configurations
        #Must add logic
        # 1. to draw configurations and lines obtained
        # 2. to check for valid edges
        # 3. to find path from init to goal using vertex
        # 4. Maybe instead of taking samples along the circumference of range_max, can use gaussian sampling

        self.vertex.append(self.goal_pt)
        print("RRT Timeout")
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









