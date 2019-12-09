import time
from random import randint
from gurobipy import *
import numpy as np
import csv
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
        return data_list, total_weight_capacity


def enumerate(data_list):

    item_list = [0 for i in range(len(data_list))]
    profit = 0
    best_profit = 0
    best_item_list = []
    count_of_solution = 1
    profit_vec = list(data_list[:, 1])
    weight_vec = list(data_list[:, 2])
    start_time = time.time()
    for i1 in range(2):
        item_list[0] = i1
        for i2 in range(2):
            item_list[1] = i2
            for i3 in range(2):
                item_list[2] = i3
                for i4 in range(2):
                    item_list[3] = i4
                    for i5 in range(2):
                        item_list[4] = i5
                        for i6 in range(2):
                            item_list[5] = i6
                            for i7 in range(2):
                                item_list[6] = i7
                                for i8 in range(2):
                                    item_list[7] = i8
                                    for i9 in range(2):
                                        item_list[8] = i9
                                        for i10 in range(2):
                                            item_list[9] = i10
                                            for i11 in range(2):
                                                item_list[10] = i11
                                                for i12 in range(2):
                                                    item_list[11] = i12
                                                    for i13 in range(2):
                                                        item_list[12] = i13
                                                        for i14 in range(2):
                                                            item_list[13] = i14
                                                            for i15 in range(2):
                                                                item_list[14] = i15
                                                                for i16 in range(2):
                                                                    item_list[15] = i16
                                                                    for i17 in range(2):
                                                                        item_list[16] = i17
                                                                        for i18 in range(2):
                                                                            item_list[17] = i18
                                                                            for i19 in range(2):
                                                                                item_list[18] = i19
                                                                                for i20 in range(2):
                                                                                    item_list[19] = i20
                                                                                    profit = sum([a*b for a, b in zip(profit_vec, item_list)])
                                                                                    count_of_solution += 1
                                                                                    if (profit > best_profit) & \
                                                                                            (total_weight_capacity >= sum([a*b for a, b in zip(weight_vec, item_list)])):
                                                                                        best_profit = profit
                                                                                        best_item_list = copy.deepcopy(item_list)
    exec_time = time.time() - start_time

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

def exact_knapsack(data_list):
    Final_Profit = []
    Final_Weight = []
    Final_Variable_List = []
    p = []
    w = []

    for i in data_list[:, 1]:
        p.append(i)

    for i in data_list[:, 2]:
        w.append(i)

    # define data coefficients
    c_w = total_weight_capacity

    # create empty model
    m = Model()

    # add decision variables
    # <VARIABLES ADDED HERE>
    x = m.addVars(len(data_list), vtype=GRB.BINARY, name='x')
    m.update()
    # set objective function
    # <OBJECTIVE SET HERE>
    m.setObjective(x.prod(p), GRB.MAXIMIZE)
    m.update()
    # add constraint
    # <CONSTRAINT ADDED HERE>
    m.addConstr(x.prod(w) <= c_w, name='weight_const')
    m.update()
    # solve model
    m.optimize()

    # display solution
    if m.SolCount > 0:
        m.printAttr('X')

    variable_list = []
    counter, weight = [0 for _ in range(2)]
    for v in m.getVars():
        counter += 1
        if v.x > 0:
            weight += w[counter - 1]
            variable_list.append(counter)

    Final_Profit.append(m.objVal)
    Final_Weight.append(weight)
    Final_Variable_List.append(variable_list)
    return Final_Profit, Final_Weight, Final_Variable_List

#todo enumerate

def local_search_1(data_list, solution):
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
    return solution, count_of_solution, best_profit, total_capacity, exec_time


def local_search_2(data_list, solution):
    start_time = time.time()
    profit_vec = data_list[:, 1]
    weight_vec = data_list[:, 2]
    count_of_solution = 1
    total_capacity = sum(weight_vec[solution])
    # Swap: Remove one item from the knapsack, while inserting another item
    best_profit = sum(profit_vec[solution])

    while True:
        i = solution[randint(0, len(solution) - 1)] # select from the knapsack
        j = randint(0, len(data_list) - 1)
        # select j out of the knapsack
        while j in solution:
            j = randint(0, len(data_list) - 1)

        temp_list = copy.deepcopy(solution)
        temp_list.remove(i) # remove from the knapsack
        temp_list.append(j) # add to knapsack from outer scope

        # Add an item which is not in the knapsack
        out_of_knapsack = [node for node in range(len(data_list)) if (node not in temp_list) & (node != i)]

        k = out_of_knapsack[randint(0, len(out_of_knapsack) - 1)]
        count_of_solution += 1
        temp_list.append(k)

        if sum(weight_vec[temp_list]) <= total_weight_capacity:
            if sum(profit_vec[temp_list]) >= best_profit:
                best_profit = sum(profit_vec[temp_list])
                total_capacity = sum(weight_vec[temp_list])
                solution.remove(i)
                solution.append(j)
                solution.append(k)
                break
        if time.time() - start_time > 1200:
            print("time out")
            best_profit = 0
            total_capacity = 0
            solution = []
            break
    exec_time = time.time() - start_time
    return solution, count_of_solution, best_profit, total_capacity, exec_time



if __name__ == '__main__':

    for file_no in range(2, 4):
        result_1 = {}
        result_2 = {}
        result = {}
        input_file = "instance" + str(file_no) + ".txt"
        file = r'C:/Users/batuhan.organ/Desktop/IEOzU/IE504/IE504/Data/HW2/' + input_file
        data_list, total_weight_capacity = read_data(file)
        initial_solution, final_weight, final_profit = create_initial_solution(data_list, total_weight_capacity)
        # exact_profit, exact_weight, exact_soln = exact_knapsack(data_list)
        # result = {file_no: {'Solution List': exact_soln, 'Final Profit': exact_profit, \
        #                       'Final Weight': exact_weight}}
        #
        # result_file = "C:/Users/batuhan.organ/Desktop/IEOzU/IE504/IE504/Output/HW2_Q1/result_file_exact_" + str(
        #     file_no) + ".txt"
        # f = open(result_file, "w")
        # f.write("Final_Profit Final_Weight\n")
        # L = str(exact_profit[0]) + " " + str(exact_weight[0])
        # f.writelines(L)
        # f.write("\n")
        # f.write("Final Variable List\n")
        # f.writelines(str(exact_soln[0]))
        # f.close()
        #
        # local_1_solution, count_of_solution, best_profit, total_capacity, exec_time = local_search_1(data_list, initial_solution)
        # result_1 = {file_no: {'Solution List': local_1_solution, 'Final Profit': best_profit, \
        #                     'Final Weight': total_capacity, 'Count of Solution': count_of_solution, 'Time': exec_time}}
        #
        # result_file = "C:/Users/batuhan.organ/Desktop/IEOzU/IE504/IE504/Output/HW2_Q1/result_file_LS1_" + str(file_no) + ".txt"
        # f = open(result_file, "w")
        # result_string = ''
        # for y in result_1[file_no]:
        #     result_string = result_string + y + ':' + str(result_1[file_no][y]) + '\n'
        # f.write(result_string)
        # f.close()


        local_2_solution, count_of_solution, best_profit, total_capacity, exec_time = local_search_2(data_list,
                                                                                                     initial_solution)
        result_2 = {file_no: {'Solution List': local_2_solution, 'Final Profit': best_profit, \
                              'Final Weight': total_capacity, 'Count of Solution': count_of_solution,
                              'Time': exec_time}}
        result_file = "C:/Users/batuhan.organ/Desktop/IEOzU/IE504/IE504/Output/HW2_Q1/result_file_LS2_" + str(
            file_no) + ".txt"
        f = open(result_file, "w")
        result_string = ''
        for y in result_2[file_no]:
            result_string = result_string + y + ':' + str(result_2[file_no][y]) + '\n'
        f.write(result_string)
        f.close()