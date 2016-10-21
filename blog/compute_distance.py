# -*-coding:utf-8-*-
from numpy import *  # 导入numpy的库函数
import numpy as np
def cos_distance( v1, v2):
    # 计算余弦距离
    a1 = np.array(v1, dtype=int)
    a2 = np.array(v2, dtype=int)
    a3 = multiply(a1, a2)
    return sum(a3) * 1.0 / (sqrt(sum(a1)) + sqrt(sum(a2)))