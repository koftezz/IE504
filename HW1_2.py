import os
import io
import numpy as np
import csv


def read_data(filename):
    with open(file, 'r') as f:
        data_list = [line for line in csv.reader(f, delimiter='\t')]
        num_of_nodes = int(data_list[0][0])
        total_weight_capacity = float(data_list[num_of_nodes + 1][0])
        total_volume_capacity = float(data_list[num_of_nodes + 2][0])
        data_list = np.asarray(data_list[1:num_of_nodes + 1])
        data_list = data_list.astype(np.float)
        np.set_printoptions(formatter={'float': lambda x: "{0:0.2f}".format(x)})
        return data_list, total_volume_capacity, total_weight_capacity


# data_list: Id, weight, volume, profit

def multi_knapsack(data_list, total_volume_capacity, total_weight_capacity):
    weight_vec = data_list[:, 1]
    volume_vec = data_list[:, 2]
    profit_vec = data_list[:, 3]

    # Equation: (Value/weight)/(Σ(val/w)) + (Value/vol)/(Σ(val/vol))
    sum_weight = sum(profit_vec / weight_vec)
    sum_volume = sum(profit_vec / volume_vec)

    coef_vec = ((profit_vec / weight_vec) / sum_weight) + ((profit_vec / volume_vec) / sum_volume)

    indexSort = np.array(np.argsort(coef_vec))
    divSort = np.sort(coef_vec)

    sortedList = []
    for j in range(0, len(indexSort)):
        sortedList.append([indexSort[j], divSort[j]])

    final_list = []
    final_weight = 0
    final_volume = 0
    final_profit = 0
    for i in range(len(sortedList)-1, -1, -1):
        node = sortedList[i][0]
        if (weight_vec[node] + final_weight <= total_weight_capacity) & \
                (volume_vec[node] + final_volume <= total_volume_capacity):
            final_list.append(node+1)
            final_volume += volume_vec[node]
            final_weight += weight_vec[node]
            final_profit += profit_vec[node]

    return final_volume, final_weight, final_list, final_profit


if __name__ == '__main__':

    for file_no in range(1, 13):

        result = {}
        input_file = "mkdp" + str(file_no) + ".txt"
        file = r'C:/Users/batuhan.organ/Desktop/IEOzU/IE504/IE504/Data/HW1_Q2_input/' + input_file
        data_list, total_volume_capacity, total_weight_capacity = read_data(file)
        final_volume, final_weight, final_list, final_profit = multi_knapsack(data_list, total_volume_capacity, \
                                                                             total_weight_capacity)

        result = {file_no: {'Final List': final_list, 'Final Profit': final_profit, \
                              'Final Weight': final_weight, 'Final Volume': final_volume}}
        result_file = "C:/Users/batuhan.organ/Desktop/IEOzU/IE504/IE504/Output/HW1_Q2/result_file_"+str(file_no)+".txt"
        f = open(result_file, "w")
        result_string = ''
        for y in result[file_no]:
            result_string = result_string + y+ ':'+ str(result[file_no][y]) +'\n'
        f.write(result_string)
        f.close()


