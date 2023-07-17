import itertools,time
from search import Rank


# # 52张牌
allCards = ['<0,0>','<0,1>','<0,2>','<0,3>','<0,4>','<0,5>','<0,6>','<0,7>','<0,8>','<0,9>','<0,10>','<0,11>','<0,12>',
            '<1,0>','<1,1>','<1,2>','<1,3>','<1,4>','<1,5>','<1,6>','<1,7>','<1,8>','<1,9>','<1,10>','<1,11>','<1,12>',
            '<2,0>','<2,1>','<2,2>','<2,3>','<2,4>','<2,5>','<2,6>','<2,7>','<2,8>','<2,9>','<2,10>','<2,11>','<2,12>',
            '<3,0>','<3,1>','<3,2>','<3,3>','<3,4>','<3,5>','<3,6>','<3,7>','<3,8>','<3,9>','<3,10>','<3,11>','<3,12>',]


# tempallCards = []
#
# for i in allCards:
#     tempallCards.append(i)
#
#
#
# tempallCards.pop(1)
# tempallCards.pop(3)
# tempallCards.pop(5)
# tempallCards.pop(8)
#
# print(len(tempallCards))
# print(len(allCards))


# ahead = tied = behind = 0
#
# print(ahead)
# print(tied)
# print(behind)

#
# def getTempAllCards(opCards = None):
#     print(opCards)
#
#
# getTempAllCards(1)
#
# temp = []
# starttime = time.time()
#
#
# for i in range(0,len(allCards) - 1):
#     for j in range(i + 1,len(allCards)):
#         temp.append(allCards[i])
#
# endtime = time.time()
# dtime = endtime - starttime
# print(dtime)
#
# print(len(temp))
#
#
#
# temp = []
#
# starttime = time.time()
#
# for i in itertools.combinations(allCards,2):
#     temp.append(i)
#
# endtime = time.time()
# dtime = endtime - starttime
# print(dtime)
#
# print(len(temp))


# handCards = ["<2,10>","<1,12>"]
# boardCards = ["<2,11>","<0,0>","<1,3>","<2,10>", '<2,7>']
#
#
# starttime = time.time()
#
# Rank.rank(handCards,boardCards)
#
# endtime = time.time()
# dtime = endtime - starttime
# print(dtime)


# a = [[1,2,3],
#      [4,5,6],
#      [7,8,9]]
#
# print(a[0][:])
# print(sum(a[0][:]))
