import matplotlib.pyplot as plt
import numpy as np
import matplotlib
import random
from search import Search
import itertools

# 设置matplotlib正常显示中文和负号
matplotlib.rcParams['font.sans-serif']=['SimHei']   # 用黑体显示中文
matplotlib.rcParams['axes.unicode_minus']=False     # 正常显示负号
# 随机生成（10000,）服从正态分布的数据
allCards = ['<0,0>','<0,1>','<0,2>','<0,3>','<0,4>','<0,5>','<0,6>','<0,7>','<0,8>','<0,9>','<0,10>','<0,11>','<0,12>',
            '<1,0>','<1,1>','<1,2>','<1,3>','<1,4>','<1,5>','<1,6>','<1,7>','<1,8>','<1,9>','<1,10>','<1,11>','<1,12>',
            '<2,0>','<2,1>','<2,2>','<2,3>','<2,4>','<2,5>','<2,6>','<2,7>','<2,8>','<2,9>','<2,10>','<2,11>','<2,12>',
            '<3,0>','<3,1>','<3,2>','<3,3>','<3,4>','<3,5>','<3,6>','<3,7>','<3,8>','<3,9>','<3,10>','<3,11>','<3,12>',]
data = []
cards = []
dict = {}
t = None
# for j in range(0,5):
#     handCards = []
#     for i in range(0,2):
#         one = random.randint(0,3)
#         two = random.randint(0,12)
#
#         three = 0
#
#         four = 0
#
#         while True:
#
#             three = random.randint(0,3)
#
#             four = random.randint(0, 12)
#
#             if three != one and four != two:
#                 break
#
#
#
#         strs = "<" + str(one) + "," + str(two) + ">"
#         handCards.append(strs)
#         strs = "<" + str(three) + "," + str(four) + ">"
#         handCards.append(strs)

for i in itertools.combinations(allCards,2):

    rank = Search.preflop(i)
    if rank in dict.keys():
        dict[rank] += 1
    else:
        dict[rank] = 1
    data.append(rank)

t = sorted(dict.items(),key=lambda item:item[0])
for i in t:
    print(i)

# print(cards)
# print(data)
"""
绘制直方图
data:必选参数，绘图数据
bins:直方图的长条形数目，可选项，默认为10
normed:是否将得到的直方图向量归一化，可选项，默认为0，代表不归一化，显示频数。normed=1，表示归一化，显示频率。
facecolor:长条形的颜色
edgecolor:长条形边框的颜色
alpha:透明度
"""
plt.hist(data, bins=40,range=(-2,20), facecolor="blue", edgecolor="black", alpha=0.7)
# 显示横轴标签
plt.xlabel("区间")
# 显示纵轴标签
plt.ylabel("频数/频率")
# 显示图标题
plt.title("频数/频率分布直方图")
# plt.xlim(-2,20)
plt.show()
