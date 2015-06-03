#-*-coding:utf-8-*-

from dataProcess import *
from LatentFactorModel import *

if __name__ == '__main__' :
    countFeature = 100
    alpha = 0.02
    beta = 0.01
    M = 8
    for ratio in [1 , 2 , 3 , 5 , 10 , 20] :
        print 'ratio = ' , ratio , 'result = ' ,  mainProcess (ratio , alpha , beta , countFeature , M)

