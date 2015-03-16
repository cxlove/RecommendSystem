#-*-coding:utf-8-*-
import math
from resultEvaluation import *
from dataProcess import *

def itemSimilarity (data) :
    """
       calculate the similarity between each pair of items
    paraments :
        data : the data for training
    return :
        sim : the matrix of the similarity between each pair of items
    description :
        Jaccard : sim[u][v] = \frac{|N[u] and N[v]|}{|N[u] or N[v]|}
        cos : sim[u][v] = \frac{|N[u] and N[v]|}{sqrt (N[u] * N[v])}
        John S. Breese : sim[u][v] = \frac{\frac{1}{\ln {1+count (the people like i)}}}{sqrt (N[u] * N[v])}  for each i in |N[u] and N[v]|
    """
    # calculate the number of users like each pairs of items
    common = dict ()
    N = dict ()
    for user , items in data.items () :
        for u in items :
            if u not in N :
                N[u] = 0
            N[u] += 1
            if u not in common :
                common[u] = dict ()
            for v in items :
                if u != v :
                    if v not in common[u] :
                        common[u][v] = 0
                    common[u][v] += 1 / math.log (1.0 + len (items))

    # calculate the similarity between two iterms
    sim = dict ()
    for u , items in common.items () :
        if u not in sim :
            sim[u] = dict ()
        for v , val in items.items () :
            sim[u][v] = common[u][v] / math.sqrt (1.0 * N[u] * N[v])

    return sim

def getRecommend (user , train , sim , k , N) :
    """
    recommend N items for user from k people which similar to user according to the training dataSet
    paraments : 
        user : the people need to recommend for
        train : training dataSet
        sim : matrix of similarity
        k : the number of people to choose
    return :

    """
    rank = dict ()
    already = train[user]
    for u in already :
        for v , val in sorted (sim[u].items () , key = lambda p : p[1] , reverse = True)[:k] :
            if v not in already :
                if v not in rank :
                    rank[v] = 0
                # weight means how many like from u to item
                weight = 1
                rank[v] += val * weight

    recommend = sorted (rank.items () , key = lambda p : p[1] , reverse = True)
    return recommend[:min(N , len (recommend))]

def mainProcess (seed , k , N , M) :
    """
    paraments :
        M : the paraments in splitData
    return :
        the analysis of the recommend result
    """

    recall = 0
    precision = 0
    coverage = 0
    popularity = 0
    for part in range (M) :
        train , test = dataProcess (seed , M , part)

        predict = dict ()
        sim = itemSimilarity (train)
        for user , items in test.items () :
            recommend = getRecommend (user , train , sim , k , N)
            predict[user] = recommend

        recall += calRecall (test , predict)
        precision += calPrecision (test , predict)
        coverage += calCoverage (train , test , predict)
        popularity += calPopularity (train , test , predict)


    return {'recall' : recall / M , 'precision' : precision / M , 'coverage' : coverage / M , 'popularity' : popularity / M}


if __name__ == '__main__' :
   pass 

