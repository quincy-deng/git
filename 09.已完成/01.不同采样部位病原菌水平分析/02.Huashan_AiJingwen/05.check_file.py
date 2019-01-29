# import pandas as pd
# import os
# import numpy as np
# import sys

# file_path =r'/hwfssz1/ST_PRECISION/USER/zhuzhongyi/04.CDC_data/05.CDC_20180518/CDC_20180518.total.txt'
# lines = 0
# for lines,line in enumerate(open(file_path)):
#     pass
# print(lines)
data = [
    [1,2],
    [2,3],
    [1,6],
    [1,3],
    [3,7],
    [3,6],
    [3,8],
    [3,7],
    [10,12],
    [110,290],
    [50,60],
    [49,55],
]

def sortsss(a, b):
    if a[0] > b[0]: return 1
    if a[0] < b[0]: return -1
    if a[1] > b[1]: return 1
    if a[1] < b[1]: return -1
    return 1

sortsss(data.sort())
print(data)
exit()
result = [] 

for a, b in data:
    if not result:
        result.append([a, b])
        continue

    la, lb = result[-1]
    if la <= a <= lb and b > lb:
        result[-1][1] = b
    if a > lb:
        result.append([a, b])

# print result