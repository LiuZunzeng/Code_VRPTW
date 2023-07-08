
from gurobipy import Model,GRB,LinExpr,Column
from Data.Data import Data
import time


class column_generating:

    def __init__(self):

        self.RMP = Model('RMP')
        self.SP = Model('SP')
        self.data = Data()
        self.customerNum = self.data.customerNum
        self.path_set = {}
        self.y = {}
        #SP决策变量
        self.x = {}
        #SP决策变量到达某个点的时刻
        self.s = {}
        self.big_M = 1e5
        #对偶变量
        self.rmp_pi =[]
        #迭代次数
        self.cnt = 0
        #MP的系数矩阵
        self.rmp_con = []

    def start(self):
        '''
        列生成的主体脉络
        :return:
        '''
        #先读数据
        self.data.readData()
        #先建立并求解初始的MP
        self.build_MP()
        t1 = time.time()
        self.RMP.optimize()

        #获取MP的每一个约束所对应的对偶变量
        self.rmp_pi = self.RMP.getAttr("Pi", self.RMP.getConstrs())
        #为了遍历的时候方便
        self.rmp_pi.insert(0, 0)
        self.rmp_pi.append(0)

        #构建子问题并求解
        self.build_SP()
        self.SP.optimize()

        # 处理好初始MP的SP之后开始迭代
        eps = - 0.01
        cnt = 0
        while (self.SP.ObjVal + self.data.vehicle_price < eps):
            self.add_column()
            self.RMP.optimize()
            # 获取MP的每一个约束所对应的对偶变量
            self.rmp_pi = self.RMP.getAttr("Pi", self.RMP.getConstrs())
            # 为了遍历的时候方便
            self.rmp_pi.insert(0, 0)
            self.rmp_pi.append(0)
            self.build_SP()
            self.SP.optimize()
        t2 = time.time()
        print("time used:",t2 - t1)
        print('刘遵增很好')
        self.RMP.write('RMP_final.lp')
        '''mip_var = self.RMP.getVars()
        for i in range(self.RMP.numVars):
            mip_var[i].setAttr("VType", GRB.INTEGER)'''

        self.RMP.optimize()
        print('最终的最优解：',self.RMP.ObjVal)
        for var in self.RMP.getVars():
            if (var.x > 0):
                print(var.VarName, '=', var.x, '\t path:', self.path_set[var.VarName])


    def build_MP(self):
        '''
        建立并求解MP，这里初始列的生成比较简单，即0→i→0
        :return:
        '''
        for i in range(self.customerNum):
            var_name = 'y_' + str(i)

            #设置决策变量
            self.y[i] = self.RMP.addVar(lb=0, obj=round(self.data.disMatrix[0][i+1] + self.data.disMatrix[i+1][0], 1)+self.data.vehicle_price, vtype=GRB.CONTINUOUS,
                              name=var_name)
            self.path_set[var_name] = [0, i + 1, self.data.NodeNum - 1]

            row_coeff = [i] * self.customerNum

        #生成初始列
        for i in range(self.customerNum):
            self.rmp_con.append(self.RMP.addConstr(self.y[i] == 1))

        self.RMP.write('RMP.lp')


    def build_SP(self):
        '''
        建立并求解SP
        :return:
        '''
        for i in range(self.data.NodeNum):
            name = 's_'  + str(i)
            self.s[i] = self.SP.addVar(lb=self.data.readyTime[i], ub=self.data.dueTime[i], vtype=GRB.CONTINUOUS, name=name)
            for j in range(self.data.NodeNum):
                if (i != j):
                    name = 'x_' + str(i) + '_' + str(j)
                    self.x[i, j] = self.SP.addVar(lb=0, ub=1, vtype=GRB.INTEGER, name=name)

        sub_obj = LinExpr(0)
        for key in self.x.keys():
            node_i = key[0]
            node_j = key[1]
            sub_obj.addTerms(self.data.disMatrix[node_i][node_j], self.x[key])
            sub_obj.addTerms(-self.rmp_pi[node_i], self.x[key])

        self.SP.setObjective(sub_obj, GRB.MINIMIZE)

        # Constraint 1
        expr = LinExpr(0)
        for key in self.x.keys():
            node_i = key[0]
            expr.addTerms(self.data.demand[node_i], self.x[key])
        self.SP.addConstr(expr <= self.data.capacity, name='cons_1')

        # Constraint 2
        expr = LinExpr(0)
        for key in self.x.keys():
            if (key[0] == 0):
                expr.addTerms(1, self.x[key])
        self.SP.addConstr(expr == 1, name='cons_2')

        # Constraint 3
        for h in range(1, self.data.NodeNum - 1):
            expr = LinExpr(0)
            for i in range(self.data.NodeNum):
                temp_key = (i, h)
                if (temp_key in self.x.keys()):
                    expr.addTerms(1, self.x[temp_key])

            for j in range(self.data.NodeNum):
                temp_key = (h, j)
                if (temp_key in self.x.keys()):
                    expr.addTerms(-1, self.x[temp_key])
            self.SP.addConstr(expr == 0, name='cons_3')

        # Constraint 4
        expr = LinExpr(0)
        for key in self.x.keys():
            if (key[1] == self.data.NodeNum - 1):
                expr.addTerms(1, self.x[key])
        self.SP.addConstr(expr == 1, name='cons_4')

        # Constraint 5
        for key in self.x.keys():
            node_i = key[0]
            node_j = key[1]
            self.SP.addConstr(self.s[node_i] + self.data.disMatrix[node_i][node_j] + self.data.serviceTime[node_i] - self.s[node_j] - self.big_M + self.big_M * self.x[key] <= 0,
                         name='cons_5')

        self.RMP.setParam("outputFlag", 0)
        self.SP.setParam("outputFlag", 0)
        self.SP.optimize()


    def add_column(self):
        '''
        将SP的最优解  →   path   →   column
        :return:
        '''
        '''print("=====RMP.opt=====SP.opt=======")
        print('the not shortest cost:',self.RMP.ObjVal)
        print("let me see see the RMP vars:")
        list = self.RMP.getVars()
        value = []
        for i in list:
           value.append(i.x)
        print(value)
        print("对偶变量：",self.rmp_pi)
        print("let me see see the SP vars:")
        lst = self.SP.getVars()
        value = {}
        for i in lst:
            value[i.VarName] = i.x
        print(value)
        print('reduced cost :', self.SP.ObjVal)'''

        self.cnt += 1
        print(' --------------- cnt =', self.cnt, '--------------- ')

        # 计算这条路径的长度，也就是MP问题目标函数中的价值系数
        path_length = 0
        for key in self.x.keys():
            node_i = key[0]
            node_j = key[1]
            path_length += self.x[key].x * self.data.disMatrix[node_i][node_j]
        path_length = round(path_length, 2)

        # create new column
        col_coef = [0] * self.data.customerNum
        for key in self.x.keys():
            if (self.x[key].x > 0):
                node_i = key[0]
                if (node_i > 0 and node_i < self.data.NodeNum - 1):
                    col_coef[node_i - 1] = 1

        print('new path length:', path_length)
        print('new column:', col_coef)

        #将新列加到系数矩阵当中??????
        rmp_col = Column(col_coef, self.rmp_con)

        # write the new path
        new_path = []
        current_node = 0
        new_path.append(current_node)
        while (current_node != self.data.NodeNum - 1):
            for key in self.x.keys():
                if (self.x[key].x > 0 and key[0] == current_node):
                    current_node = key[1]
                    new_path.append(current_node)

        # 在MP中加入一个代表新列的决策变量和对应的c
        var_name = 'cg_' + str(self.cnt)
        self.RMP.addVar(lb=0.0, obj=path_length + self.data.vehicle_price, vtype=GRB.CONTINUOUS, name=var_name, column=rmp_col)
        self.RMP.update()
        self.path_set[var_name] = new_path
        print("the column number of the RMP", self.RMP.NumVars)


if __name__ == '__main__':
    m = column_generating()
    m.start()