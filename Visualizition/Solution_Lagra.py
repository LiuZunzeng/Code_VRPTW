from Data.Data import Data
from Lagrange_relaxation.OptModel_grad import OptModel_grad
import re

class Solution:
    '''
    1.OptModel输出的最优解  →  routes
    2.可视化
    '''

    def __init__(self):
        self.model = OptModel_grad()
        self.data = Data()
        self.X = [[([0] * self.data.vehicleNum) for i in range(self.data.NodeNum)] for j in range(self.data.NodeNum)]
        self.S = [[([0] * self.data.vehicleNum) for i in range(self.data.NodeNum)] for j in range(self.data.NodeNum)]
        self.y = [[] for k in range(self.data.vehicleNum)]
        self.m = 0
        self.routes = []
        self.routeNum = 0

    def start(self):
        self.data.readData()
        self.model.start()
        self.getSolution()

    def getSolution(self):
        '''
        1.OptModel输出的最优解  →  routes
        2.可视化
        :return:
        '''
        #1.OptModel输出的最优解  →  routes
        for i in self.model.model.getVars():
            str = re.split(r"_",i.VarName)
            if(str[0] == 'X' and i.x == 1) :
                self.X[int(str[1])][int(str[2])][int(str[3])] = i.x
            if(str[0] == "s" and i.x == 1):
                self.S[int(str[1])][int(str[2])] = i.x

            if(str[0] == "y"):
                self.y[int(str[1])] = i.x

        price = 0
        for k in range(self.data.vehicleNum):
            for i in range(self.data.NodeNum):
                for j in range(self.data.NodeNum):
                    if(self.X[i][j][k] > 0 and (not(i == 0 and j == self.data.NodeNum))):
                        price += self.data.disMatrix[i][j]
                        print("x[{0},{1},{2}] = {3}" .format(i,j,k,self.X[i][j][k]))
        price += self.data.vehicle_price * self.data.vehicleNum
        print("目标函数值：",price)
        #可视化

        '''for k in range(self.data.vehicleNum):
            if(self.y[k] > 0):
                i = 0
                subRoute = []
                subRoute.append(i)
                finish = False
                while(not finish):
                    for j in range(self.data.NodeNum):
                           if (self.X[i][j][k] > 0):
                              subRoute.append(j)
                              i = j
                              if(j == self.data.NodeNum -1):
                                  finish = True
                #if(len(subRoute) >= 3):
                subRoute[len(subRoute)-1] = 0
                self.routes.append(subRoute)
                self.routeNum +=1
        #print("\n\n==============Route of Vehicles===============")
        print(self.routes)
        print("\n\n==============Drawing the Graph==============")
        plt.figure(0)
        plt.xlabel('x')
        plt.ylabel('y')
        plt.title("All Customers")
        plt.scatter(self.data.cor_X[0],self.data.cor_Y[0],c='blue',alpha=1,marker=',',linewidths=3,label='depot')
        plt.scatter(self.data.cor_X[1:-1], self.data.cor_Y[1:-1], c='black', alpha=1, marker='o', linewidths=3,
                    label='customer')
        for k in range(self.routeNum):
            for i in range(len(self.routes[k]) - 1):
                a = self.routes[k][i]
                b = self.routes[k][i+1]
                x = [self.data.cor_X[a],self.data.cor_X[b]]
                y = [self.data.cor_Y[a], self.data.cor_Y[b]]
                plt.plot(x,y,'k',linewidth = 1)
        plt.grid(False)
        plt.legend(loc='best')
        plt.show()'''

if __name__ == '__main__':
    s = Solution()
    s.start()