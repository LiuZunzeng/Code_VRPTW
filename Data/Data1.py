import pandas as pd
import math
import random

class Data:

    def __init__(self):
        self.customerNum = 50
        self.NodeNum = self.customerNum + 2
        self.vehicleNum = 7
        self.cor_X = []
        self.cor_Y = []
        self.degree = []
        self.serviceTime = []
        self.readyTime = []
        self.dueTime = []
        self.demand = []
        self.disMatrix = [[]]
        self.arcs = {}
        self.volume = 200
        self.capacity = []
        self.hours = 80
        self.vehicle_price = 50
        #护理人员的等级
        random.seed(2023)
        for k in range(self.vehicleNum):
            self.capacity.append(random.randint(3,4))

    def readData(self):
        df = pd.read_excel("D:\optimazation algorithm\整数线性规划建模\VRPTW\Data\R101.xlsx")
        count = 0
        for index, row in df.iterrows():
            self.cor_X.append(float(row["XCOORD."]))
            self.cor_Y.append(float(row["YCOORD."]))
            self.degree.append(float(row["DEGREE"]))
            self.serviceTime.append(float(row["SERVICE TIME"]))
            self.readyTime.append(float(row["READY TIME"]))
            self.dueTime.append(float(row["DUE DATE"]))
            self.demand.append(float(row["DEMAND"]))
            self.disMatrix = [([0] * self.NodeNum) for p in range(self.NodeNum)]
            count += 1
            if (count == self.customerNum + 1):
                break
        self.cor_X.append(self.cor_X[0])
        self.cor_Y.append(self.cor_Y[0])
        self.degree.append(self.degree[0])
        self.serviceTime.append(self.serviceTime[0])
        self.readyTime.append(self.readyTime[0])
        self.dueTime.append(self.dueTime[0])
        self.demand.append(self.demand[0])

        for i in range(self.NodeNum):
            for j in range(self.NodeNum):
                temp = (self.cor_X[i] - self.cor_X[j]) ** 2 + (self.cor_Y[i] - self.cor_Y[j]) ** 2
                self.disMatrix[i][j] = math.sqrt(temp)

        # =================data pre-processing==================
        for i in range(self.NodeNum):
            for j in range(self.NodeNum):
                if (i == j):
                    self.arcs[i, j] = 0
                else:
                    self.arcs[i, j] = 1
        '''for i in range(self.NodeNum):
            for j in range(self.NodeNum):
                if(i == j):
                   self.arcs[i,j] = 0
                elif(self.readyTime[i] +self.serviceTime[i] + self.disMatrix[i][j] > self.dueTime[j] or self.demand[i] + self.demand[j] > self.capacity):
                    self.arcs[i,j] = 0
                else:
                    self.arcs[i,j] = 1'''
        for i in range(self.NodeNum):
            self.arcs[self.NodeNum - 1,i] = 0
            self.arcs[i,0]  = 0
