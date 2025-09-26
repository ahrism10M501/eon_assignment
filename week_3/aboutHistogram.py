import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math

# 표준 정규 분포(평균 0, 표준편차 1)의 난수 데이터 생성
data = np.random.randn(100000)
# 정규 분포 데이터 생성(평균 1, 표준편차 3)
data2 = np.random.normal(1, 3, 100000)
# weibull 분포 데이터 생성()
data3 = np.random.weibull(1, 100000)

def showHist(data):
    plt.figure(figsize = (15, 5))
    plt.hist(data, bins=int(math.sqrt(len(data))), color='red')
    plt.xlabel('hist')
    plt.show()
	
 
showHist(data)
showHist(data2)
showHist(data3)