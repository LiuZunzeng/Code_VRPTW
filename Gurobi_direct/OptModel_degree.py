from gurobipy import Model,GRB,LinExpr,QuadExpr
from Data.Data1 import Data
import time

class OptModel_gurobi:
    '''
    using gurobi to slove the problem
    '''
    def __init__(self):
        self.big_M = 10000
        self.model = Model("VRPTW")
        self.data = Data()
        self.X = [[[[] for k in range(self.data.vehicleNum)] for j in range(self.data.NodeNum)] for i in range(self.data.NodeNum)]
        self.S = [[[] for k in range(self.data.vehicleNum)] for i in range(self.data.NodeNum)]
        self.y = [[] for k in range(self.data.vehicleNum)]
        self.wait_time = [[[] for k in range(self.data.vehicleNum)] for i in range(self.data.NodeNum - 2)]
        self.abs = [[] for i in range(self.data.customerNum)]
        self.slack = [[[] for k in range(self.data.vehicleNum)] for i in range(self.data.NodeNum)]


    def start(self):
        '''
        process of the model
        :return:
        '''
        self.data.readData()
        self.var()
        self.obj()
        self.cons()
        self.model.optimize()
        #self.model.computeIIS()
        #self.model.write("a1.ilp")
        #self.model.write("a2.lp")
        #self.model.optimize()

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
                        self.X[i][j][k] = self.model.addVar(0, 1, vtype=GRB.BINARY, name=name2)
        for k in range(self.data.vehicleNum):
            for i in range(self.data.NodeNum):
                name_1 = "v_" + str(i) + "_" + str(k)
                self.slack[i][k] = self.model.addVar(lb=0,vtype=GRB.CONTINUOUS,name=name_1)

        self.m = self.model.addVar(lb = 0,vtype = GRB.INTEGER,name = "vehicleNum")

        #新加一个变量，用来约束车的数量
        for k in range(self.data.vehicleNum):
            name = "y_"+str(k)
            self.y[k] = self.model.addVar(0,1,vtype = GRB.INTEGER,name = name)

    def obj(self):
        '''
        add the objective
        :return:
        '''
        obj1 = LinExpr(0)
        for k in range(self.data.vehicleNum):
            for i in range(self.data.NodeNum):
                for j in range(self.data.NodeNum):
                    if (i != j):
                       obj1.addTerms(self.data.disMatrix[i][j], self.X[i][j][k])
        for k in range(self.data.vehicleNum):
                    for i in range(1,self.data.NodeNum):
                        obj1.addTerms(self.big_M, self.slack[i][k])
        obj1.addTerms(self.data.vehicle_price,self.m)

        self.model.setObjective(obj1, GRB.MINIMIZE)

    def cons(self):
        '''
        add constraints
        :return:
        '''
        # Constraint(1) 每一个顾客点只能被一辆车经过
        for i in range(1, self.data.NodeNum - 1):
            expr = LinExpr(0)
            for j in range(1,self.data.NodeNum):
                if (i != j):
                    for k in range(self.data.vehicleNum):
                        expr.addTerms(1, self.X[i][j][k])

            self.model.addConstr(expr == 1, "c1" + "_" + str(i))
            expr.clear()

        # Constrain(2) 运载量约束
        for k in range(self.data.vehicleNum):
            expr = LinExpr(0)
            for i in range(1, self.data.NodeNum - 1):
                for j in range(self.data.NodeNum):
                    if (i != j):
                        expr.addTerms(self.data.demand[i], self.X[i][j][k])
            self.model.addConstr(expr <= self.data.volume, "c2" + "_" + str(k))
            expr.clear()

        # Constraint(3) 起点平衡约束
        for k in range(self.data.vehicleNum):
            expr = LinExpr(0)
            for j in range(1, self.data.NodeNum - 1):
                expr.addTerms(1.0, self.X[0][j][k])
            self.model.addConstr(expr == self.y[k], "c3" + "_" + str(k))
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
            self.model.addConstr(expr == self.y[k], "c5" + "_" + str(k))
            expr.clear()

        # constraint(6) 时间窗约束
        for k in range(self.data.vehicleNum):
            for i in range(self.data.NodeNum):
                for j in range(self.data.NodeNum):
                    if (i != j):
                        self.model.addConstr(
                            self.S[i][k] + self.data.disMatrix[i][j] - (self.S[j][k]+ self.slack[j][k]) <= \
                            self.big_M - self.big_M * self.X[i][j][k], "c6" + "_" + str(k) + "_" + str(i) + "_" + str(j))

        # constraint(7)两个布尔逻辑变量之间的约束
        for k in range(self.data.vehicleNum):
            for i in range(self.data.NodeNum):
                for j in range(self.data.NodeNum):
                    if (i != j):
                        self.model.addConstr(self.X[i][j][k] <= self.y[k],"c7_"+str(k) + "_" + str(i) + "_" + str(j))

        #constraint(8)车辆数约束
        expr = LinExpr(0)
        for k in range(self.data.vehicleNum):
            expr.addTerms(1,self.y[k])
        self.model.addConstr(expr == self.m,"c8")
        expr.clear()

        #constraint(9)等级匹配约束
        expr = LinExpr(0)
        for k in range(self.data.vehicleNum):
            for i in range(1,self.data.NodeNum - 1):
                for j in range(self.data.NodeNum):
                    if (i != j):
                       expr.addTerms(1,self.X[i][j][k])
                self.model.addConstr(self.data.degree[i] <= self.data.capacity[k] + self.big_M * (1 - expr),
                                     "c9_"+str(i)+str(k))
                expr.clear()

if __name__ == '__main__':
    m = OptModel_gurobi()
    m.start()
#for m in model.getVars():
    #if(m.x == 1):
        #print("%s \t %d" % (m.varName,m.x))