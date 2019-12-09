import math
import random
import csv
import numpy as np
import time
import copy

def read_data(filename):
    with open(file, 'r') as f:
        data_list = [line for line in csv.reader(f, delimiter='\t')]
        num_of_nodes = int(data_list[0][0])
        # Id Profit Weight
        total_weight_capacity = float(data_list[num_of_nodes + 1][0])
        data_list = np.asarray(data_list[1:num_of_nodes + 1])
        data_list = data_list.astype(np.float)
        np.set_printoptions(formatter={'float': lambda x: "{0:0.2f}".format(x)})
        return data_list, total_weight_capacity, num_of_nodes


def annealing_algorithm(number, total_weight_capacity, data_list, init_temp, epoch, cooling_rate):
    start_solution = create_initial_solution(data_list, total_weight_capacity)[0]
    best_profit, best_solution = simulate(start_solution, data_list, total_weight_capacity, init_temp, epoch, cooling_rate)
    best_combination = [0] * number
    for idx in best_solution:
        best_combination[idx] = 1
    return best_profit, best_combination


def create_initial_solution(data_list, total_weight_capacity):
    # pi / wi

    profit_vec = data_list[:, 1]
    weight_vec = data_list[:, 2]
    score = weight_vec / profit_vec

    indexSort = np.array(np.argsort(score))
    divSort = np.sort(score)

    sortedList = []
    for j in range(0, len(indexSort)):
        sortedList.append([indexSort[j], divSort[j]])

    initial_solution = []
    final_weight = 0
    final_profit = 0
    for i in range(len(sortedList) - 1, -1, -1):
        node = sortedList[i][0]
        if weight_vec[node] + final_weight <= total_weight_capacity:
            initial_solution.append(node)
            final_weight += weight_vec[node]
            final_profit += profit_vec[node]
    return initial_solution, final_weight, final_profit


def local_search_1(solution, data_list, total_weight_capacity):
    start_time = time.time()
    profit_vec = data_list[:, 1]
    weight_vec = data_list[:, 2]
    count_of_solution = 0
    improvement = False
    best_improvement = (0, 0, 0)
    # Swap: Remove one item from the knapsack, while inserting another item
    best_profit = sum(profit_vec[solution])
    for i in range(len(data_list)):
        for j in range(len(data_list) - 1):
            if (i in solution) & (j not in solution):
                temp_list = copy.deepcopy(solution)
                temp_list.remove(i)
                temp_list.append(j)
                out_of_knapsack = [node for node in range(len(data_list)) if node not in temp_list]
                for k in out_of_knapsack:
                    count_of_solution += 1
                    temp_list.append(k)
                    if sum(weight_vec[temp_list]) <= total_weight_capacity:
                        if sum(profit_vec[temp_list]) > best_profit:
                            best_profit = sum(profit_vec[temp_list])
                            best_improvement = (i, j, k)
                            improvement = True
                    temp_list.remove(k)
    if improvement:
        solution.remove(best_improvement[0])
        solution.append(best_improvement[1])
        solution.append(best_improvement[2])
    total_capacity = sum(weight_vec[temp_list])
    exec_time = time.time() - start_time
    return solution, improvement



def calculate_cost(solution, weight_profit):
    profit, weight = 0, 0
    for item in solution:
        profit += data_list[item][1]
        weight += data_list[item][2]
    return profit, weight


def simulate(solution, data_list, total_weight_capacity, init_temp, epoch, cooling_rate):

    temperature = init_temp

    best = copy.deepcopy(solution)
    best_profit = calculate_cost(solution, data_list)[0]

    current_sol = copy.deepcopy(solution)
    while True:
        current_best = calculate_cost(best, data_list)[0]
        for i in range(0, epoch):
            moves = local_search_1(current_sol, data_list, total_weight_capacity)[0]
            # idx = random.randint(0, len(moves) - 1)
            # random_move = moves[idx]
            delta = calculate_cost(moves, data_list)[0] - best_profit
            if delta > 0:
                best = copy.deepcopy(moves)
                best_profit = calculate_cost(best, data_list)[0]
                current_sol = copy.deepcopy(moves)
            else:
                if math.exp(delta / float(temperature)) > random.random():
                    current_sol = copy.deepcopy(moves)

        temperature *= cooling_rate
        if current_best >= best_profit or temperature <= termin_criteria:
            break
    return best_profit, best

if __name__ == '__main__':

    init_temp = 5000
    cooling_rate = 0.95
    epoch = 3
    termin_criteria = 0.001


    for file_no in range(1,7):
        input_file = "instance" + str(file_no) + ".txt"
        file = r'C:/Users/batuhan.organ/Desktop/IEOzU/IE504/IE504/Data/HW2/' + input_file
        data_list, total_weight_capacity, num_of_nodes = read_data(file)
        best_profit, best_combination = annealing_algorithm(num_of_nodes, total_weight_capacity, data_list, init_temp, epoch, cooling_rate)
    #todo automate for all experiments, store all results