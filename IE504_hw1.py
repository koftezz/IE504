import os
import io
import random

import numpy as np
import math
from scipy.spatial import distance_matrix

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

def truck(numOfTrucks, truck_capacity, truck_distance):
    truck_capacity_vec = [2000 for capacity in range(numOfTrucks)]
    truck_distance_vec = [500 for capacity in range(numOfTrucks)]
    return numOfTrucks, truck_capacity_vec, truck_distance_vec

# should be at least 5 since total demand / truck capacity: 8752.2 / 2000 = 4.37
#numOfTrucks, truck_capacity_vec, truck_distance_vec = truck(5, 2000, 500)

def euclid_distance(x, y):
    return math.sqrt((x[0] - y[0]) ** 2 + (x[1] - y[1]) ** 2)

def dist_matrix(points):
    dist_matrix = np.asarray([[euclid_distance(point1, point2) for point2 in points] for point1 in points])
    return dist_matrix

def length(tour, distance_matrix):
    z = distance_matrix[tour[-1], tour[0]]    # edge from last to first city of the tour
    for i in range(1, len(tour)):
        z += distance_matrix[tour[i], tour[i-1]]      # add length of edge from city i-1 to i
    return z

def Nearest_neighbor_search(demand, dist_matrix):
    
    dist_matrix = dist_matrix(points)
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

    # Nearest_neighbor_search(demand, dist_matrix)

    # dist_matrix = dist_matrix(points)
    # print(np.argmin(dist_matrix[0, 1:20])+1)

    file = 'C:/Users/Eren/Downloads/Q1_Data.txt'

    points, demand, numOfNodes = read_data(file)
    dist_matrix = dist_matrix(points)
    unVisited_list = [i for i in range(1, 20)]
    Result_list = []
    Result_tour_length =[]
    Result_tour_volume =[]

    Control2 = True
    assigned_node = 0

    # for vehicle in range(1, 20):
    while Control2:

        temp_list = [0]
        total_distance = 0.0
        total_capacity = 0.0
        nearest_node_distance = 0
        bestCost = 0
        Control = True

        nearest_node = np.argmin(dist_matrix[0, unVisited_list])
        nearest_node = unVisited_list[nearest_node]
        assigned_node = assigned_node + 1
        temp_list.append(nearest_node)
        total_distance += dist_matrix[0, nearest_node]
        total_capacity += demand[nearest_node]
        unVisited_list.remove(nearest_node)

        while Control:

            if assigned_node == 19:
                temp_list.append(0)
                total_distance += dist_matrix[temp_list[-1], 0]

                Result_list.append(temp_list)
                Result_tour_length.append(total_distance)
                Result_tour_volume.append(total_capacity)

                del temp_list
                Control = False
                Control2 = False
                break
            new_node = random.choice(unVisited_list)
            nearest_node_capacity = demand[new_node]

            for j in range(len(temp_list) - 1):
                cost = dist_matrix[temp_list[j], new_node] + dist_matrix[new_node, temp_list[j + 1]] - dist_matrix[
                    temp_list[j], temp_list[j + 1]]

                if (cost < bestCost) or (j == 0):
                    bestCost = cost
                    insert_index = j

            if (total_distance + bestCost + dist_matrix[temp_list[-1], 0] < 500) and (
                            total_capacity + nearest_node_capacity < 2000) and (assigned_node < 19):

                assigned_node += 1
                temp_list.append(new_node)
                total_distance += bestCost
                total_capacity += nearest_node_capacity
                unVisited_list.remove(new_node)

            else:
                temp_list.append(0)
                total_distance += dist_matrix[temp_list[-1], 0]

                Result_list.append(temp_list)
                Result_tour_length.append(total_distance)
                Result_tour_volume.append(total_capacity)

                del temp_list
                Control = False
                if assigned_node == 19:
                    Control2 = False

    print('\n', "------------ Ouestion-1 Part a Result ------------")
    print("Result List:", Result_list)
    print("Tour length:", Result_tour_length)
    print("Tour Volume:", *Result_tour_volume)
    print("Required Vehicle Number: ", len(Result_list), '\n')


    print("------------ Ouestion-1 Part b Result ------------")

for iteration in range(5):
    best_saving = 0
    best_i, best_j, best_k = [0 for _ in range(3)]

    for i in range(len(Result_list)):
        for j in range(1, len(Result_list[i])-2):
            vehicle_1 = Result_list[i][j]

            for k in range(j+1, len(Result_list[i]) - 1):
                vehicle_2 = Result_list[i][k]

                #print("i:", i, "j:", j, "k:", vehicle_1, "-", vehicle_2)

                if j+1==k:
                    saving = (dist_matrix[Result_list[i][j - 1], vehicle_2] + dist_matrix[vehicle_1, Result_list[i][k + 1]]) -\
                             (dist_matrix[Result_list[i][j-1], vehicle_1] + dist_matrix[vehicle_2, Result_list[i][k+1]])
                else:
                    saving = (dist_matrix[Result_list[i][j - 1], vehicle_2] + dist_matrix[vehicle_2, Result_list[i][j + 1]]
                              + dist_matrix[Result_list[i][k - 1], vehicle_1] + dist_matrix[vehicle_1, Result_list[i][k + 1]]) -\
                             (dist_matrix[Result_list[i][j-1], vehicle_1] + dist_matrix[vehicle_1, Result_list[i][j+1]] \
                             + dist_matrix[Result_list[i][k-1], vehicle_2] + dist_matrix[vehicle_2, Result_list[i][k+1]])


                if saving < best_saving:
                    best_saving = saving
                    best_i = i
                    best_j = j
                    best_k = k


    print("--- Iteration", iteration + 1, " ---")
    #print(best_i, best_j, best_k)

    print("Before Swap: ", Result_list)

    temp = Result_list[best_i][best_j]
    temp2 = Result_list[best_i][best_k]

    Result_list[best_i][best_j] = temp2
    Result_list[best_i][best_k] = temp
    print("After  Swap: ", Result_list)

    if best_saving < 0:
        print("Changed Vehicle :", best_i+1)

    print("Saving: ", -best_saving, '\n')

