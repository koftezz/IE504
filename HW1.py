import os
import io
import numpy as np
import math


file = 'C:/Users/batuhan.organ/Desktop/IE OzU/IE 504/IE 504/Data/Q1_Data.txt'


def read_data(filename):
    with open(file) as f:
        points = []
        dataset_list = f.read().splitlines()
        numOfNodes = len(dataset_list)
        dataset_list = ' '.join(dataset_list)
        for item in dataset_list.split(' '):  # comma, or other
            points.append(float(item))

        points = np.array(points)
        points = points.reshape(numOfNodes, 3)
        demand = points[:, [2]]
        points = points[:, [0, 1]]
    return points, demand, numOfNodes


def euclid_distance(x, y):
    return math.sqrt((x[0] - y[0]) ** 2 + (x[1] - y[1]) ** 2)

def dist_matrix(points):
    dist_matrix = np.asarray([[euclid_distance(point1, point2) for point2 in points] for point1 in points])
    return dist_matrix

if __name__ == '__main__':

    points, demand, numOfNodes = read_data(file)
    dist_matrix = dist_matrix(points)

    unVisited_list = [i for i in range(1, numOfNodes)]
    Result_list = []
    Capacity_list = []
    Distance_list = []
    Control = True
    assigned_node = 0
    vehicle = 0
    distance = 500
    capacity = 2000

    while unVisited_list:
        vehicle += 1
        temp_list = [0]
        total_distance = 0.0
        total_capacity = 0.0
        nearest_node_distance = 0
        Control = True

        while Control:
            for i in unVisited_list:
                if ((dist_matrix[temp_list[-1], i] < nearest_node_distance) or (0 == unVisited_list.index(i))):
                    nearest_node = i
                    nearest_node_distance = dist_matrix[temp_list[-1], i]
                    nearest_node_capacity = demand[i]
                    back_to_depot = dist_matrix[i, 0]
            if (total_distance + nearest_node_distance + back_to_depot < distance) and (total_capacity + nearest_node_capacity < capacity)\
                    and (assigned_node < numOfNodes - 1):
                assigned_node = assigned_node + 1
                temp_list.append(nearest_node)
                total_distance += nearest_node_distance
                total_capacity += nearest_node_capacity
                unVisited_list.remove(nearest_node)
            else:
                #add depot at the end of the route
                temp_list.append(0)
                Result_list.append(temp_list)
                Capacity_list.append(total_capacity.item())
                Distance_list.append(total_distance.item())
                del temp_list
                Control = False
    print(Result_list, Capacity_list, Distance_list)


