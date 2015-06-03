#-*-coding:utf-8-*_

import time
import math
import random
from dataProcess import *
from resultEvaluation import *

def initModel (dataSet , countFeature) :
    """
    """
    P = dict ()
    Q = dict ()
    for each in dataSet.userList :
        P[each] = [0.0] * countFeature
        for i in range (countFeature) :
            P[each][i] = random.random () / countFeature 
    for each in dataSet.itemList :
        Q[each] = [0.0] * countFeature
        for i in range (countFeature) :
            Q[each][i] = random.random () / countFeature
    return P , Q

def getPredict (P , Q , user , item , countFeature) :
    """
    predict = \sum\limits_{k\in Feature}P(user , k) * Q(item , k)
    """
    predict = 0.0
    for feature in range (countFeature) :
        predict += P[user][feature] * Q[item][feature]
    #if predict < 0.0 : return 0.0
    #if predict > 1.0 : return 1.0
    return predict

def latentFactorModel (dataSet , countFeature , countIterative , alpha , beta , ratio) :
    """
    P(user , k) : the relationship between the user and the feature k
    Q(item , k) : the relationship between the item and the feature k
    optimize the paraments by stochasitc gradient descent
    L = \sum{(r_truth - r_predict)^2} + \beta * ||P|| ^ 2 + \beta * ||Q|| ^ 2
    for sgd :
        p(user , k) -= \alpha * (-2 * (r_truth - r_predict) * q(item , k) + 2 * \beta * p(user , k))
        q(item , k) -= \alpha * (-2 * (r_truth - r_predict) * p(user , k) + 2 * \beta * q(item , k))
    """
    P , Q = initModel (dataSet , countFeature)
    for step in range (countIterative) :
        error = 0
        count = 0
        for user in dataSet.userList :
            data = dataSet.randomSelectNegativeSample (user , ratio)
            for item , rui in data.items () :
                predict = getPredict (P , Q , user , item , countFeature)
                eui = rui - predict
                error += eui ** 2
                count += 1
                for feature in range (countFeature) :
                    #tmp_p = P[user][feature]
                    P[user][feature] -= alpha * (-2 * Q[item][feature] * (rui - predict) + 2 * beta * P[user][feature])
                    Q[item][feature] -= alpha * (-2 * P[user][feature] * (rui - predict) + 2 * beta * Q[item][feature])
        alpha *= 0.9
        # print 'step : ' , step
        # print 'error : ' , error / count
    return P , Q

def getRecommend (user , dataSet , P , Q , countFeature , N) :
    """
    for each user in testing data , recommend some items
    paraments :
        N : how many items need to recommend
    return :
        the list of items recommend , (item , score)
    """
    rank = []
    for item in dataSet.itemList : 
        if item not in dataSet.train[user] :
            rank.append ([item , getPredict (P , Q , user , item , countFeature)])
    return sorted (rank , key = lambda a : a[1] , reverse = True)[:N]

def mainProcess (ratio , alpha , beta , countFeature , M) :
    """
    calculate the average result of the LFM
    """
    recall , precision , popularity , coverage = 0 , 0 , 0 , 0
    countIterative = 50 
    N = 20
    seed = 321
    for part in range (M) :
        predict = {}
        dataSet = DataSet (seed , M , part)
        P , Q = latentFactorModel (dataSet , countFeature , countIterative , alpha , beta , ratio)
        for user , items in dataSet.test.items () :
            recommend = getRecommend (user , dataSet , P , Q , countFeature , N)
            predict[user] = recommend
        
        recall += calRecall (dataSet.test , predict)
        precision += calPrecision (dataSet.test , predict)
        coverage += calCoverage (dataSet.train , dataSet.test , predict)
        popularity += calPopularity (dataSet.train , dataSet.test , predict)

    return {'recall' : recall / M , 'precision' : precision / M , 'coverage' : coverage / M , 'popularity' : popularity / M}
        
    
    


