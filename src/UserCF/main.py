#-*-coding:utf-8-*-

from dataProcess import *
from userCF import *
import random

if __name__ == '__main__' :
    seed = random.randint (0 , 9999999)
    for N in [5 , 10 , 20 , 50 , 100] :
        for K in [3 , 5 , 10 , 20] :
            print 'N = ' , N , '  K = ' , K
            print mainProcess (seed , K , N , 8)
