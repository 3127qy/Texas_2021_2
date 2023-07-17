# 该文件主要是cfr算法核心代码

import numpy as np
import itertools
from search import Rank
from basic.Stimulation import *
from basic.node import Node
from search import Search
from basic import Basic

#cfr算法的最大迭代次数
maxIterator = 1
# maxIterator = 5
# p0,p1分别是选择行为的概率.now_player表示下一个该谁做行为 0代表自己，1代表对手,每次调用的时候交换双方的 rank
def cfr(h, p0, p1, depth, max_my_rank, max_op_rank, last_bet_chips, now_player, HS,chips_pool,temp_map):

    if len(h) > 1 or h == "f":

        if h[len(h) - 1] == 'c' and len(h) > 1:
            if max_my_rank > max_op_rank:
                return (last_bet_chips + chips_pool)
            elif max_my_rank == max_op_rank:
                return 0
            elif max_my_rank < max_op_rank:
                return -(last_bet_chips + chips_pool)

        elif h[len(h) - 1] == "f":
            if max_my_rank > max_op_rank:
                return -(last_bet_chips + chips_pool)
            elif max_my_rank == max_op_rank:
                return 0
            elif max_my_rank < max_op_rank:
                return (last_bet_chips + chips_pool)

        elif h[len(h) - 1] == 'r' and depth > 4 and h[len(h) - 2] == 'r':
            if max_my_rank > max_op_rank:
                return (last_bet_chips + chips_pool)
            elif max_my_rank == max_op_rank:
                return 0
            elif max_my_rank < max_op_rank:
                return -(last_bet_chips + chips_pool)


    if (h not in temp_map.keys()):
        temp_map[h] = Node(h)

    temp_node = temp_map[h]

    util = np.zeros((temp_node.NUM_ACTION,), dtype=float)


    strategy = temp_node.get_before_action_strategy(p0 if now_player ==0 else p1)

    nodeUtil = 0

    # for i in (0,2,1):
    i=random.randint(0,2)
        # check,call在数组中以index=0表示,raise在数组中以index=1表示,fold在数组中以index=2表示

    if i == 0:
        util[i] = (-cfr(h + "c", p0 * strategy[i], p1, depth + 1,max_op_rank,max_my_rank, last_bet_chips,
                       int(not now_player), HS,chips_pool,temp_map)) \
            if now_player == 0 else \
            (-cfr(h + "c", p0, p1 * strategy[i], depth + 1, max_op_rank,  max_my_rank, last_bet_chips,
                 int(not now_player), HS,chips_pool,temp_map))

    elif i == 2:
        util[i] = (-cfr(h + "f", p0 * strategy[i], p1, depth + 1,max_op_rank ,  max_my_rank, last_bet_chips,
                       int(not now_player), HS,chips_pool,temp_map)) \
            if now_player == 0 else \
            (-cfr(h + "f", p0, p1 * strategy[i], depth + 1, max_op_rank,  max_my_rank, last_bet_chips,
                 int(not now_player), HS,chips_pool,temp_map))

        #把raise行为放在最后，因为raise行为会改变last_bet_chips的大小，其他行为会受到last_bet_chips大小的影响
    elif i == 1:
        last_bet_chips = 110 if last_bet_chips == 0 else last_bet_chips * 2
        util[i] = (-cfr(h + "r", p0 * strategy[i], p1, depth + 1, max_op_rank, max_my_rank, last_bet_chips,
                       int(not now_player), HS,chips_pool,temp_map)) \
            if now_player == 0 else \
            (-cfr(h + "r", p0, p1 * strategy[i], depth + 1, max_op_rank, max_my_rank, last_bet_chips,
                 int(not now_player), HS,chips_pool,temp_map))

    regret = strategy[i] * util[i]
    temp_node.setRegretSum(i, p0 * regret if now_player == 0 else p1 * regret)
    nodeUtil += strategy[i] * util[i]

    # nodeUtil += (strategy[i] * util[i]) / 3
    # 计算后悔值
    # for i in range(temp_node.NUM_ACTION):
    #     regret = util[i] - nodeUtil
    #     temp_node.setRegretSum(i, p0 * regret if now_player == 0 else p1 * regret)
        # regret = 0
        # for j in range(temp_node.NUM_ACTION):
        #     regret += util[j] - util[i]
        # temp_node.setRegretSum(i, p0 * regret if now_player == 0 else p1 * regret)

    return nodeUtil


# cfr算法的触发器
def trainer(h, last_bet_chips, HS,now_palyers,hand_cards, board_cards,chips_pool):
    # 自己手牌的值
    max_my_rank, hand_type = Rank.rank(hand_cards, board_cards)

    #生成的map
    temp_map = {}

    # 获取桌面上还没有出现的牌
    tempAllCards = getTempAllCards(hand_cards, board_cards)
    boardType = Search.getBoardCardType(board_cards)

    for i in range(0, maxIterator):
        for temp_op_hand_cards in itertools.combinations(tempAllCards, 2):
            # 对方手牌的值
            max_op_rank, max_op_type = Rank.rank(temp_op_hand_cards, board_cards)

            if ((len(h) >= 1 and h[len(h)-1] == "r") or Basic.op_raise_count >= 1) and boardType == max_op_type:
                if random.random() <= 0.5:
                    continue

            cfr(h, 1, 1, 0, max_my_rank,max_op_rank, last_bet_chips,now_palyers,HS,chips_pool,temp_map)

    return temp_map