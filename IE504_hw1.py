import os
import io
import numpy as np
import math
from scipy.spatial import distance_matrix


file = 'C:/Users/Eren/Downloads/Q1_Data.txt'


def read_data(filename):
    with open(file) as f:
        points = []
        dataset_list = f.read().splitlines()
        numOfNodes = len(dataset_list)
        dataset_list = ' '.join(dataset_list)
        for item in dataset_list.split(' '):  # comma, or other
            points.append(float(item))

        points = np.array(points)
        points = points.reshape(numOfNodes,3)
        demand = points[:, [2]]
        points = points[:, [0, 1]]
    return points, demand, numOfNodes

points, demand, numOfNodes = read_data(file)


def truck(numOfTrucks, truck_capacity, truck_distance):
    truck_capacity_vec = [2000 for capacity in range(numOfTrucks)]
    truck_distance_vec = [500 for capacity in range(numOfTrucks)]
    return numOfTrucks, truck_capacity_vec, truck_distance_vec

# should be at least 5 since total demand / truck capacity: 8752.2 / 2000 = 4.37
numOfTrucks, truck_capacity_vec, truck_distance_vec = truck(5, 2000, 500)

def euclid_distance(x, y):
    return math.sqrt((x[0] - y[0]) ** 2 + (x[1] - y[1]) ** 2)

def dist_matrix(points):
    dist_matrix = np.asarray([[euclid_distance(point1, point2) for point2 in points] for point1 in points])
    return dist_matrix

dist_matrix = dist_matrix(points)

visited = np.array([0])
unvisited = np.arange(1,20)

#
# for point1 in points:
#     points.where(points = point1)
#     unvisited.append(point1)
#
# C = []
# n = [0,9, 15, 17, 19, 4, 5]


def length(tour, distance_matrix):
    z = distance_matrix[tour[-1], tour[0]]    # edge from last to first city of the tour
    for i in range(1, len(tour)):
        z += distance_matrix[tour[i], tour[i-1]]      # add length of edge from city i-1 to i
    return z

def Nearest_neighbor_search(demand, dist_matrix):
    unVisited_list = [i for i in range(1, 20)]
    Result_list = []
    Control2 = True
    assigned_node = 0

    #for vehicle in range(1, 20):
    while Control2:

        temp_list = [0]
        total_distance = 0.0
        total_capacity = 0.0
        nearest_node_distance = 0
        Control = True

        while Control:

            for i in unVisited_list:
                if (dist_matrix[temp_list[-1], i] < nearest_node_distance) or (0 == unVisited_list.index(i)):
                    # nearest_node = unVisited_list.index(i)
                    nearest_node = i
                    nearest_node_distance = dist_matrix[temp_list[-1], i]
                    nearest_node_capacity = demand[i]


            if (total_distance + nearest_node_distance + dist_matrix[nearest_node, 0] < 500) and (total_capacity + nearest_node_capacity < 2000) and (assigned_node < 19):

                assigned_node = assigned_node + 1
                temp_list.append(nearest_node)
                total_distance += nearest_node_distance
                total_capacity += nearest_node_capacity
                # unVisited_list.remove(unVisited_list[nearest_node])
                unVisited_list.remove(nearest_node)

            else:
                temp_list.append(0)
                total_distance += dist_matrix[nearest_node, 0]

                Result_list.append(temp_list)
                del temp_list
                Control = False
                if assigned_node == 19:
                    Control2 = False

    print(Result_list)



if __name__ == '__main__':
    #print dist_matrix, "\n", points, "\n", demand, "\n", numOfNodes

    Nearest_neighbor_search(demand, dist_matrix)

    # listoflists = []
    # a_list = []
    # for i in range(0, 10):
    #     a_list.append(i)
    #     if len(a_list) > 3:
    #         a_list.remove(a_list[0])
    #         listoflists.append((list(a_list), a_list[0]))
    # print listoflists




