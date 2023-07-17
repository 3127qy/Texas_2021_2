import itertools
from search import Search,Rank
import basic.Stimulation as Stimulation
import time
from multiprocessing.dummy import Pool as ThreadPool
from threading import Thread
import threading
# 52张牌
allCards = ['<0,0>','<0,1>','<0,2>','<0,3>','<0,4>','<0,5>','<0,6>','<0,7>','<0,8>','<0,9>','<0,10>','<0,11>','<0,12>',
            '<1,0>','<1,1>','<1,2>','<1,3>','<1,4>','<1,5>','<1,6>','<1,7>','<1,8>','<1,9>','<1,10>','<1,11>','<1,12>',
            '<2,0>','<2,1>','<2,2>','<2,3>','<2,4>','<2,5>','<2,6>','<2,7>','<2,8>','<2,9>','<2,10>','<2,11>','<2,12>',
            '<3,0>','<3,1>','<3,2>','<3,3>','<3,4>','<3,5>','<3,6>','<3,7>','<3,8>','<3,9>','<3,10>','<3,11>','<3,12>',]

cnt = {}
score = {}
for i in range(-2,22):
    cnt[i] = score[i] = 0


s = time.time()
lock=threading.Lock()
def before_do(card):
    get_score(card[0],card[1],card[2])
def get_score(my,op,boards):
    HS = Search.preflop(my)

    cnt[HS] += 1


    win = 0
    tid = 0

    for b in boards:
        my_rank, _ = Rank.rank(my, b)
        op_rank, _ = Rank.rank(op, b)

        if my_rank > op_rank:
            win += 1
        elif my_rank == op_rank:
            tid += 1


    score[HS] += (win + tid / 2)

total_score = {}
t = len(list(itertools.combinations(allCards,5)))
for all_cards in itertools.combinations(allCards,5):
    h = all_cards[0:2]
    b = all_cards[2:]
    total_score[all_cards] = Rank.rank(h, b)
    print(t)
    t-=1

# for temp_my_hand_cards in itertools.combinations(['<0,0>','<0,1>'],2):
#
#     total_op_cards = Stimulation.getTempAllCards(temp_my_hand_cards)
#
#     for temp_op_cards in itertools.combinations(['<0,2>','<0,3>','<0,4>','<0,5>'],2):
#         total_board_cards = Stimulation.getTempAllCards(temp_my_hand_cards, temp_op_cards)
#
#
#
#         pa = [temp_my_hand_cards]
#         pa.append(temp_op_cards)
#         pa.append(list(itertools.combinations(total_board_cards, 3)))
#
#         # t = list(itertools.combinations(total_board_cards, 3))
#         # a = [temp_my_hand_cards for i in range(len(t))]
#         # pa = [temp_op_cards for i in range(len(t))]
#         # pa = list(zip(a,pa,t))
#
#         t = Thread(target=get_score,args=pa)
#         t.start()
#         t.join()
#
#         # pool = ThreadPool()
#         # pool.map(before_do, pa)
#         # pool.close()
#         # pool.join()
#
# # for t in threads:
# #     t.join()

print(time.time() - s)


for i in range(-2,22):
    if cnt[i] != 0:
        score[i] = score[i] // cnt[i]

for key in score.keys():
    print(str(key) + "   " + str(score[key]))


