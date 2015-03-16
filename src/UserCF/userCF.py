#-*-coding:utf-8-*-
import math
from resultEvaluation import *
from dataProcess import *

def userSimilarity (data) :
    """
    calculate the similarity between each pair of users
    paraments :
        data : the data for training
    return :
        sim : the matrix of the similarity between each pair of users 
    description :
        Jaccard : sim[u][v] = \frac{|N[u] and N[v]|}{|N[u] or N[v]|}
        cos : sim[u][v] = \frac{|N[u] and N[v]|}{sqrt (N[u] * N[v])}
        John S. Breese : sim[u][v] = \frac{\frac{1}{\ln {1+count (the people like i)}}}{sqrt (N[u] * N[v])}  for each i in |N[u] and N[v]|
    """
    allUser = set ()
    # build the inverse table between the users and items
    inverseTable = dict ()
    for user , items in data.items () :
        allUser.add (user)
        for item in items :
            if item not in inverseTable :
                inverseTable[item] = set ()
            inverseTable[item].add (user)

    # calculate the weight of items they both like between two users
    N = dict ()
    sim = dict ()
    common = dict ()
    for u in allUser :
        N[u] = 0
        common[u] = dict ()
        sim[u] = dict ()
        for v in allUser :
            if u != v :
                common[u][v] = 0
    for item , users in inverseTable.items () :
        for u in users :
            N[u] += 1
            for v in users :
                if u != v :
                    common[u][v] += 1 / math.log (1 + len (users))
    
    # calculate the similarity between two users
    for u , users in common.items () :
        for v , val in users.items () :
            sim[u][v] = common[u][v] / math.sqrt (N[u] * N[v])

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
    for u , val in sorted (sim[user].items () , key = lambda p : p[1] , reverse = True)[:k] :
        for item in train[u] :
            if item not in already :
                if item not in rank :
                    rank[item] = 0
                # weight means how many like from u to item
                weight = 1
                rank[item] += val * weight

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
        sim = userSimilarity (train)
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

