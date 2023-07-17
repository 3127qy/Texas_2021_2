# -*- coding: utf-8 -*-
import time
from multiprocessing.dummy import Pool as ThreadPool
def process(item):
  print('正在并行for循环')
  t= item[1]
  print(t)
  item = item[0]
  print(item)

  time.sleep(5)
items = [['apple', 'bananan', 'cake', 'dumpling'],['app', 'banan', 'ce', 'duling']]
pool = ThreadPool()
pool.map(process, items)
pool.close()
pool.join()