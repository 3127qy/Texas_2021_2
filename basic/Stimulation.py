# 该包用于模拟生成未知牌型
import random

# 52张牌
allCards = ['<0,0>','<0,1>','<0,2>','<0,3>','<0,4>','<0,5>','<0,6>','<0,7>','<0,8>','<0,9>','<0,10>','<0,11>','<0,12>',
            '<1,0>','<1,1>','<1,2>','<1,3>','<1,4>','<1,5>','<1,6>','<1,7>','<1,8>','<1,9>','<1,10>','<1,11>','<1,12>',
            '<2,0>','<2,1>','<2,2>','<2,3>','<2,4>','<2,5>','<2,6>','<2,7>','<2,8>','<2,9>','<2,10>','<2,11>','<2,12>',
            '<3,0>','<3,1>','<3,2>','<3,3>','<3,4>','<3,5>','<3,6>','<3,7>','<3,8>','<3,9>','<3,10>','<3,11>','<3,12>',]


# 生成手牌函数
def creatHandCard(hand_cards,board_cards):

    temp_op_hand_cards = []

    # 获取所有还未出现的牌
    tempAllCards = getTempAllCards(hand_cards,board_cards)

    # 再随机生成第一张对手手牌
    firstOpHandCard = tempAllCards[random.randint(0, len(tempAllCards) -1)]

    tempAllCards.remove(firstOpHandCard)

    # 再随机生成第二张对手手牌
    secondOpHandCard = tempAllCards[random.randint(0, len(tempAllCards) - 1)]

    temp_op_hand_cards.append(firstOpHandCard)
    temp_op_hand_cards.append(secondOpHandCard)

    return temp_op_hand_cards

# 获取所有还未出现的牌
def getTempAllCards(hand_cards=[],board_cards=[],opCards = None):

    # 先将先讲所有牌存入零时变量
    tempAllCards = allCards[0:]

    # 再在所有牌中删去已知的牌
    for i in hand_cards:
        if i in tempAllCards:
            tempAllCards.remove(i)

    for i in board_cards:
        if i in tempAllCards:
            tempAllCards.remove(i)

    if opCards is not None:
        for i in opCards:
            if i in tempAllCards:
                tempAllCards.remove(i)

    return tempAllCards


