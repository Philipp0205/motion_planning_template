import math
import time
import numpy as np


def get_c1_random_config():
    mu, sigma = 0, 600
    gaussian_distribution = np.random.normal(mu, sigma, 1000)

    low, high = 0, 979
    uniform_distribution = np.random.uniform(low, high, 1000)

    low_rand, high_rand = 0, 999
    rand_index_gaussian = np.random.randint(low_rand, high_rand)
    rand_index_uniform = np.random.randint(low_rand, high_rand)

    # init ct and cr
    ct = round(gaussian_distribution[rand_index_gaussian])
    cr = round(uniform_distribution[rand_index_uniform])

    # check if ct or cr is negative or out of bounds and assign new values from the arrays
    while ct < 0 or cr < 0 or ct > 1349 or cr > 979:
        ct = round(gaussian_distribution[np.random.randint(low_rand, high_rand)])
        cr = round(uniform_distribution[np.random.randint(low_rand, high_rand)])

    return ct, cr


def get_distance_d_from_normal_distribution():
    mu, sigma = 0, 10
    normal_distribution = np.random.normal(mu, sigma, 1000)

    rand_index = np.random.randint(0, 999)
    distance_d = round(normal_distribution[rand_index])

    return distance_d


def get_c2_config(c1_ct, c1_cr):
    distance_d = get_distance_d_from_normal_distribution()

    ct_ = c1_ct + distance_d

    while ct_ > 1349:
        distance_d = get_distance_d_from_normal_distribution()
        ct_ = c1_ct + distance_d

    circle_from_c1_with_distance_d = get_points_on_circumference(distance_d, c1_ct, c1_cr)

    if len(circle_from_c1_with_distance_d) > 0:
        rand_index = np.random.randint(0, len(circle_from_c1_with_distance_d) - 1)
        choose_random_point_on_circumference = circle_from_c1_with_distance_d[rand_index]
        cr = choose_random_point_on_circumference[1]
        return ct_, cr
    else:
        cr = c1_cr
        return ct_, cr


def get_points_on_circumference(distance, x_coordinate, y_coordinate):
    pi = math.pi
    n = round(distance / 2) + 1
    circumference_points = []

    if x_coordinate + distance < 1350 and y_coordinate + distance < 980 and n > 0:
        for x in range(0, n + 1):
            single_circum_point = round((math.cos(2 * pi / n * x) * distance) + x_coordinate), round(
                (math.sin(2 * pi / n * x) * distance) + y_coordinate)
            circumference_points.insert(x, single_circum_point)

    return circumference_points


class GaussianSampling:
    def __init__(self, configspace, workspace):
        self.configspace = configspace
        self.workspace = workspace

        self.benchmark_gaussian_sampling_2()

    def gaussian_sampling_2(self, n):
        graph_samples = []

        # loop
        for x in range(0, n + 1, 1):
            # c1 (ct, cr) a random config after --> ct: gaussian_distrib, cr: uniform_distrib
            c1 = get_c1_random_config()
            c1_ct, c1_cr = c1[0], c1[1]

            # c2 (ct',cr) config after --> with ct': ct + distance_d, cr: valid y point random
            # from circumference method of point c1
            c2 = get_c2_config(c1_ct, c1_cr)
            c2_ct, c2_cr = c2[0], c2[1]

            # robot in collision
            # c1_in_c_free = not self.workspace.isRobotInCollision2(c1_ct, c1_cr)
            # c2_in_c_free = not self.workspace.isRobotInCollision2(c2_ct, c2_cr)

            # normal in collision
            c1_in_c_free = not self.workspace.isInCollision(c1_ct, c1_cr)
            c2_in_c_free = not self.workspace.isInCollision(c2_ct, c2_cr)

            if c1_in_c_free and not c2_in_c_free:
                graph_samples.insert(x, c1)
            elif c2_in_c_free and not c1_in_c_free:
                graph_samples.insert(x, c2)
            else:
                c1 = None
                c2 = None

        self.draw_point_of_array(graph_samples)
        return len(graph_samples)

    def draw_point_of_array(self, array):
        if array is not None:
            for x in array:
                self.configspace.drawConfiguration(x[0], x[1], "Yellow")

    def benchmark_gaussian_sampling_2(self):
        start = time.perf_counter()
        sample_count = self.gaussian_sampling_2(100000)
        print(sample_count, "Actual samples created")
        print(f"Completed Execution in {time.perf_counter() - start} seconds")