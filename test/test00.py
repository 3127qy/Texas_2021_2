import itertools
from search import Search,Rank
import basic.Stimulation as Stimulation
import time
# 52张牌
allCards = ['<0,0>','<0,1>','<0,2>','<0,3>','<0,4>','<0,5>','<0,6>','<0,7>','<0,8>','<0,9>','<0,10>','<0,11>','<0,12>',
            '<1,0>','<1,1>','<1,2>','<1,3>','<1,4>','<1,5>','<1,6>','<1,7>','<1,8>','<1,9>','<1,10>','<1,11>','<1,12>',
            '<2,0>','<2,1>','<2,2>','<2,3>','<2,4>','<2,5>','<2,6>','<2,7>','<2,8>','<2,9>','<2,10>','<2,11>','<2,12>',
            '<3,0>','<3,1>','<3,2>','<3,3>','<3,4>','<3,5>','<3,6>','<3,7>','<3,8>','<3,9>','<3,10>','<3,11>','<3,12>',]

cnt = {}
score = {}
for i in range(-2,22):
    cnt[i] = score[i] = 0

sum = 28094757600
s = time.time()
for temp_my_hand_cards in itertools.combinations(allCards,2):
    # HS = Search.preflop(temp_my_hand_cards)
    # cnt[HS] += 1
    total_op_cards = Stimulation.getTempAllCards(temp_my_hand_cards)

    for temp_op_cards in itertools.combinations(total_op_cards,2):

        win = 0
        tid = 0

        total_board_cards = Stimulation.getTempAllCards(temp_my_hand_cards,temp_op_cards)
        for temp_board_cards in itertools.combinations(total_board_cards, 3):
            # my_rank, _ = Rank.rank(temp_my_hand_cards, temp_board_cards)
            # op_rank, _ = Rank.rank(temp_op_cards, temp_board_cards)
            #
            # if my_rank > op_rank:
            #     win += 1
            # elif my_rank == op_rank:
            #     tid += 1

            print(sum)
            sum -= 1

        # score[HS] += (win + tid/2)


print(time.time() - s)

for i in range(-2,22):
    if cnt[i] != 0:
        score[i] = score[i] // cnt[i]

for key in score.keys():
    print(str(key) + "   " + str(score[key]))
