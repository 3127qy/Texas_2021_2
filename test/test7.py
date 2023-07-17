import time

a = time.time()





while 1:
    time.sleep(0.001)
    b = time.time()
    if(int(b - a) == 1):
        print(1)
        a = b



print(b-a)