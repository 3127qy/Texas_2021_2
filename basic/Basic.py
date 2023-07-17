import winsound
import re
from search import Search
import random
import time
from search import Rank
import itertools
import logging
import traceback
from basic.node import Node
import numpy as np
from basic.Stimulation import *
from basic.CfrAlgorithm import trainer

# 最大回合数
max_bout = 70

# 每个新阶段判断是不是自己开始的标志
my_start_turn = False

# 当前阶段
phase = ""

# 位置
position = ""

# 手牌
hand_cards = []

# 公共牌
board_cards = []

# 每一阶段轮到自己走步的次数
my_count = 0

# 当前局数自己剩余筹码量
my_rest_chips = 20000

# 暂存上一阶段后自己所剩的筹码量
last_phase_my_rest_chips = 20000

# 整个局面上次raise所下注大小，用来更新底池
last_put_chips = 0

# 底池总金额
chips_pool = 0

# 需要赢的下限
win_low_limit = 101

# 自己当前行为的下注量
my_bet_chips = 0

# 对手非翻牌前阶段加注次数
op_raise_count = 0

# 对手非翻牌前阶段看牌次数
op_check_count = 0

# 下注的最低预警线
betline = 110

# cfr算法的map
cfr_map = {}

# 动作序列
action_sequence = ""

# 判断对方是大注的底线(用于判断对方是不是下大注选手),默认500
op_big_bet_line = 500

# 对方下大注的底线，默认1000
big_bet = 3000

# 对方上次下大注的量
op_last_big_bet = -1

# 判断对方是不是下大注的选手
is_big_bet_op = False

# 计算对方连续开局下大注的次数
op_continue_big_bet_num = 0

# 对方上次是否下大注
is_op_last_big_bet = False

# 对手连续下大注超过big_bet_count次后,判断其为下大注选手
big_bet_count = 3

# 写入文件的字符串
to_file_str = ""

# 加注倍率(用来调整下注的倍数)
raise_time = 1

# 对手上一个阶段第一次加注的筹码量
op_last_pahse_first_bet_chip = 0

# 标识自己是不是该阶段第一个加注的
first_raise_is_me = False

# 自己已经下了大注
already_my_big_chip = False

# 只选择弃牌的标志
only_fold = False

# 52张牌
allCards = ['<0,0>', '<0,1>', '<0,2>', '<0,3>', '<0,4>', '<0,5>', '<0,6>', '<0,7>', '<0,8>', '<0,9>', '<0,10>',
            '<0,11>', '<0,12>',
            '<1,0>', '<1,1>', '<1,2>', '<1,3>', '<1,4>', '<1,5>', '<1,6>', '<1,7>', '<1,8>', '<1,9>', '<1,10>',
            '<1,11>', '<1,12>',
            '<2,0>', '<2,1>', '<2,2>', '<2,3>', '<2,4>', '<2,5>', '<2,6>', '<2,7>', '<2,8>', '<2,9>', '<2,10>',
            '<2,11>', '<2,12>',
            '<3,0>', '<3,1>', '<3,2>', '<3,3>', '<3,4>', '<3,5>', '<3,6>', '<3,7>', '<3,8>', '<3,9>', '<3,10>',
            '<3,11>', '<3,12>', ]

"""
sk：socket通信接口
already_win_chips:已经赢取的筹码量
current_bout：当前是第几局
"""


def basic(sk, already_win_chips, current_bout):
    # 初始化函数
    clear()

    global my_start_turn, last_phase_my_rest_chips, op_raise_count, op_check_count, message, \
        last_put_chips, chips_pool, action_sequence, cfr_map, my_bet_chips, first_raise_is_me,raise_time

    # 暂存上一阶段
    last_phase = "None"

    # 无限循环接受消息
    while True:
        # time.sleep(1)
        try:
            message = sk.recv(1024).decode("utf-8")
            my_print("message: " + str(message))

            # time.sleep(2)

            # 先判断该局是否结束
            win_sign, win_chips = checkFinish(message)
            if win_sign:
                return win_chips, win_low_limit

            # 获取位置信息
            getPosition(message)

            # 获取阶段信息,成功获取阶段信息后将手牌或者公共牌存入相应变量
            getPhase(message)

            if not my_start_turn:
                my_start_turn = True
                continue

            time.sleep(0.5)
            # time.sleep(3)

            # 获取对手行为
            op_action = getOpAction(message)
            my_print("op_action: " + str(op_action))

            # 记录对方加注次数
            if phase != "preflop" and (op_action[0] == "raise" or op_action[0] == "allin"):
                op_raise_count += 1
                my_print("op_raise_count : " + str(op_raise_count))

            # 记录对方看牌次数
            if phase != "preflop" and op_action[0] == "check":
                op_check_count += 1
                my_print("op_check_count : " + str(op_check_count))

            # 如果最终局面已经赢了，直接弃牌
            if judgeAlreadyWin(already_win_chips, current_bout):
                # if False:
                # winsound.Beep(600, 1000)
                my_print("Already Win!!!!")
                time.sleep(0.5)
                sk.send("fold".encode())

            # 不是已经赢了就正常操作
            else:
                # 如果对手行为不是“fold”，我需要做决策
                if op_action[0] != "fold":
                    # time.sleep(1)
                    my_print("my_count: " + str(my_count))

                    if last_phase != phase and phase != "preflop":
                        # 清空动作序列、cfr表、自己上一次加注量、是否是自己首先下注
                        action_sequence = ""
                        cfr_map = {}
                        my_bet_chips = 0
                        first_raise_is_me = False

                        last_phase = phase
                        last_phase_my_rest_chips = my_rest_chips

                    #如果输得比较多的话就把下注量稍微提高一些
                    if already_win_chips <= -500:
                        raise_time = 2
                    else:
                        raise_time = 1

                    # 采取行动
                    if phase == "preflop":
                        doPreflop(sk, op_action, already_win_chips, current_bout)
                    elif phase == "turn" or phase == "flop":
                        doFlopAndTurn(sk, op_action, already_win_chips, current_bout)
                    elif phase == "river":
                        doFlopAndTurn(sk, op_action, already_win_chips, current_bout)

                    # my_print("my_rest_chips : " + str(my_rest_chips))

                    # 分界线
                    my_print("---")

        except Exception as e:

            time.sleep(5)
            logging.exception(e)

            continue


def clear():
    global my_start_turn, phase, position, hand_cards, board_cards, my_count, my_rest_chips, \
        my_last_put_chips, chips_pool, last_phase_my_rest_chips, op_raise_count, op_check_count, first_raise_is_me, already_my_big_chip

    my_start_turn = False
    phase = ""
    position = ""
    hand_cards = []
    board_cards = []
    my_count = 0
    my_rest_chips = 20000
    my_last_put_chips = 0
    chips_pool = 150
    last_phase_my_rest_chips = 20000
    op_raise_count = 0
    op_check_count = 0
    first_raise_is_me = False
    already_my_big_chip = False


def checkFinish(message):
    elements = re.split("[ ]", message)

    if elements[0] == "earnChips" and "oppo_hands" not in elements[1] and "preflop" not in elements[1]:
        win_chips = eval(elements[1])
        return True, win_chips
    elif elements[0] == "earnChips":
        win_chips = 0
        if "oppo_hands" in elements[1]:
            win_chips = eval(elements[1][:elements[1].index("oppo_hands")])
        elif "preflop" in elements[1]:
            win_chips = eval(elements[1][:elements[1].index("preflop")])

        return True, win_chips
    else:

        return False, 0


def my_print(s):
    global to_file_str
    to_file_str += s + "\n"
    print(s)


def to_file(already_win_chips):
    timeArray = time.localtime(time.time())  # 秒数
    time_idntity = time.strftime("%Y-%m-%d_%H.%M.%S", timeArray)

    win_s = ""
    if already_win_chips > 0:
        win_s = "赢"
    elif already_win_chips < 0:
        win_s = "输"
    else:
        win_s = "平局"

    # 写入对局信息
    file_name = "../log/" + str(time_idntity) + "_" + win_s + ".txt"
    with open(file_name, "w+", encoding="utf-8") as fp:
        fp.write(to_file_str)


# 返回能赢的最小筹码
def getWinMinChips(current_bout):
    return (max_bout - current_bout) * 75


def judgeAlreadyWin(already_win_chips, current_bout):
    # 判断自己是否已经输了
    if already_win_chips + (max_bout - current_bout) * 75 < 0:
        my_print("Already lose!!!!")

    # max_bout局后保证自己所赢筹码量大于指定数量
    if already_win_chips - (getWinMinChips(current_bout)) >= win_low_limit:
        return True
    else:
        return False


def getPhase(message):
    global phase, my_count, my_start_turn, hand_cards, board_cards, my_rest_chips, last_put_chips, chips_pool, cfr_map

    if "oppo_hands" in message and "preflop" in message:
        index = message.index("preflop")
        message = message[index:]

    elements = re.split("[|]", message)

    if (elements[0] != "oppo_hands" and len(elements) == 2 or len(elements) == 3 and "|" in message):
        phase = elements[0]
        # my_print(message)
        my_print("phase: " + str(phase))

        # 更新底池
        if phase == "flop" and last_put_chips != 0:
            chips_pool = last_put_chips * 2
        elif phase != "preflop":
            chips_pool += last_put_chips * 2
        # my_print("new pool:" + str(chips_pool) + "*" * 40)
        last_put_chips = 0

        #       进入新阶段，判断是否是自己起手
        if phase == "preflop":
            if position == "BIGBLIND":
                my_start_turn = False
                my_rest_chips -= 100
            else:
                my_start_turn = True
                my_rest_chips -= 50

            # my_print("enterNewContest my_rest_chips:" + str(my_rest_chips))
        else:
            if position == "BIGBLIND":
                my_start_turn = True
            else:
                my_start_turn = False

        #         进入新阶段，将my_count置为0
        my_count = 0

        #     成功获取阶段信息后将手牌或者公共牌存入变量
        if phase == "preflop":

            getHandCards(elements[2])
        elif phase != "oppo_hands":

            getBoardCards(elements[1])


def getPosition(message):
    global position

    if "oppo_hands" in message and "preflop" in message:
        index = message.index("preflop")
        message = message[index:]

    elements = re.split("[|]", message)

    if (len(elements) == 3):
        position = elements[1]


def getOpAction(message):
    op_action = []
    elements = re.split("[ ]", message)

    if elements[0] == "call" or elements[0] == "fold" or elements[0] == "check" or elements[0] == "allin":
        op_action.append(elements[0])
        op_action.append(0)
        return op_action

    # raise 操作平台会返回信息 raise 筹码 用 op_action[0]存储动作, 用 op_action[1] 存储筹码
    elif elements[0] == "raise":
        op_action.append(elements[0])
        op_action.append(int(eval(elements[1]) + 1))
        return op_action
    else:
        return ["None", 0]


def getHandCards(cardStr):
    global hand_cards

    tempCards = re.split("[<,>]", cardStr)

    # 将字符数组中 所有 '' 字符移除
    for i in range(0, len(tempCards)):
        if '' in tempCards:
            tempCards.remove('')

    for i in range(0, len(tempCards), 2):
        str = "<" + tempCards[i] + "," + tempCards[i + 1] + ">"
        hand_cards.append(str)


def getBoardCards(cardStr):
    global board_cards

    tempCards = re.split("[<,>]", cardStr)

    # 将字符数组中 所有 '' 字符移除
    for i in range(0, len(tempCards)):
        if '' in tempCards:
            tempCards.remove('')

    for i in range(0, len(tempCards), 2):
        str = "<" + tempCards[i] + "," + tempCards[i + 1] + ">"
        board_cards.append(str)

# 返回所赢筹码的相反数
def oppositeAlreadyWinChips(already_win_chips):
    return -already_win_chips


# 返回下大注的确切的值
def betBigChips(current_bout, already_win_chips, rate=1.0):
    # 加110 是为了设置下限
    bigChips = int(
        (getWinMinChips(current_bout) + win_low_limit + oppositeAlreadyWinChips(already_win_chips) + 110) * rate)
    if phase == "preflop":
        if bigChips >= 201:
            return bigChips
        else:
            return 201
    else:
        if bigChips >= 101:
            return bigChips
        else:
            return 101


def handStrength(hand_cards, board_cards):
    ahead = tied = behind = 0

    # 自己手牌的值
    max_my_rank, hand_type = Rank.rank(hand_cards, board_cards)

    my_print("hand_cards: " + str(hand_cards))
    my_print("board_cards: " + str(board_cards))
    my_print("hand_type: " + str(hand_type))

    boardType = Search.getBoardCardType(board_cards)
    my_print("boardType : " + str(boardType))

    # 获取所有还未出现的牌
    tempAllCards = getTempAllCards(hand_cards, board_cards)

    for temp_op_hand_cards in itertools.combinations(tempAllCards, 2):
        # my_print("currentCount:" + str(i))

        # 模拟对手手牌
        # temp_op_hand_cards = creatHandCard()

        # 存储对方手牌最大的值
        max_op_rank, max_op_type = Rank.rank(temp_op_hand_cards, board_cards)

        # 如果对方加注了，其牌型应该不小，所以直接忽略掉小的牌型
        if op_raise_count >= 1 and boardType == max_op_type:
            if random.random() <= 0.5:
                continue

        if max_my_rank > max_op_rank:
            ahead += 1

        elif max_my_rank == max_op_rank:
            tied += 1

        elif max_my_rank < max_op_rank:
            behind += 1

    # 未加入潜力值的手牌强度
    HS = (ahead + tied / 2) / (ahead + tied + behind)

    return HS


# 判断对手是不是下大注类型,同时更新对手每一阶段第一次加注大小
def judge_big_player(op_action):
    global op_continue_big_bet_num, is_big_bet_op, is_op_last_big_bet, op_last_pahse_first_bet_chip, raise_time, big_bet, op_last_big_bet

    # 先判断对手是不是下大注的类型
    if op_action[1] >= op_big_bet_line and is_big_bet_op == False:
        if is_op_last_big_bet == True:
            op_continue_big_bet_num += 1
            # 如果对方不是下固定的大注
            if op_action[1] != op_last_big_bet:
                op_last_big_bet = -1
        else:
            is_op_last_big_bet = True
            op_continue_big_bet_num += 1
            # 记录对方上次下大注的量
            op_last_big_bet = op_action[1]

        if op_continue_big_bet_num >= big_bet_count:
            is_big_bet_op = True
            # 把底线稍微提高
            if op_last_big_bet != -1 and op_last_big_bet >= 1500:
                big_bet = int(op_last_big_bet * 1.1)
            else:
                big_bet = int(big_bet * 1.5)

    elif is_big_bet_op == False:
        op_continue_big_bet_num = 0
        is_op_last_big_bet = False

    my_print("is_big_bet_op: " + str(is_big_bet_op))
    # op_last_pahse_first_bet_chip = op_action[1]


# 判断对方是否是下的大注
def is_big_op_chip(op_action):

    my_print("big_bet: " + str(big_bet))
    # 如果对方不是下大注的选手，但却下了非常大的注(大注下限/上次加注的4倍),需警惕，
    # 如果是自己第一个加注（自己首先加小注），范围就放宽一些
    if is_big_bet_op is False \
            and ((first_raise_is_me and op_action[1] > (big_bet if (last_put_chips == 0) else (last_put_chips * 10)))
                 or ((not first_raise_is_me) and op_action[1] > (big_bet if (last_put_chips == 0) else (last_put_chips * 4)))):
        return True
    # 如果对方是下大注的选手，但却下了非常大的注(大注下限/上次加注的4倍),需警惕，
    # 如果是自己第一个加注（自己首先加小注），范围就放宽一些
    elif is_big_bet_op is True \
            and ((first_raise_is_me and op_action[1] > (big_bet if (last_put_chips == 0) else (last_put_chips * 15)))
                 or ((not first_raise_is_me) and op_action[1] > (big_bet if (last_put_chips == 0) else (last_put_chips * 4)))):
        return True

    return False


def doPreflop(sk, op_action, already_win_chips, current_bout):
    global my_count, my_rest_chips, my_last_put_chips, chips_pool, last_phase_my_rest_chips, my_bet_chips, \
        last_put_chips, is_big_bet_op, op_continue_big_bet_num, is_op_last_big_bet, op_last_pahse_first_bet_chip, \
        action_sequence, first_raise_is_me

    action = None

    HS = Search.preflop(hand_cards)
    my_print("hand_cards: " + str(hand_cards))
    my_print("HS:" + str(HS))

    if HS >= 13:
        my_print("BigPreflop!！！")

    elif HS >= 8 and HS < 13:
        my_print("MiddlePreflop!！！")

    if position == "SMALLBLIND":

        # 如果对手选择allin
        if op_action[0] == "allin" and action is None:
            if HS >= 8:
                action = "call"
            else:
                action = "fold"

        if my_count == 0 and action is None:

            # 主动弃牌
            if only_fold and random.random() < 0.9:
                action = "fold"

            if HS >= 13 and action is None:
                my_bet_chips = 201 * (raise_time // 2 + 1)
                action = "raise " + str(my_bet_chips)
                my_rest_chips = last_phase_my_rest_chips - my_bet_chips
                first_raise_is_me = True

            elif HS >= 3 and HS < 13 and action is None:

                action = "call"
                my_rest_chips -= 50
                chips_pool = 200

            elif HS >= 1 and HS < 3 and action is None:

                action = "call"
                my_rest_chips -= 50
                chips_pool = 200

            elif HS < 1 and action is None:
                options = ["call", "fold"]
                action = options[random.randint(0, 1)]
                if action == "call":
                    my_rest_chips -= 50
                    chips_pool = 200

        elif my_count == 1 and action is None:

            # 如果对手选择加注
            if op_action[0] == "raise":

                # judge_big_player(op_action)

                if HS >= 13 and action is None:

                    if (op_action[1] * 2) >= betBigChips(current_bout, already_win_chips, 0.25):
                        my_bet_chips = op_action[1] * 2
                        action = "raise " + str(my_bet_chips)
                        my_rest_chips = last_phase_my_rest_chips - my_bet_chips
                    else:
                        my_bet_chips = betBigChips(current_bout, already_win_chips, 0.25)
                        action = "raise " + str(my_bet_chips)
                        my_rest_chips = last_phase_my_rest_chips - my_bet_chips

                elif HS >= 8 and HS < 13 and action is None:

                    action = "call"
                    my_rest_chips = last_phase_my_rest_chips - op_action[1]

                elif HS >= 5 and HS < 8 and action is None:

                    action = "call"
                    my_rest_chips = last_phase_my_rest_chips - op_action[1]

                elif HS >= 1 and HS < 5 and action is None:

                    # 判断对方是否下大注
                    if is_big_op_chip(op_action):
                        action = "fold"
                    else:
                        action = "call"
                        my_rest_chips = last_phase_my_rest_chips - op_action[1]

                    if my_rest_chips <= 0:
                        action = "fold"

                elif HS < 1 and action is None:
                    action = "fold"

            # 如果对方选择check
            elif op_action[0] == "check":

                if HS >= 8 and action is None:
                    my_bet_chips = 201 * (raise_time//2 + 1)
                    action = "raise " + str(my_bet_chips)
                    my_rest_chips = last_phase_my_rest_chips - my_bet_chips
                    first_raise_is_me = True
                else:
                    action = "check"

        # 只有自己HS>=8才会进入这里
        elif my_count >= 2 and action is None:
            action = "call"
            my_rest_chips = last_phase_my_rest_chips - op_action[1]

    elif position == "BIGBLIND":

        # 如果对手选择allin,对方allin自己第一次做行为时选择check
        if my_count != 0 and op_action[0] == "allin" and action is None:
            if HS >= 8:
                action = "call"
            else:
                action = "fold"

        if my_count == 0 and action is None:

            # 主动弃牌
            if only_fold and random.random() < 0.9:
                action = "fold"

            # 如果对手选择allin
            if op_action[0] == "allin" and action is None:
                # 修改底池
                # chips_pool = 20100
                # action = "check"
                action = "fold"

            # 如果对手选择跟注
            if op_action[0] == 'call':

                # 修改底池
                chips_pool = 200

                if HS >= 13 and action is None:
                    my_bet_chips = 201 * (raise_time//2 + 1)
                    action = "raise " + str(my_bet_chips)
                    my_rest_chips = last_phase_my_rest_chips - my_bet_chips
                    first_raise_is_me = True

                elif HS >= 3 and HS < 13 and action is None:

                    my_bet_chips = 201
                    action = "raise " + str(my_bet_chips)
                    my_rest_chips = last_phase_my_rest_chips - my_bet_chips
                    first_raise_is_me = True

                elif HS < 3 and action is None:
                    # action = "check"
                     action = "fold"



            # 如果对手选择加注
            elif op_action[0] == "raise":

                # judge_big_player(op_action)

                if HS >= 13 and action is None:

                    # action = "check"

                    if (op_action[1] * 2) >= betBigChips(current_bout, already_win_chips, 0.25):
                        my_bet_chips = op_action[1] * 2
                        action = "raise " + str(my_bet_chips)
                        my_rest_chips = last_phase_my_rest_chips - my_bet_chips
                    else:
                        my_bet_chips = betBigChips(current_bout, already_win_chips, 0.25)
                        action = "raise " + str(my_bet_chips)
                        my_rest_chips = last_phase_my_rest_chips - my_bet_chips

                    # if (op_action[1] * 2) >= betBigChips(current_bout, already_win_chips, 0.25):
                    #     my_bet_chips = op_action[1] * 2
                    #     action = "raise " + str(my_bet_chips)
                    #     my_rest_chips = last_phase_my_rest_chips - my_bet_chips
                    # else:
                    #     my_bet_chips = betBigChips(current_bout, already_win_chips, 0.25)
                    #     action = "raise " + str(my_bet_chips)
                    #     my_rest_chips = last_phase_my_rest_chips - my_bet_chips

                elif HS >= 8 and HS < 13 and action is None:
                    # action = "check"
                    action = "call"
                    my_rest_chips = last_phase_my_rest_chips - op_action[1]


                elif HS >= 5 and HS < 8 and action is None:
                    # action = "check"
                    action = "call"
                    my_rest_chips = last_phase_my_rest_chips - op_action[1]

                elif HS >= 1 and HS < 5 and action is None:
                    # 判断对方是否下大注
                    if is_big_op_chip(op_action):
                        action = "fold"
                    else:
                        action = "call"
                        my_rest_chips = last_phase_my_rest_chips - op_action[1]

                    if my_rest_chips <= 0:
                        action = "fold"
                    # action = "check"

                elif HS < 1 and action is None:
                    # action = "check"
                    action = "fold"


        elif my_count >= 1 and action is None:

            # 如果对手选择加注
            if op_action[0] == "raise":

                if HS >= 13 and action is None:

                    if (op_action[1] * 2) >= betBigChips(current_bout, already_win_chips, 0.25):
                        my_bet_chips = op_action[1] * 2
                        action = "raise " + str(my_bet_chips)
                        my_rest_chips = last_phase_my_rest_chips - my_bet_chips
                    else:
                        my_bet_chips = betBigChips(current_bout, already_win_chips, 0.25)
                        action = "raise " + str(my_bet_chips)
                        my_rest_chips = last_phase_my_rest_chips - my_bet_chips



                elif HS >= 8 and HS < 13 and action is None:

                    action = "call"
                    my_rest_chips = last_phase_my_rest_chips - op_action[1]


                elif HS >= 5 and HS < 8 and action is None:

                    action = "call"
                    my_rest_chips = last_phase_my_rest_chips - op_action[1]

                elif HS >= 1 and HS < 5 and action is None:

                    # 判断对方是否下大注
                    if is_big_op_chip(op_action):
                        action = "fold"
                    else:
                        action = "call"
                        my_rest_chips = last_phase_my_rest_chips - op_action[1]

                    if my_rest_chips <= 0:
                        action = "fold"

                elif HS < 1 and action is None:
                    action = "fold"

        # 只有自己HS>=8才会进入这里
        elif my_count >= 2 and action is None:
            action = "call"
            my_rest_chips = last_phase_my_rest_chips - op_action[1]

    if action is None:
        action = "fold"

    my_count = my_count + 1

    if "raise" in action:
        last_put_chips = my_bet_chips

    if my_rest_chips <= 0 and action != "fold":
        action = "allin"

    my_print("myAction: " + action)
    sk.send(action.encode())


# 获取下一个行为
def getNextAction(h):
    temp_map = cfr_map[h]

    r = random.random()

    strategy = temp_map.getStrategy(1)
    strategySum = temp_map.getStrategySum()
    regertSum = temp_map.getRegretSum()
    my_print("regertSum: " + str(regertSum))
    my_print("strategy: " + str(strategy))
    # my_print("strategySum: " + str(strategySum))

    # 如果出现regertSum: [0. 0. 0.]，表示模拟出赢和输的次数相同，
    # HS在0.5左右会出现，并且概率非常小
    if regertSum[0] == regertSum[1] and regertSum[1] == regertSum[2]:
        return "fold"

    temp_sum = 0

    i = 0
    while i < temp_map.NUM_ACTION:
        temp_sum += strategy[i]

        if (r < temp_sum):
            break

        i += 1

    if i == 0:
        return "call"
    elif i == 1:
        return "raise"
    elif i == 2:
        return "fold"


def doFlopAndTurn(sk, op_action, already_win_chips, current_bout):
    global my_count, my_rest_chips, my_last_put_chips, chips_pool, last_phase_my_rest_chips, my_bet_chips, \
        last_put_chips, is_big_bet_op, op_continue_big_bet_num, is_op_last_big_bet, action_sequence, cfr_map, first_raise_is_me, already_my_big_chip

    # 最终行为
    action = None

    # 经过模拟之后得到的手牌强度
    HS = handStrength(hand_cards, board_cards)
    my_print("HS:" + str(HS))

    # 开始做决策
    if position == "BIGBLIND":

        if op_action[0] == "allin":
            if HS >= (0.8 if phase == "river" else 0.9) or already_my_big_chip is True:
                action = "call"
            else:
                action = "fold"

        if already_my_big_chip is True and action is None:
            action = "allin"

        # 第一次做行为
        if my_count == 0 and action is None:

            action_sequence = ""
            # 开始训练
            cfr_map = trainer(action_sequence, 0, HS, 0, hand_cards, board_cards, chips_pool)
            next_action = getNextAction(action_sequence)

            if (next_action == "call" or next_action == "fold") and action is None:
                # 随机加注
                if random.random() < 0.8:
                    my_bet_chips = 101
                    action = "raise " + str(my_bet_chips)
                    my_rest_chips = last_phase_my_rest_chips - my_bet_chips
                    action_sequence += "r"
                    first_raise_is_me = True
                else:
                    action = "check"
                    action_sequence += "c"

            elif next_action == "raise" and action is None:
                my_bet_chips = 110 * raise_time
                action = "raise " + str(my_bet_chips)
                my_rest_chips = last_phase_my_rest_chips - my_bet_chips
                first_raise_is_me = True
                action_sequence += "r"

        # 第二次做行为
        elif my_count >= 1 and action is None:
            # 大盲第二次做行为，只能收到对方 raise 的消息
            if op_action[0] == "raise":

                # 如果我上一次是call行为，对方第一次加注
                if action_sequence[len(action_sequence) - 1] == 'c':
                    judge_big_player(op_action)

                action_sequence += "r"

                # 判断对方是否下大注
                if is_big_op_chip(op_action):
                    if HS >= (0.8 if phase == "river" else 0.9):
                        if op_action[1] * 2 >= int(my_rest_chips * 0.4 + 110):
                            my_bet_chips = op_action[1] * 2
                            action = "raise " + str(my_bet_chips)
                            my_rest_chips = last_phase_my_rest_chips - my_bet_chips
                            first_raise_is_me = False
                            already_my_big_chip = True
                        else:
                            my_bet_chips = int(my_rest_chips * 0.4 + 110)
                            action = "raise " + str(my_bet_chips)
                            my_rest_chips = last_phase_my_rest_chips - my_bet_chips
                            action_sequence += "r"
                            already_my_big_chip = True
                            my_print("big")
                    else:
                        action = "fold"

                cfr_map = trainer(action_sequence, op_action[1], HS, 0, hand_cards, board_cards, chips_pool)
                next_action = getNextAction(action_sequence)

                if (next_action == "call" or next_action == "raise") and action is None:

                    if HS >= (0.8 if phase == "river" else 0.9) and my_count < 2:
                        if op_action[1] * 2 >= betBigChips(current_bout, already_win_chips, 1):
                            my_bet_chips = op_action[1] * 2

                        else:
                            my_bet_chips = betBigChips(current_bout, already_win_chips, 1)


                        # already_my_big_chip = True
                        action = "raise " + str(my_bet_chips)
                        my_rest_chips = last_phase_my_rest_chips - my_bet_chips
                        first_raise_is_me = False
                        action_sequence += "r"

                    else:
                        action = "call"
                        my_rest_chips = last_phase_my_rest_chips - op_action[1]
                        action_sequence += "c"


                elif next_action == "fold" and action is None:
                    action = "fold"

    elif position == "SMALLBLIND":

        if op_action[0] == "allin":
            if HS >= (0.8 if phase == "river" else 0.9) or already_my_big_chip is True:
                action = "call"
            else:
                action = "fold"

        if already_my_big_chip is True and action is None:
            action = "allin"

        # 第一次做行为
        if my_count == 0 and action is None:
            action_sequence = ""
            if op_action[0] == "check":
                action_sequence += "c"

                my_bet_chips = 101
                action = "raise " + str(my_bet_chips)
                my_rest_chips = last_phase_my_rest_chips - my_bet_chips
                action_sequence += "r"
                first_raise_is_me = True

            elif op_action[0] == "raise":
                action_sequence += "r"
                judge_big_player(op_action)

                # 判断对方是否下大注
                if is_big_op_chip(op_action):
                    if HS >= (0.8 if phase == "river" else 0.9):
                        if op_action[1] * 2 >= int(my_rest_chips * 0.4 + 110):
                            my_bet_chips = op_action[1] * 2
                            action = "raise " + str(my_bet_chips)
                            my_rest_chips = last_phase_my_rest_chips - my_bet_chips
                            first_raise_is_me = False
                            already_my_big_chip = True
                        else:
                            my_bet_chips = int(my_rest_chips * 0.4 + 110)
                            action = "raise " + str(my_bet_chips)
                            my_rest_chips = last_phase_my_rest_chips - my_bet_chips
                            action_sequence += "r"
                            already_my_big_chip = True
                            my_print("big")
                    else:
                        action = "fold"

            # 开始训练
            cfr_map = trainer(action_sequence, op_action[1], HS, 0, hand_cards, board_cards, chips_pool)
            next_action = getNextAction(action_sequence)

            if next_action == "call" and action is None:
                action = "call"
                if op_action[0] == "raise":
                    my_rest_chips = last_phase_my_rest_chips - op_action[1]
                action_sequence += "c"

            elif next_action == "raise" and action is None:

                if op_action[0] == "raise":
                    my_bet_chips = op_action[1] * 2
                else:
                    my_bet_chips = 110 * raise_time
                    first_raise_is_me = True

                action = "raise " + str(my_bet_chips)
                my_rest_chips = last_phase_my_rest_chips - my_bet_chips

                action_sequence += "r"


            elif next_action == "fold" and action is None:
                if op_action[0] == "check":
                    action = "call"
                    action_sequence += "c"

                else:
                    action = "fold"


        # 第二次做行为
        elif my_count >= 1 and action is None:
            # 第二次做行为，只能收到对方 raise 的消息
            if op_action[0] == "raise":

                # 判断对方是否下大注
                if is_big_op_chip(op_action):
                    if HS >= (0.8 if phase == "river" else 0.9):
                        if op_action[1] * 2 >= int(my_rest_chips * 0.4 + 110):
                            my_bet_chips = op_action[1] * 2
                            action = "raise " + str(my_bet_chips)
                            my_rest_chips = last_phase_my_rest_chips - my_bet_chips
                            first_raise_is_me = False
                            already_my_big_chip = True
                        else:
                            my_bet_chips = int(my_rest_chips * 0.4 + 110)
                            action = "raise " + str(my_bet_chips)
                            my_rest_chips = last_phase_my_rest_chips - my_bet_chips
                            action_sequence += "r"
                            already_my_big_chip = True
                            my_print("big")
                    else:
                        action = "fold"

                action_sequence += "r"

                cfr_map = trainer(action_sequence, op_action[1], HS, 0, hand_cards, board_cards, chips_pool)
                next_action = getNextAction(action_sequence)

                if (next_action == "call" or next_action == "raise") and action is None:

                    if HS >= (0.8 if phase == "river" else 0.9) and my_count < 2:
                        if op_action[1] * 2 >= betBigChips(current_bout, already_win_chips, 1):
                            my_bet_chips = op_action[1] * 2

                        else:
                            my_bet_chips = betBigChips(current_bout, already_win_chips, 1)


                        # already_my_big_chip = True
                        action = "raise " + str(my_bet_chips)
                        my_rest_chips = last_phase_my_rest_chips - my_bet_chips
                        first_raise_is_me = False
                        action_sequence += "r"

                    else:
                        action = "call"
                        my_rest_chips = last_phase_my_rest_chips - op_action[1]
                        action_sequence += "c"

                elif next_action == "fold" and action is None:
                    action = "fold"

    if action is None:
        action = "fold"

    my_count = my_count + 1

    if "raise" in action:
        last_put_chips = my_bet_chips

    if my_rest_chips <= 0 and action != "fold":
        action = "allin"

    my_print("myAction: " + action)
    sk.send(action.encode())

