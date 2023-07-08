import copy
from gurobipy import Model,GRB,LinExpr
import re
import math
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from Gurobi_direct.OptModel_m_pre import OptModel_gurobi

class Node:
    def __init__(self):
        self.local_LB = 0
        self.local_UB = np.inf
        self.x_sol ={}
        self.x_int_sol = {}
        self.branch_var_list = []
        self.model = None
        self.cnt = None
        self.is_integer = False
        self.var_LB = { }
        self.var_UB = {}

    def deepcopy_node(node):
        new_node = Node()
        new_node.local_LB = 0
        new_node.var_UB = np.inf
        new_node.x_sol = copy.deepcopy(node.x_int_sol)
        new_node.x_int_sol = copy.deepcopy(node.x_int_sol)
        new_node.branch_var_list = []
        new_node.model = node.model.copy()
        new_node.cnt = node.cnt
        new_node.is_integer = node.is_integer

        return new_node

class Node_2:

    def __init__(self):
        self.local_LB = 0
        self.local_UB = np.inf
        self.x_sol = {}
        self.x_int_sol = {}
        self.branch_var_list = []
        self.cnt = None
        self.is_integer = False
        self.var_LB = {}
        self.var_UB = {}

    def deepcopy_node(node):
        new_node = Node()
        new_node.local_LB = 0
        new_node.var_UB = np.inf
        new_node.x_sol = copy.deepcopy(node.x_int_sol)
        new_node.x_int_sol = copy.deepcopy(node.x_int_sol)
        new_node.branch_var_list = []
        new_node.cnt = node.cnt
        new_node.is_integer = node.is_integer
        new_node.var_LB = copy.deepcopy(node.var_LB)
        new_node.var_UB = copy.deepcopy(node.var_UB)

        return new_node

def Branch_and_bound(VRPTW_model, summary_interval):

    #Relax_VRPTW_model = VRPTW_model.relax()
    global_UB = np.inf
    global_LB = VRPTW_model.ObjVal
    eps = 1e-6
    incumbent_node = None
    Gap = np.inf
    feasible_sol_cnt = 0
    '''
       Branch and Bound starts
    '''
    Queue = []
    node = Node()
    node.local_LB = global_LB
    node.local_UB = np.inf
    node.model  = VRPTW_model.copy()
    node.model.setParam("OutputFlag",0)
    node.cnt = 0
    Queue.append(node)

    cnt = 0
    branch_cnt = 0
    Global_UB_change = []
    Global_LB_change = []
    while (len(Queue) > 0 and global_UB - global_LB > eps):
        #pop()取列表的最后一个元素,且将其从列表中删掉
        current_node = Queue.pop()
        cnt += 1

        current_node.model.optimize()
        #status==2,代表最优；status=3,代表无可行解；status==5,无界解
        Solution_status = current_node.model.Status
        is_integer = True
        is_pruned = False
        if(Solution_status == 2):
            for var in current_node.model.getVars():
                if(var.VarName.startswith('X')):
                    #current_node.x_sol[var.varName] = copy.deepcopy(current_node.model.getVarByName())
                    current_node.x_sol[var.varName] = var.x
                    #print(var.VarName,'=',var.x)
                    #将非整数决策变量全部加入节点的分支变量列表
                    if(abs(round(var.x,0) - var.x) >= eps):
                        is_integer = False
                        current_node.branch_var_list.append(var.VarName)
            if (is_integer == True):
                feasible_sol_cnt += 1
                current_node.is_integer = True
                current_node.local_LB = current_node.model.ObjVal
                current_node.local_UB = current_node.model.ObjVal
                if (current_node.local_UB < global_UB):
                    global_UB = current_node.local_UB
                    #深拷贝，开拓新内存，“=”是共用同一块内存
                    incumbent_node = Node.deepcopy_node(current_node)
            if (is_integer == False):
                current_node.is_integer = False
                current_node.local_UB = global_UB
                current_node.local_LB = current_node.model.ObjVal

            if(is_integer  == True):
                is_pruned = True

            if(is_integer == False and current_node.local_LB > global_UB):
                is_pruned = True

            Gap = round(100*(global_UB  - global_LB)/global_LB,2)

        elif (Solution_status != 2):
            is_integer = False
            is_pruned = True

            continue

        if(is_pruned == False):
            branch_cnt += 1
            branch_var_name = None

            #从所有非整数变量中找到一个离0.5最近的变量
            min_diff = 100
            for var_name in current_node.branch_var_list:
                if(abs(current_node.x_sol[var_name] - 0.5) < min_diff):
                    branch_var_name = var_name
                    min_diff = abs(current_node.x_sol[var_name] - 0.5)
            #每迭代50次，输出用来分支的变量
            if(branch_cnt % summary_interval == 0):
                print('Branch var name',branch_var_name,'\t,Branch var value :',current_node.x_sol[branch_var_name])
            #左边是0，右边是1
            left_var_bound = (int)(current_node.x_sol[branch_var_name])
            right_var_bound = (int)(current_node.x_sol[branch_var_name]) + 1

            left_node = Node.deepcopy_node(current_node)
            right_node = Node.deepcopy_node(current_node)

            temp_var = left_node.model.getVarByName(branch_var_name)
            left_node.model.addConstr(temp_var <= left_var_bound,name = 'branch_left' + str(cnt))
            left_node.model.setParam("OutputFlag",0)
            left_node.model.update()
            cnt +=1
            left_node.cnt = cnt

            temp_var = right_node.model.getVarByName(branch_var_name)
            right_node.model.addConstr(temp_var >= right_var_bound, name='branch_right' + str(cnt))
            right_node.model.setParam("OutputFlag", 0)
            right_node.model.update()
            cnt += 1
            right_node.cnt = cnt

            Queue.append(left_node)
            Queue.append(right_node)

            temp_global_LB = np.inf
            #遍历叶子节点队列,更新下界
            for node in Queue:
                node.model.optimize()
                if(node.model.status == 2):
                    if(node.model.ObjVal <= temp_global_LB and node.model.ObjVal <= global_UB):
                        temp_global_LB = node.model.ObjVal

            global_LB = temp_global_LB
            Global_UB_change.append(global_UB)
            Global_LB_change.append(global_LB)

        if((cnt - 2)% summary_interval == 0):
            print('\n\n==================')
            print('Queue length:',len(Queue))
            print('\n -------------- \n',cnt,'UB =',global_UB,'LB =',global_LB,'\t Gap = ',Gap,' %','feasible_sol_cnt:',feasible_sol_cnt)

    #all the nodes are explored,update the LB and UB
    incumbent_node.model.optimize()
    global_UB  = incumbent_node.model.ObjVal
    global_LB = global_UB
    Gap = round(100 * (global_UB - global_LB)/global_LB,2)
    Global_UB_change.append(global_UB)
    Global_LB_change.append(global_LB)

    print('\n\n\n\n')
    print('-----------------------------------------')
    print('      Branch and Bound terminates        ')
    print('        Optimal solution found           ')
    print('-----------------------------------------')
    print('\nIter cnt = ',cnt, '\n\n')
    print('\nFinal Gap = ',Gap, '%\n\n')
    print(' -------Optimal Solution ---------')
    '''for key in incumbent_node.x_sol.keys():
        if(incumbent_node.x_sol[key] > 0):
            print(key, '=', incumbent_node.x_sol[key])'''
    print('\nOptimal Obj:',global_LB)

    return incumbent_node,Gap,Global_UB_change,Global_LB_change

m = OptModel_gurobi()
m.start()
incumbent_node,Gap,Global_UB_change,Global_LB_change  = Branch_and_bound(m.model,summary_interval= 50)
for key in incumbent_node.x_sol.keys():
    if(incumbent_node.x_sol[key] > 0):
        print(key, '=', incumbent_node.x_sol[key])

import  matplotlib.pyplot as plt
print(len(Global_LB_change))
x = range(len(Global_UB_change))
plt.figure(figsize=(12,8),dpi=80)
plt.plot(x,Global_UB_change,label='UB',color='red',linestyle=':',marker='.',markersize=5)
plt.plot(x,Global_LB_change,label='LB',color='black',linestyle='--',marker='.',markersize=5)
plt.xlabel('Iterations')
plt.ylabel('Bound Value')
plt.title('Change of the Bound')
#xtick = ['{}'.format(i) for i in x ]
#plt.xticks(x,xtick)
#plt.grid(alpha=0.8)
plt.legend(loc = 'upper left')
plt.show()