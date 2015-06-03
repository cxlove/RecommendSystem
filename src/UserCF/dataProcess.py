# -*-coding:utf-8-*-
import random

def readData () :
    """
    read the data
    parameters :
        None
    return :
        a list of data , form of [userID , filmID]
    """
    rating = open ('../../data/MoviesLensSmall/u.data').readlines ()
    data = []
    for each in rating :
        each = each.strip ()
        if each : 
            data.append (each.split ('\t')[:-2])
    return data

def splitData (data , seed , M , k) :
    """
    split the data to train data and test data
    parameters :
        data : orgin data in readData
        seed : random seed , same in each dataSet
        M : how many parts to split
        k : witch part is the test data
    return :
        train , test : the data for training and testing 
                       transform it to a dictionary ,means what films they like for each users
    """
    random.seed (seed)
    train = dict ()
    test = dict ()
    for each in data :
        if random.randint (0 , M - 1) == k :
            if each[0] not in test :
                test[each[0]] = []
            test[each[0]].append (each[1])
        else :
            if each[0] not in train :  
                train[each[0]] = []
            train[each[0]].append (each[1])
    return train , test

def dataProcess (seed , M , k) :
    """
    dataProcess
    paraments :
        same as splitData
    return :
        same as splitData
    """
    data = readData ()
    train , test = splitData (data , seed , M , k)
    return train , test

if __name__ == '__main__' :
    dataProcess (321 , 8 , 0)
