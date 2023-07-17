import random
import re
from basic import Basic
#
# boardCards = "<2,11>"
# count = 0
#
# print(re.split("[,>]",boardCards)[1])
#
#
# print(508 < 420.5)

# bet =

# if 500 < Basic.betLine(0,50,0.5):
#     print(500)


# message = "earnChips 201oppo_hands|<2,11><1,9>preflop|BIGBLIND|<1,0><1,5>"
# message = "earnChips 201preflop|BIGBLIND|<1,0><1,5>"
# message = "earnChips 201"
message = "preflop|BIGBLIND|<1,0><1,5>"

# print(eval(message[:message.index("oppo_hands")]))

# if "oppo_hands" in message and "preflop" in message:
#     phase = "preflop"
#     message = message.split("preflop")[1:]
#
#
# print(message)

def checkFinish(message):

    elements = re.split("[ ]",message)

    if elements[0] == "earnChips" and "oppo_hands" not in elements[1] and "preflop" not in elements[1]:

        winChips = eval(elements[1])
        print("1  " + str(winChips))
        return True,winChips

    elif elements[0] == "earnChips":

        winChips = 0
        if "oppo_hands"  in elements[1]:
            winChips = eval(elements[1][:elements[1].index("oppo_hands")])
        elif "preflop"  in elements[1]:
            winChips = eval(elements[1][:elements[1].index("preflop")])
        print("2  " + str(winChips))
        return True,winChips
    else:

        print(3)
        return False,0

checkFinish(message)