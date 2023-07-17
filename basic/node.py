import numpy as np


class Node:
    CHECK = CALL = 0 #check,call在数组中以index=0表示
    RAISE = 1 #raise在数组中以index=1表示
    FOLD = 2 #fold在数组中以index=2表示

    NUM_ACTION = 3

    actions = [] #存储动作序列

    chips_pool = 0 #该节点中的底池

    def __init__(self,infoSet):
        self.infoSet = infoSet
        self.regretSum = np.zeros((self.NUM_ACTION,), dtype=np.float)
        self.strategy = np.ones((self.NUM_ACTION,), dtype=np.float)
        self.strategySum = np.zeros((self.NUM_ACTION,), dtype=np.float)

    def getStrategy(self,weight):
        normalize_sum = 0.

        for a in range(self.NUM_ACTION):
            self.strategy[a] = self.regretSum[a] if self.regretSum[a] > 0 else 0
            normalize_sum += self.strategy[a]

        for a in range(self.NUM_ACTION):
            if normalize_sum > 0:
                self.strategy[a] /= normalize_sum
            else:
                self.strategy[a] = 1. / self.NUM_ACTION

            self.strategySum[a] += weight * self.strategy[a]

        return self.strategy

    def get_before_action_strategy(self,weight):

        for a in range(self.NUM_ACTION):
            self.strategy[a] = self.strategy[a] * weight

        return self.strategy

    def getStrategySum(self):
        normalize_sum = 0.

        for a in range(self.NUM_ACTION):
            normalize_sum += self.strategySum[a]

        for a in range(self.NUM_ACTION):
            if normalize_sum > 0:
                self.strategySum[a] /= normalize_sum
            else:
                self.strategySum[a] = 1. /self.NUM_ACTION

        # print("strategy: " + str(self.strategy))

        return self.strategySum
    
    # def getNormalizeRegetSum(self):
    #     normalize_sum = 0.
    #
    #     normalize_regret_sum =  np.zeros((self.NUM_ACTION,), dtype=np.float)
    #
    #
    #     for a in range(self.NUM_ACTION):
    #         normalize_regret_sum[a] = self.regretSum[a] if self.regretSum[a] > 0 else 0
    #         normalize_sum += normalize_regret_sum[a]
    #     for a in range(self.NUM_ACTION):
    #         if normalize_sum > 0:
    #             normalize_regret_sum[a] /= normalize_sum
    #         else:
    #             normalize_regret_sum[a] =  1. /self.NUM_ACTION
    #
    #
    #     print("normalize_regret_sum: " + str(normalize_regret_sum))
    #     return normalize_regret_sum


    def setStrategySum(self,i,strategySum):
        self.strategySum[i] += strategySum

    def setStrategy(self,i,strategy):
        self.strategy[i] += strategy

    def setRegretSum(self,i,regret):
        self.regretSum[i] += regret

    def getRegretSum(self):
        return self.regretSum






