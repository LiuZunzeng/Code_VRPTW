from gurobipy import Model,GRB,LinExpr
from Data.Data import Data
import time
import re
import matplotlib.pyplot as plt

class OptModel_grad:
    '''
    using gurobi to slove the problem
    '''
    def __init__(self):
        self.big_M = 10000
        self.model = Model("Lag")
        self.data = Data()
        self.X = [[[[] for k in range(self.data.vehicleNum)] for j in range(self.data.NodeNum)] for i in range(self.data.NodeNum)]
        self.S = [[[] for k in range(self.data.vehicleNum)] for i in range(self.data.NodeNum)]
        self.wait_time = [[[] for k in range(self.data.vehicleNum)] for i in range(self.data.NodeNum - 2)]
        self.slack = [[[] for k in range(self.data.vehicleNum)] for i in range(self.data.NodeNum)]
        self.u = [[]for i in range(self.data.NodeNum - 2)]#对偶变量（拉格朗日乘子）
        self.grads = [[] for i in range(self.data.NodeNum)]#拉格朗日函数的次梯度
        self.X_value = [[([0] * self.data.vehicleNum) for i in range(self.data.NodeNum)] for j in range(self.data.NodeNum)]
        self.UB = 363.25
        self.eps = 0.00035

    def start(self):
        '''
        process of the model
        :return:
        '''
        self.data.readData()
        #设置u_0,构建拉格朗日松弛模型
        for i in range(self.data.NodeNum-2):
            self.u[i] = 0.5
        self.var()
        self.cons()
        #次梯度迭代
        iter = 0
        iter_num = 70
        cite = 0.5
        self.lb_list = []
        self.t_list = []
        u_dict = {}
        grad_list = []
        obj_list = []
        while(iter<iter_num):
            print("-----------第",iter,"次迭代-------------")
            u_dict[iter] = self.u
            print("拉格朗日乘子：")
            print(self.u)
            self.obj()
            self.model.optimize()#得到最优解z(u_0),利用得到的最优解去更新拉格朗日乘子或者说得到u_1
            #self.model.setParam("outputFlag", 0)
            '''if (iter > 0 and (self.model.ObjVal - obj_list[iter - 1])**2 <= 0.00001):
                self.iter_final = iter
                self.visualization()
                return
            obj_list.append(self.model.ObjVal)'''
            #计算次梯度

            for i in self.model.getVars():
                str = re.split(r"_",i.VarName)
                if(str[0] == 'X') :
                    self.X_value[int(str[1])][int(str[2])][int(str[3])] = i.x
            for i in range(1,self.data.NodeNum - 1):
                expr = 1
                for j in range(self.data.NodeNum):
                    if (i != j):
                        for k in range(self.data.vehicleNum):
                            expr -= self.X_value[i][j][k]
                self.grads[i] = expr

            #计算步长
            sum = 0
            for i in range(1,self.data.NodeNum-1):
                sum += self.grads[i] ** 2
            if(sum < self.eps):
                break
            t = cite*(self.UB - self.model.ObjVal )/sum
            for i in range(1,self.data.NodeNum-1):
                self.u[i - 1] = self.u[i - 1] + t * self.grads[i]

            iter +=1
            self.lb_list.append(self.model.ObjVal)
            self.t_list.append(t)
            grad_list.append(self.grads)
        print("-----------次梯度迭代结束-------------")
        print("-----------最终的LB是:",self.model.ObjVal,"---------------")
        print("\n ---------------------iteration log information--------------------\n")
        print("Iter       LB        stepsize")
        for i in range(len(self.lb_list)):
            print(i,self.lb_list[i],self.t_list[i])
        print(max(self.lb_list))

        #可视化
        x = range(len(self.lb_list))
        y1 = self.lb_list
        y2 = []
        for i in range(len(self.lb_list)):
           y2.append(self.UB)
        # y2 = [2010.6902579779296, 2028.2105635640107, 2013.7377206008218, 2006.138800324195, 2006.2673427530817, 1991.5042316942925, 1984.7983361680003, 1980.3365704166067, 1971.5867116168054, 1964.3954137940352]
        plt.figure(figsize=(12, 8), dpi=80)
        plt.plot(x, y2, label = 'UB',color='red', linestyle='--', marker='.', markersize=5)
        plt.plot(x, y1,label = 'LB',color='blue', linestyle='-', marker='.', markersize=5)
        # plt.plot(x,y2,label='LB',color='black',linestyle='--',marker='.',markersize=5)
        plt.xlabel('iteration')
        plt.ylabel('LB')
        plt.title('How does the objective change when lamda changes')
        #xtick = ['{}'.format(i) for i in x]
        #plt.xticks(x, xtick)
        #plt.grid(alpha=0.8)
        plt.legend(loc='upper left')
        plt.show()
        return max(self.lb_list)


            #更新优化模型，

            #self.model.computeIIS()
            #self.model.write("a1.ilp")
            #self.model.write("a1.lp")
            #self.model.optimize()

    def visualization(self):
        print("-----------次梯度迭代结束-------------")
        print("-----------最终的LB是:", self.model.ObjVal, "---------------")
        print("\n ---------------------iteration log information--------------------\n")
        print("Iter       LB        stepsize")
        for i in range(self.iter_final):
            print(i, self.lb_list[i], self.t_list[i])

    def var(self):
        '''
        Initialize variables and constant
        :return:
        '''
        for i in range(self.data.NodeNum):
            for k in range(self.data.vehicleNum):
                name1 = "s_" + str(i) + "_" + str(k)
                self.S[i][k] = self.model.addVar(lb=self.data.readyTime[i], ub=self.data.dueTime[i], vtype=GRB.CONTINUOUS, name=name1)
                for j in range(self.data.NodeNum):
                    if (i != j):
                        name2 = "X_" + str(i) + "_" + str(j) + "_" + str(k)
                        self.X[i][j][k] = self.model.addVar(0, 1, vtype=GRB.INTEGER, name=name2)

    def obj(self):
        '''
        add the objective
        :return:
        '''
        obj = LinExpr(0)
        '''for k in range(self.data.vehicleNum):
            for i in range(1,self.data.NodeNum):
                obj.addTerms(self.big_M, self.slack[i][k])'''
        for i in range(self.data.NodeNum - 1):
            for j in range(self.data.NodeNum):
                if (i != j):
                    for k in range(self.data.vehicleNum):
                        if(i == 0):
                            obj.addTerms(self.data.disMatrix[i][j], self.X[i][j][k])
                        else:
                            obj.addTerms(self.data.disMatrix[i][j] - self.u[i - 1], self.X[i][j][k])

        for i in range(1,self.data.NodeNum-1):
            obj += self.u[i - 1]
        #obj += self.data.vehicleNum * self.data.vehicle_price

        self.model.setObjective(obj, GRB.MINIMIZE)

    def cons(self):
        '''
        add constraints
        :return:
        '''
        #把约束(1)松弛掉，放到目标函数里面
        ''''# Constraint(1) 每一个顾客点只能被一辆车经过
        for i in range(1, self.data.NodeNum - 1):
            expr = LinExpr(0)
            for j in range(1,self.data.NodeNum):
                if (i != j):
                    for k in range(self.data.vehicleNum):
                        expr.addTerms(1, self.X[i][j][k])

            self.model.addConstr(expr == 1, "c1" + "_" + str(i))
            expr.clear()'''

        # Constrain(2) 运载量约束
        for k in range(self.data.vehicleNum):
            expr = LinExpr(0)
            for i in range(1, self.data.NodeNum - 1):
                for j in range(self.data.NodeNum):
                    if (i != j):
                        expr.addTerms(self.data.demand[i], self.X[i][j][k])
            self.model.addConstr(expr <= self.data.capacity, "c2" + "_" + str(k))
            expr.clear()

        # Constraint(3) 起点平衡约束
        for k in range(self.data.vehicleNum):
            expr = LinExpr(0)
            for j in range(1, self.data.NodeNum - 1):
                expr.addTerms(1.0, self.X[0][j][k])
            self.model.addConstr(expr == 1.0, "c3" + "_" + str(k))
            expr.clear()

        # Constraint(4) 中间节点约束
        for k in range(self.data.vehicleNum):
            for h in range(1, self.data.NodeNum - 1):
                expr1 = LinExpr(0)
                expr2 = LinExpr(0)
                for i in range(self.data.NodeNum - 1):
                    if (h != i):
                        expr1.addTerms(1, self.X[i][h][k])

                for j in range(1,self.data.NodeNum):
                    if (h != j):
                        expr2.addTerms(1, self.X[h][j][k])

                self.model.addConstr(expr1 == expr2, "c4" + "_" + str(k) + "_" + str(h))
                expr1.clear()
                expr2.clear()

        # Constraint(5) 末点平衡约束
        for k in range(self.data.vehicleNum):
            expr = LinExpr(0)
            for i in range(1, self.data.NodeNum - 1):
                expr.addTerms(1, self.X[i][self.data.NodeNum - 1][k])
            self.model.addConstr(expr == 1, "c5" + "_" + str(k))
            expr.clear()

        # constraint(6) 时间窗约束
        for k in range(self.data.vehicleNum):
            for i in range(self.data.NodeNum):
                for j in range(self.data.NodeNum):
                    if (i != j):
                        self.model.addConstr(
                            self.S[i][k] + self.data.disMatrix[i][j] + self.data.serviceTime[i] - self.S[j][k]  <= \
                            self.big_M - self.big_M * self.X[i][j][k], "c6" + "_" + str(k) + "_" + str(i) + "_" + str(j))
        self.model.setParam("outputFlag", 0)

if __name__ == '__main__':    
    m = OptModel_grad()
    m.start()
    '''LB_list = []
    for i in range(10):
       LB = m.start()
       LB_list.append(LB)
       m.UB += 30
    print(LB_list)'''
#for m in model.getVars():
    #if(m.x == 1):
        #print("%s \t %d" % (m.varName,m.x))