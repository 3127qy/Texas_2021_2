import itertools
from search  import Rank
import random


allCards = ['<0,0>','<0,1>','<0,2>','<0,3>','<0,4>','<0,5>','<0,6>','<0,7>','<0,8>','<0,9>','<0,10>','<0,11>','<0,12>',
            '<1,0>','<1,1>','<1,2>','<1,3>','<1,4>','<1,5>','<1,6>','<1,7>','<1,8>','<1,9>','<1,10>','<1,11>','<1,12>',
            '<2,0>','<2,1>','<2,2>','<2,3>','<2,4>','<2,5>','<2,6>','<2,7>','<2,8>','<2,9>','<2,10>','<2,11>','<2,12>',
            '<3,0>','<3,1>','<3,2>','<3,3>','<3,4>','<3,5>','<3,6>','<3,7>','<3,8>','<3,9>','<3,10>','<3,11>','<3,12>',]

# handCards = ('<1,0>', '<0,1>')
# boardCards = ["<2,3>","<0,2>","<3,5>"]
#
# print(Rank.rank(handCards,boardCards) / 45035996274539160 )
# 45035996274539160
# 45035996274539160

dict = {}
# for i in itertools.combinations(allCards,5):
#     handCards = i[0:2]
#     boardCards = i[2:]
#     rank,type = Rank.rank(handCards,boardCards)
#     rank = rank / 45035996274539160
#
#     if type not in dict.keys():
#         dict[type] = 1
#     else:
#         dict[type] += 1
#
#
# for i in dict.keys():
#     print(str(i) + " " + str(dict[i]))

# dict = {"1~0.9":0,"0.9~0.8":0,"0.8~0.7":0,"0.7~0.6":0,"0.6~0.5":0,"0.5~0.4":0,"0.4~0.3":0,"0.3~0.2":0,"0.2~0.1":0,"0.1~0":0}
# for i in range(0,100):
#     r = random.random()
#     if r > 0.9 and r <= 1:
#         dict["1~0.9"] += 1
#     elif r > 0.8 and r <= 0.9:
#         dict["0.9~0.8"] += 1
#     elif r > 0.7 and r <= 0.8:
#         dict["0.8~0.7"] += 1
#     elif r > 0.6 and r <= 0.7:
#         dict["0.7~0.6"] += 1
#     elif r > 0.5 and r <= 0.6:
#         dict["0.6~0.5"] += 1
#     elif r > 0.4 and r <= 0.5:
#         dict["0.5~0.4"] += 1
#     elif r > 0.3 and r <= 0.4:
#         dict["0.4~0.3"] += 1
#     elif r > 0.2 and r <= 0.3:
#         dict["0.3~0.2"] += 1
#     elif r > 0.1 and r <= 0.2:
#         dict["0.2~0.1"] += 1
#     elif r > 0 and r <= 0.1:
#         dict["0.1~0"] += 1
#
# for i in dict.keys():
#     print(i + " " +str(dict[i]))




# 获取所有还未出现的牌
def getTempAllCards(handCards,boardCards,opCards = None):

    # 先将先讲所有牌存入零时变量
    tempAllCards = allCards[0:]

    # for i in allCards:
    #     tempAllCards.append(i)

    # 再在所有牌中删去已知的牌
    for i in handCards:
        if i in tempAllCards:
            tempAllCards.remove(i)

    for i in boardCards:
        if i in tempAllCards:
            tempAllCards.remove(i)

    if opCards is not None:
        for i in opCards:
            if i in tempAllCards:
                tempAllCards.remove(i)


    return tempAllCards



def handStengthNO(handCards,boardCards):

    # 潜力值
    PPot = 0

    # 总共模拟次数
    totalCount = 400

    ahead = tied = behind = 0

    # 用与对潜力值的估计的下标
    aheadIndex = 0
    tiedIndex = 1
    behindIndex = 2

    index = 0

    #第一层所有情况
    allHPCondition = [0,0,0]

    # 第二层潜力值
    HP = [[0,0,0],
          [0,0,0],
          [0,0,0]]

    # 自己手牌的值
    maxMyRank,handType = Rank.rank(handCards, boardCards)

    print("handCards: " + str(handCards))
    print("boardCards: " + str(boardCards))
    print("handType: " + str(handType))


    # 获取所有还未出现的牌
    tempAllCards = getTempAllCards(handCards,boardCards)

    for tempOpHandCards in itertools.combinations(tempAllCards,2):
        # print("currentCount:" + str(i))

        # 模拟对手手牌
        # tempOpHandCards = creatHandCard()

        # 存储对方手牌最大的值
        maxOpRank,_ = Rank.rank(tempOpHandCards, boardCards)

        if maxMyRank > maxOpRank:
            ahead += 1
            index = aheadIndex
        elif maxMyRank == maxOpRank:
            tied += 1
            index = tiedIndex
        elif maxMyRank < maxOpRank:
            behind += 1
            index = behindIndex

        allHPCondition[index] += 1

    # #   分不同阶段估算潜力值
    #     if phase == "flop":
    #         # 获取所有还未出现的牌
    #         allUnkonwnCards = getTempAllCards(tempOpHandCards)
    #
    #         for tempCards in itertools.combinations(allUnkonwnCards, 2):
    #
    #             turnCard = tempCards[0]
    #             riverCard = tempCards[1]
    #
    #             # 将模拟出的桌面所有牌存入临时变量
    #             tempBoardCard = boardCards[0:]
    #
    #             # for i in boardCards:
    #             #     tempBoardCard.append(i)
    #
    #             tempBoardCard.append(turnCard)
    #             tempBoardCard.append(riverCard)
    #
    #             maxMyRank = Rank.rank(handCards, tempBoardCard)
    #             maxOpRank = Rank.rank(tempOpHandCards, tempBoardCard)
    #
    #             if maxMyRank > maxOpRank:
    #                 HP[index][aheadIndex] += 1
    #             elif maxMyRank == maxOpRank:
    #                 HP[index][tiedIndex] += 1
    #             elif maxMyRank < maxOpRank:
    #                 HP[index][behindIndex] += 1
    #
    #
    #
    #     elif phase == "turn":
    #         # 获取所有还未出现的牌
    #         allUnkonwnCards = getTempAllCards(tempOpHandCards)
    #
    #         # 进入river阶段模拟
    #         for riverCard in allUnkonwnCards:
    #             # 将模拟出的桌面所有牌存入临时变量
    #             tempBoardCard = boardCards[0:]
    #
    #             # for i in boardCards:
    #             #     tempBoardCard.append(i)
    #
    #             tempBoardCard.append(riverCard)
    #
    #             maxMyRank = Rank.rank(handCards, tempBoardCard)
    #             maxOpRank = Rank.rank(tempOpHandCards, tempBoardCard)
    #
    #             if maxMyRank > maxOpRank:
    #                 HP[index][aheadIndex] += 1
    #             elif maxMyRank == maxOpRank:
    #                 HP[index][tiedIndex] += 1
    #             elif maxMyRank < maxOpRank:
    #                 HP[index][behindIndex] += 1
    #
    #

    # if HP[behindIndex][aheadIndex] + HP[behindIndex][tiedIndex] / 2 + HP[tiedIndex][aheadIndex] != 0:
    #     PPot = (HP[behindIndex][aheadIndex] + HP[behindIndex][tiedIndex] / 2 + HP[tiedIndex][aheadIndex]) / (sum(HP[behindIndex][:]) + sum(HP[tiedIndex][:]) + sum(HP[aheadIndex][:]))

    # 对自己未来可能出现的牌型做预测

    # 预测手牌强度
    PHS = 0

    # 对自己未来手牌预测的牌型字典
    handsType = {"高牌": 0, "一对": 0, "两对": 0, "三条": 0, "顺子": 0, "同花": 0, "葫芦": 0, "四条": 0, "同花顺": 0, "皇家同花顺": 0}

    # 每个阶段可模拟的总次数
    count = 0

    # if phase == 'flop':
    #
    #     # c(47,2) = 1081
    #     count = 1081
    #
    #     for tempCards in itertools.combinations(tempAllCards,2):
    #
    #         # 模拟的公共牌
    #         tempBoardCards = boardCards[0:]
    #
    #         for i in tempCards:
    #             tempBoardCards.append(i)
    #
    #         rank,handType = Rank.rank(handCards,tempBoardCards)
    #
    #         handsType[handType] += 1
    #
    #
    # elif phase == 'turn':
    #
    #     # c(46,1) = 46
    #     count = 46
    #
    #     for tempCards in tempAllCards:
    #
    #         # 模拟的公共牌
    #         tempBoardCards = boardCards[0:]
    #
    #
    #         tempBoardCards.append(tempCards)
    #
    #         rank,handType = Rank.rank(handCards,tempBoardCards)
    #
    #         handsType[handType] += 1
    #
    # if phase != "river":
    #     for type in handsType.keys():
    #
    #         # 跳过预测牌型为高牌的牌型
    #         if type == "高牌":
    #             continue
    #
    #
    #         # 记录小于该牌型的牌型数
    #         lowCount = 0
    #
    #         # 先将小于该牌型的所有牌型相加
    #         for lowType in handsType.keys():
    #
    #             # 直到到了与该牌型相同情况，则退出循环
    #             if type == lowType:
    #                 break
    #
    #             lowCount += handsType[lowType]
    #
    #         PHS += (handsType[type] / count) * (lowCount / count)



    #未加入潜力值的手牌强度
    HS = (ahead + tied / 2) / (ahead + tied + behind)

    # 加入预测值的手牌强度
    HS = HS + (1-HS) * PHS



    return HS



def handStength(handCards,boardCards):

    # 潜力值
    PPot = 0

    # 总共模拟次数
    totalCount = 400

    ahead = tied = behind = 0

    # 用与对潜力值的估计的下标
    aheadIndex = 0
    tiedIndex = 1
    behindIndex = 2

    index = 0

    #第一层所有情况
    allHPCondition = [0,0,0]

    # 第二层潜力值
    HP = [[0,0,0],
          [0,0,0],
          [0,0,0]]

    # 自己手牌的值
    maxMyRank,handType = Rank.rank(handCards, boardCards)

    print("handCards: " + str(handCards))
    print("boardCards: " + str(boardCards))
    print("handType: " + str(handType))


    # 获取所有还未出现的牌
    tempAllCards = getTempAllCards(handCards,boardCards)

    for tempOpHandCards in itertools.combinations(tempAllCards,2):
        # print("currentCount:" + str(i))

        # 模拟对手手牌
        # tempOpHandCards = creatHandCard()

        # 存储对方手牌最大的值
        maxOpRank,_ = Rank.rank(tempOpHandCards, boardCards)

        if maxMyRank > maxOpRank:
            ahead += 1
            index = aheadIndex
        elif maxMyRank == maxOpRank:
            tied += 1
            index = tiedIndex
        elif maxMyRank < maxOpRank:
            behind += 1
            index = behindIndex

        allHPCondition[index] += 1

    # #   分不同阶段估算潜力值
    #     if phase == "flop":
    #         # 获取所有还未出现的牌
    #         allUnkonwnCards = getTempAllCards(tempOpHandCards)
    #
    #         for tempCards in itertools.combinations(allUnkonwnCards, 2):
    #
    #             turnCard = tempCards[0]
    #             riverCard = tempCards[1]
    #
    #             # 将模拟出的桌面所有牌存入临时变量
    #             tempBoardCard = boardCards[0:]
    #
    #             # for i in boardCards:
    #             #     tempBoardCard.append(i)
    #
    #             tempBoardCard.append(turnCard)
    #             tempBoardCard.append(riverCard)
    #
    #             maxMyRank = Rank.rank(handCards, tempBoardCard)
    #             maxOpRank = Rank.rank(tempOpHandCards, tempBoardCard)
    #
    #             if maxMyRank > maxOpRank:
    #                 HP[index][aheadIndex] += 1
    #             elif maxMyRank == maxOpRank:
    #                 HP[index][tiedIndex] += 1
    #             elif maxMyRank < maxOpRank:
    #                 HP[index][behindIndex] += 1
    #
    #
    #
    #     elif phase == "turn":
    #         # 获取所有还未出现的牌
    #         allUnkonwnCards = getTempAllCards(tempOpHandCards)
    #
    #         # 进入river阶段模拟
    #         for riverCard in allUnkonwnCards:
    #             # 将模拟出的桌面所有牌存入临时变量
    #             tempBoardCard = boardCards[0:]
    #
    #             # for i in boardCards:
    #             #     tempBoardCard.append(i)
    #
    #             tempBoardCard.append(riverCard)
    #
    #             maxMyRank = Rank.rank(handCards, tempBoardCard)
    #             maxOpRank = Rank.rank(tempOpHandCards, tempBoardCard)
    #
    #             if maxMyRank > maxOpRank:
    #                 HP[index][aheadIndex] += 1
    #             elif maxMyRank == maxOpRank:
    #                 HP[index][tiedIndex] += 1
    #             elif maxMyRank < maxOpRank:
    #                 HP[index][behindIndex] += 1
    #
    #

    # if HP[behindIndex][aheadIndex] + HP[behindIndex][tiedIndex] / 2 + HP[tiedIndex][aheadIndex] != 0:
    #     PPot = (HP[behindIndex][aheadIndex] + HP[behindIndex][tiedIndex] / 2 + HP[tiedIndex][aheadIndex]) / (sum(HP[behindIndex][:]) + sum(HP[tiedIndex][:]) + sum(HP[aheadIndex][:]))

    # 对自己未来可能出现的牌型做预测

    # 预测手牌强度
    PHS = 0

    # 对自己未来手牌预测的牌型字典
    handsType = {"高牌": 0, "一对": 0, "两对": 0, "三条": 0, "顺子": 0, "同花": 0, "葫芦": 0, "四条": 0, "同花顺": 0, "皇家同花顺": 0}

    # 每个阶段可模拟的总次数
    count = 0



    # c(47,2) = 1081
    # count = 1081

    for tempCards in itertools.combinations(tempAllCards,2):
        count += 1
        # 模拟的公共牌
        tempBoardCards = boardCards[0:]

        for i in tempCards:
            tempBoardCards.append(i)

        rank,handType = Rank.rank(handCards,tempBoardCards)

        handsType[handType] += 1


    # elif phase == 'turn':
    #
    # c(46,1) = 46
    # count = 46

    # for tempCards in tempAllCards:
    #     count += 1
    #
    #     # 模拟的公共牌
    #     tempBoardCards = boardCards[0:]
    #
    #
    #     tempBoardCards.append(tempCards)
    #
    #     rank,handType = Rank.rank(handCards,tempBoardCards)
    #
    #     handsType[handType] += 1


    for type in handsType.keys():

        # 跳过预测牌型为高牌的牌型
        if type == "高牌":
            continue


        # 记录小于该牌型的牌型数
        lowCount = 0

        # 先将小于该牌型的所有牌型相加
        for lowType in handsType.keys():

            # 直到到了与该牌型相同情况，则退出循环
            if type == lowType:
                break

            lowCount += handsType[lowType]

        PHS += (handsType[type] / count) * (lowCount / count)



    #未加入潜力值的手牌强度
    HS = (ahead + tied / 2) / (ahead + tied + behind)

    # 加入预测值的手牌强度
    HS = HS + (1-HS) * PHS




    return HS

handCards= ['<1,12>', '<0,6>']
boardCards= ['<2,10>', '<0,2>', '<2,2>']
# boardCards = ['<1,0>', '<3,2>', '<0,4>',"<0,6>","<0,8>"]

print("noHP: " + str(handStengthNO(handCards,boardCards)))

print("haveHP: " + str(handStength(handCards,boardCards)))