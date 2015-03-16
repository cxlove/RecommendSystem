#-*-coding:utf-8-*-
import math

def calRecall (test , predict) :
    """
    calculate the percent of recall
    paraments :
        test : testing dataSet
        predict : for each user in test , the item that system recommend
    return :
        recall
    description :
        recall = |set (recommend) & set (truth)| / |set (truth)| 
    """
    recall = 0.0
    all = 0.0
    for user , items in test.items () :
        maybe = predict[user]
        for item , val in maybe :
            if item in items :
                recall += 1
        all += len (items)
    return recall / all

def calPrecision (test , predict) :
    """
    calculate the percent of precision
    description :
        precision = |set (recommend) & set (truth)| / |set (recommend)|
    """
    precision = 0.0
    all = 0.0
    for user , items in test.items () :
        maybe = predict[user]
        for item , val in maybe :
            if item in items :
                precision += 1
        all += len (maybe)
    return precision / all

def calCoverage (train , test , predict) :
    """
    calculate the percent of coverage all of the items
    description :
        coverage = |set (recommend)| / |set (all of the items)|
    """
    itemAll = set ()
    for user , items in train.items () :
        for item in items :
            itemAll.add (item)
    itemRecommend = set ()
    for user , items in predict.items () :
        for item , val in items :
            itemRecommend.add (item)

    return len (itemRecommend) * 1.0 / len (itemAll)

def calPopularity (train , test , predict) :
    """
    calculate the popularity of items have been choosed
    """
    itemPopularity = dict ()
    for user , items in train.items () :
        for item in items :
            if item not in itemPopularity :
                itemPopularity[item] = 0
            itemPopularity[item] += 1

    cnt = 0
    popularity = 0
    for user , items in predict.items () :
        for item , val in items : 
            cnt += 1.0
            popularity += math.log (1 + itemPopularity[item])
    return popularity / cnt
