from gurobipy import Model,GRB,LinExpr
from Data.Data import Data
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
        self.wait_time = [[[] for k in range(self.data.vehicleNum)] for i in range(self.data.NodeNum - 2)]
        self.slack = [[[] for k in range(self.data.vehicleNum)] for i in range(self.data.NodeNum)]
        self.y = [[] for k in range(self.data.vehicleNum)]
        self.is_relax = 1

    def start(self):
        '''
        process of the model
        :return:
        '''
        self.data.readData()
        self.var()
        self.obj()
        self.cons()
        #self.model.setParam("outputFlag", 0)
        self.model.optimize()
        print("整数规划模型",self.model.ObjVal)
        if(self.is_relax):
            self.relax()
            self.model.optimize()
            print("松弛模型",self.model.ObjVal)
        #self.model.computeIIS()
        #self.model.write("a1.ilp")
        self.model.write("a1.lp")
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
                    if (i != j and self.data.arcs[i,j] > 0):
                        name2 = "X_" + str(i) + "_" + str(j) + "_" + str(k)
                        self.X[i][j][k] = self.model.addVar(0, 1, vtype=GRB.INTEGER, name=name2)

        #车辆数变量
        self.m = self.model.addVar(lb=0,vtype=GRB.INTEGER,name="m")

        # 新加一个变量，用来约束车的数量
        for k in range(self.data.vehicleNum):
            name = "y_" + str(k)
            self.y[k] = self.model.addVar(0, 1, vtype=GRB.INTEGER, name=name)

    def relax(self):
        '''
        将model中的整型变量转化为连续变量
        :return:
        '''
        mip_var = self.model.getVars()
        for i in range(self.model.numVars):
            mip_var[i].setAttr("VType", GRB.CONTINUOUS)
        self.model.update()

    def obj(self):
        '''
        add the objective
        :return:
        '''
        obj = LinExpr(0)
        '''for k in range(self.data.vehicleNum):
            for i in range(1,self.data.NodeNum):
                obj.addTerms(self.big_M, self.slack[i][k])'''
        for i in range(self.data.NodeNum):
            for j in range(self.data.NodeNum):
                if (i != j and self.data.arcs[i,j] > 0):
                    for k in range(self.data.vehicleNum):
                        obj.addTerms(self.data.disMatrix[i][j], self.X[i][j][k])
        obj.addTerms(self.data.vehicle_price,self.m)
        self.model.setObjective(obj, GRB.MINIMIZE)

    def cons(self):
        '''
        add constraints
        :return:
        '''
        # Constraint(1) 每一个顾客点只能被一辆车经过
        for i in range(1, self.data.NodeNum - 1):
            expr = LinExpr(0)
            for j in range(1,self.data.NodeNum):
                if (i != j and self.data.arcs[i,j] > 0):
                    for k in range(self.data.vehicleNum):
                        expr.addTerms(1, self.X[i][j][k])

            self.model.addConstr(expr == 1, "c1" + "_" + str(i))
            expr.clear()

        # Constrain(2) 运载量约束
        for k in range(self.data.vehicleNum):
            expr = LinExpr(0)
            for i in range(1, self.data.NodeNum - 1):
                for j in range(self.data.NodeNum):
                    if (i != j and self.data.arcs[i,j] > 0):
                        expr.addTerms(self.data.demand[i], self.X[i][j][k])
            self.model.addConstr(expr <= self.data.capacity, "c2" + "_" + str(k))
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
                    if (h != i and self.data.arcs[i,h] > 0):
                        expr1.addTerms(1, self.X[i][h][k])

                for j in range(1,self.data.NodeNum):
                    if (h != j and self.data.arcs[h,j] > 0):
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
                    if (i != j and self.data.arcs[i,j] > 0):
                        self.model.addConstr(
                            self.S[i][k] + self.data.disMatrix[i][j] + self.data.serviceTime[i] - self.S[j][k]  <= \
                            self.big_M - self.big_M * self.X[i][j][k], "c6" + "_" + str(k) + "_" + str(i) + "_" + str(j))

        # constraint(7)两个布尔逻辑变量之间的约束
        for k in range(self.data.vehicleNum):
            for i in range(self.data.NodeNum):
                for j in range(self.data.NodeNum):
                    if (i != j and self.data.arcs[i,j] > 0):
                        self.model.addConstr(self.X[i][j][k] <= self.y[k],"c7_"+str(k) + "_" + str(i) + "_" + str(j))

        #constraint(8)车辆数约束
        expr = LinExpr(0)
        for k in range(self.data.vehicleNum):
            expr.addTerms(1,self.y[k])
        self.model.addConstr(expr == self.m,"c8")
        expr.clear()

        self.model.setParam("outputFlag", 0)


if __name__ == '__main__':
    m = OptModel_gurobi()
    m.start()
#for m in model.getVars():
    #if(m.x == 1):
        #print("%s \t %d" % (m.varName,m.x))
