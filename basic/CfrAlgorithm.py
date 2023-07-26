# 该文件主要是cfr算法核心代码

import numpy as np
import itertools
from search import Rank
from basic.Stimulation import *
from basic.node import Node
from search import Search
from basic import Basic

# cfr算法的最大迭代次数
maxIterator = 1
# maxIterator = 5
"""
   CFR算法的主要递归函数。

   参数：
   h：一个表示游戏中动作历史的字符串。
   p0 和 p1：分别表示当前玩家和对手选择行为的概率。
   depth：当前节点在游戏树中的深度。
   max_my_rank 和 max_op_rank：分别表示当前玩家和对手手牌的牌型值。
   last_bet_chips：上一次行动下注的筹码数量。
   now_player：一个整数（0或1），表示当前玩家（0表示自己，1表示对手）每次调用的时候交换双方的 rank。
   chips_pool：筹码池中的总筹码数量。
   temp_map：一个字典，用于存储游戏树中的节点以及它们对应的策略和后悔值。
   c:跟注 f 弃牌 r加注
   返回值：
   返回当前节点的效用值（expected value）。
   """


def cfr(h, p0, p1, depth, max_my_rank, max_op_rank, last_bet_chips, now_player, HS, chips_pool, temp_map):
    # 如果历史动作长度大于1或为"f"（弃牌），进入终止状态判断
    if len(h) > 1 or h == "f":
        # 终止状态时的效用计算
        if h[len(h) - 1] == 'c' and len(h) > 1:
            # 自己的牌型大于对手，返回获得的筹码
            if max_my_rank > max_op_rank:
                return (last_bet_chips + chips_pool)
            # 自己的牌型与对手相等，返回0
            elif max_my_rank == max_op_rank:
                return 0
            # 自己的牌型小于对手，返回损失的筹码
            elif max_my_rank < max_op_rank:
                return -(last_bet_chips + chips_pool)

        elif h[len(h) - 1] == "f":
            # 自己弃牌，对手获胜，返回损失的筹码
            if max_my_rank > max_op_rank:
                return -(last_bet_chips + chips_pool)
                # 自己弃牌，对手弃牌或与自己牌型相等，返回0
            elif max_my_rank == max_op_rank:
                return 0
            # 自己弃牌，对手牌型较小，返回获得的筹码
            elif max_my_rank < max_op_rank:
                return (last_bet_chips + chips_pool)

        elif h[len(h) - 1] == 'r' and depth > 4 and h[len(h) - 2] == 'r':
            # 过多次加注后，两次加注者都没有弃牌，根据牌型判断获胜者，返回相应的筹码
            if max_my_rank > max_op_rank:
                return (last_bet_chips + chips_pool)
            elif max_my_rank == max_op_rank:
                return 0
            elif max_my_rank < max_op_rank:
                return -(last_bet_chips + chips_pool)

    # 若历史动作未在临时映射中，则创建新的节点
    if (h not in temp_map.keys()):
        temp_map[h] = Node(h)

    temp_node = temp_map[h]
    # 创建动作效用数组
    util = np.zeros((temp_node.NUM_ACTION,), dtype=float)

    # 获取当前节点的策略
    strategy = temp_node.get_before_action_strategy(p0 if now_player == 0 else p1)
    # 初始化节点效用
    nodeUtil = 0

    # for i in (0,2,1):
    # 随机选择一个动作进行递归
    i = random.randint(0, 2)
    # check,call在数组中以index=0表示,raise在数组中以index=1表示,fold在数组中以index=2表示

    if i == 0:
        # 如果当前玩家是自己(0)，则递归时调用函数交换双方的概率和手牌值，否则交换对手的概率和手牌值
        util[i] = (-cfr(h + "c", p0 * strategy[i], p1, depth + 1, max_op_rank, max_my_rank, last_bet_chips,
                        int(not now_player), HS, chips_pool, temp_map)) \
            if now_player == 0 else \
            (-cfr(h + "c", p0, p1 * strategy[i], depth + 1, max_op_rank, max_my_rank, last_bet_chips,
                  int(not now_player), HS, chips_pool, temp_map))

    elif i == 2:
        util[i] = (-cfr(h + "f", p0 * strategy[i], p1, depth + 1, max_op_rank, max_my_rank, last_bet_chips,
                        int(not now_player), HS, chips_pool, temp_map)) \
            if now_player == 0 else \
            (-cfr(h + "f", p0, p1 * strategy[i], depth + 1, max_op_rank, max_my_rank, last_bet_chips,
                  int(not now_player), HS, chips_pool, temp_map))

        # 把raise行为放在最后，因为raise行为会改变last_bet_chips的大小，其他行为会受到last_bet_chips大小的影响
    elif i == 1:
        last_bet_chips = 110 if last_bet_chips == 0 else last_bet_chips * 2
        util[i] = (-cfr(h + "r", p0 * strategy[i], p1, depth + 1, max_op_rank, max_my_rank, last_bet_chips,
                        int(not now_player), HS, chips_pool, temp_map)) \
            if now_player == 0 else \
            (-cfr(h + "r", p0, p1 * strategy[i], depth + 1, max_op_rank, max_my_rank, last_bet_chips,
                  int(not now_player), HS, chips_pool, temp_map))

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


# CFR算法的触发器函数
# h: 一个字符串，表示游戏中已经发生的动作历史
# last_bet_chips: 上一次行动下注的筹码数量
# HS: 未在代码片段中明确表示，可能是与游戏相关的信息
# now_players: 当前进行行动的玩家，0表示自己，1表示对手
# hand_cards: 自己手牌
# board_cards: 桌面上的公共牌
# chips_pool: 筹码池中的总筹码数量
def trainer(h, last_bet_chips, HS, now_palyers, hand_cards, board_cards, chips_pool):
    # 自己手牌的值
    max_my_rank, hand_type = Rank.rank(hand_cards, board_cards)

    # 生成的map
    temp_map = {}

    # 获取桌面上还没有出现的牌
    tempAllCards = getTempAllCards(hand_cards, board_cards)
    boardType = Search.getBoardCardType(board_cards)
    # 进行CFR的迭代
    for i in range(0, maxIterator):
        for temp_op_hand_cards in itertools.combinations(tempAllCards, 2):
            # 对方手牌的值
            max_op_rank, max_op_type = Rank.rank(temp_op_hand_cards, board_cards)

            # 如果有过raise并且对手的手牌类型和当前牌桌牌型相同，有50%的几率跳过此次迭代，以提高效率
            if ((len(h) >= 1 and h[len(h) - 1] == "r") or Basic.op_raise_count >= 1) and boardType == max_op_type:
                if random.random() <= 0.5:
                    continue
            # 调用cfr函数更新策略和后悔值
            cfr(h, 1, 1, 0, max_my_rank, max_op_rank, last_bet_chips, now_palyers, HS, chips_pool, temp_map)

    return temp_map
