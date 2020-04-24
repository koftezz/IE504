import numpy as np
import os
import csv
from gurobipy import *
import math


def read_data(filename):
    with open(file, 'r') as f:
        data_list = [line for line in csv.reader(f, delimiter='\t')]
        data_list = np.asarray(data_list[:])
        data_list = data_list.astype(np.float)
        np.set_printoptions(formatter={'float': lambda x: "{0:0.2f}".format(x)})
        return data_list


def euclid_distance(x, y):
    return math.sqrt((x[0] - y[0]) ** 2 + (x[1] - y[1]) ** 2)


def dist_matrix(points):
    dist_matrix = np.asarray([[euclid_distance(point1, point2) for point2 in points] for point1 in points])
    return dist_matrix


input_file = "test_input.txt"

file = r'C:/Users/batuhan.organ/Desktop/IEOzU/IE504/IE504/Inputs/' + input_file
data_list = read_data(file)

file = r'C:/Users/batuhan.organ/Desktop/IEOzU/IE504/IE504/Inputs/test_input_dist.txt'
data_list2 = read_data(file)

node_list = []
x_list = []
y_list = []
priority_list = []

for i in range(len(data_list)):
    node_list.append(data_list[i, 0])
    x_list.append(data_list[i, 1])
    y_list.append(data_list[i, 2])
    priority_list.append(data_list[i, 3])

dist_matrix = dist_matrix(data_list2)

N = 20  # num of nodes
depot = 0
end_depot = N + 1
RS = 4

V_R = [end_depot + i + 1 for i in range(RS)]  # set of recharge stations
V_F = [i for i in range(1, N+1)]  # set of all nodes
V_F_0 = V_F.copy()
V_F_0.insert(0, depot)
# V_F + V_R
V_0 = V_F + V_R

# same as V_0
V = V_0.copy()
V_0.insert(0,0)
# Set of visits to recharging stations, dummy vertices of set of
# recharging stations RS
V_R_Prime = []
upper_bound_rs = 5

for i in V_R:
    for j in range(upper_bound_rs):
        V_R_Prime.append(i)

for i in range(0, len(V_R_Prime) - 1):
    V_R_Prime[i+1] = V_R_Prime[i] + 1

V_Prime_0_N = V_F.copy()
V_Prime_0_N.insert(0, depot)
V_Prime_0_N = V_Prime_0_N + V_R_Prime
V_Prime_0_N.append(end_depot)
V_Prime_0_N.append(42)  # dummy end depot

V_Prime = V_F + V_R_Prime

# outflow
V_0_Prime = V_F.copy()
V_0_Prime.insert(0, depot)
V_0_Prime = V_0_Prime + V_R_Prime

# inflow
V_Prime_N = V_F.copy()
V_Prime_N = V_Prime_N + V_R_Prime
V_Prime_N.append(end_depot)
V_Prime_N.append(42) #dummy end depot
# RS with dummy
V_R_Prime_0 = V_R_Prime.copy()
V_R_Prime_0.insert(0, depot)

m = Model("DVRP")

######### Parameters ###########

# Battery consumption required to move from 𝑖 to 𝑗
b = 2 * dist_matrix.copy()

# Time to move from 𝑖 to 𝑗
total = 0
for i in range(len(dist_matrix)):
    for j in range(len(dist_matrix)):
        # print(dist_matrix[i, j])
        total += dist_matrix[i, j]

average_dist = total / 600
t_list = dist_matrix * average_dist

for i in range(len(dist_matrix[1])):
    for j in range(len(dist_matrix[1])):
        t_list[i, j] = 2
t_list = 2 * dist_matrix.copy()
# Time elapsed during the photographing process of node 𝑖
scanning_cost = 10
s = [scanning_cost for i in V_F]
s.append(0)  # end depot
s = s + [0 for i in range(N, N + len(V_R_Prime))]
s.insert(0, 0)  # starting depot
s.append(0)  # end depot 2
# Battery consumption of the photographing process for node 𝑖
photo_cost = 10
p = [photo_cost for i in V_F]
p.append(0)  # end depot
p = p + [0 for i in range(N, N + len(V_R_Prime))]
p.insert(0, 0)  # starting depot
p.append(0)  # end depot 2
# Recharge Time
recharge_time = 0

# Battery Level
B = 300

# Priority coefficient for node 𝑖
k = priority_list.copy()

############### Decision Variables ################

# Binary variable indicating if node 𝑖 follows 𝑗 in the route
x = {}
for i in V_0_Prime: #V_0_Prime
    for j in V_Prime_N:
        if i != j:
            x[i, j] = m.addVar(vtype=GRB.BINARY, name='x' + str(i) + '_' + str(j))
            # x[j, i] = x[i, j]
m.update()

yy = m.addVar(vtype=GRB.BINARY, name='yy')
xx = m.addVar(vtype=GRB.BINARY, name='xx')
m.update()
# Completion time for node 𝑖
c = {}
for i in V_Prime_0_N:
    c[i] = m.addVar(lb=0.0, vtype=GRB.CONTINUOUS, name='c' + str(i))
m.update()

# Representing the battery level in node 𝑗
y = {}
for j in V_Prime_0_N:
    y[j] = m.addVar(lb=0.0, vtype=GRB.CONTINUOUS, name='y' + str(j))
m.update()

# Representing the arrival time to node 𝑖
a = {}
for i in V_Prime_0_N:
    a[i] = m.addVar(lb=0.0, vtype=GRB.CONTINUOUS, name='a' + str(i))
m.update()

# Summation of all 𝑡𝑖𝑗
M = 0
for i in range(len(t_list)):
    for j in range(len(t_list)):
        M = M + t_list[i, j]

############ Objective Function #############

obj = quicksum(k[i] * c[i] for i in V_Prime_0_N)


# obj = quicksum(x[(i, j)] * dist_matrix[i, j]
#                for j in V_Prime_N
#                for i in V_0_Prime if i != j)
m.setObjective(obj, GRB.MINIMIZE)

############# Constraints ##########3

# const 1
# for i in V_Prime_0_N:
for j in V_Prime_0_N:
    m.addConstr((a[j] + s[j] <= c[j]))
m.update()

# const 2
for i in V_F:
    m.addConstr(quicksum(x[(i, j)] for j in V_Prime_N if i != j) == 1)
m.update()

# const 3
for i in V_R_Prime:
    m.addConstr(quicksum(x[(i, j)] for j in V_Prime_N if i != j) <= 1)
m.update()

# const 4
for j in V_Prime:
    m.addConstr(quicksum(x[(j, i)] for i in V_Prime_N if i != j) -
                quicksum(x[(i, j)] for i in V_0_Prime if i != j) == 0)
m.update()

# const 5
for i in V_0:
    for j in V_Prime_N:
        if i != j:
            m.addConstr((a[i] + ((t_list[i, j] + s[i]) * x[(i, j)]) -
                         (M * (1 - x[(i, j)])) <= a[j]))
m.update()


# const 6
for i in V_R_Prime:
    for j in V_Prime_N:
        if i != j:
            m.addConstr((a[i] + ((t_list[i, j] * x[(i, j)]) + recharge_time * (B - y[i])) -
                     (M * (1 - x[(i, j)])) <= a[j]))
m.update()

# const 7
for i in V_F:
    for j in V_Prime_N:
        if i != j:
            m.addConstr((y[i] - ((b[i, j] + p[i]) * x[(i, j)]) +
                     (B * (1 - x[(i, j)])) >= y[j]))
m.update()

# const 8
for i in V_R_Prime_0:
    for j in V_Prime_N:
        if i != j:
            m.addConstr((y[j] + (b[i, j] * x[(i, j)])) <= B)
m.update()

# vehicle const
m.addConstr(quicksum(x[(0, j)] for j in V_Prime_N) <= 2)
m.update()

# vehicle const
# m.addConstr(quicksum(x[(j, 21)] for j in V_R_Prime if (j != 21 and j != 42)) +
#             quicksum(x[(j, 42)] for j in V_R_Prime if (j != 21 and j != 42)) >= 2*yy)
m.addConstr(quicksum(x[(j, 21)] for j in V_R_Prime if (j != 21 and j != 42)) <= yy)
m.addConstr(quicksum(x[(j, 42)] for j in V_R_Prime if (j != 21 and j != 42)) <= xx)
m.addConstr(quicksum(x[(j, 21)] for j in V_F) <= (1 - yy))
m.addConstr(quicksum(x[(j, 21)] for j in V_F) >= 0)
m.addConstr(quicksum(x[(j, 42)] for j in V_F) <= (1 - xx))
m.addConstr(quicksum(x[(j, 42)] for j in V_F) >= 0)

m.update()

# m.setParam("MIPGap", 0.80)
m.setParam("TimeLimit", 3600)
m.optimize()

if m.status == GRB.Status.OPTIMAL:
    print('Optimal objective: %g' % m.objVal)
elif m.status == GRB.Status.INF_OR_UNBD:
    print('Model is infeasible or unbounded')
    exit(0)
elif m.status == GRB.Status.INFEASIBLE:
    print('Model is infeasible')
    exit(0)
elif m.status == GRB.Status.UNBOUNDED:
    print('Model is unbounded')
    exit(0)
elif m.status == 9:
    print('Time Limit termination')
else:
    print('Optimization ended with status %d' % m.status)
    exit(0)

for v in m.getVars():
    if (v.varName[0] == 'x') & (v.x != 0):
        print('%s %g' % (v.varName, v.x))
m.objVal
m.Params.outputFlag = 0
print('')
for k in range(m.solCount):
    m.Params.solutionNumber = k
    objn = 0
    for v in m.getVars():
        objn += v.obj * v.xn
    print('Solution %d has objective %g' % (k, objn))
print('')
m.Params.outputFlag = 1
#
# m.write("DVRP.lp")

