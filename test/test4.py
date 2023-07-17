import random
from search import Search

# allCards = ['<0,0>','<0,1>','<0,2>','<0,3>','<0,4>','<0,5>','<0,6>','<0,7>','<0,8>','<0,9>','<0,10>','<0,11>','<0,12>',
# #             '<1,0>','<1,1>','<1,2>','<1,3>','<1,4>','<1,5>','<1,6>','<1,7>','<1,8>','<1,9>','<1,10>','<1,11>','<1,12>',
# #             '<2,0>','<2,1>','<2,2>','<2,3>','<2,4>','<2,5>','<2,6>','<2,7>','<2,8>','<2,9>','<2,10>','<2,11>','<2,12>',
# #             '<3,0>','<3,1>','<3,2>','<3,3>','<3,4>','<3,5>','<3,6>','<3,7>','<3,8>','<3,9>','<3,10>','<3,11>','<3,12>',]
# #
# #
# # list = []
# # for i in range(0,len(allCards)):
# #     list.append(i)
# #
# #
# # dict = {}
# # rateDict = {}
# # for i in range(-1,21):
# #     dict[i] = 0
# #     rateDict[i] = 0
# #
# # for i in range(0,100000):
# #     one = random.randint(0,51)
# #     two = -1
# #     while True:
# #         two = random.randint(0,51)
# #         if one != two:
# #             break
# #
# #     handCards = [allCards[one],allCards[two]]
# #
# #     rank = Search.preflop(handCards)
# #
# #     dict[rank] += 1
# #
# #
# # for rank in dict.keys():
# #
# #
# #     lowCount = 0
# #
# #     for lowRank in dict.keys():
# #
# #         if lowRank == rank:
# #             break
# #
# #         lowCount += dict[lowRank]
# #
# #
# #     rateDict[rank] = (dict[rank] / 100000) * (lowCount / 100000)
# #
# # for i in rateDict.keys():
# #     print(str(i) )
# #
# #
# # for i in rateDict.keys():
# #
# #     print(str(rateDict[i]))
# #
# #
# # for i in rateDict.keys():
# #
# #     print(str(i) + " " + str(rateDict[i]))


# action  = 'raise 100'
#
# if "raise" in action:
#     print(1)

hands = ["<0,6>","<0,1>"]

print(Search.preflop(hands))