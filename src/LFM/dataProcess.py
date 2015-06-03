#-*-coding:utf-8-*-
import random 

class DataSet () :
    """

    """
    def __init__ (self , seed , M , k) :
        """
        paraments :
            seed : random seed
            M : how many parts the data split
            k : the part whitch choose for testing
        return :
            itemAll : for training data , the list of all item (no discrete)
            train : training data (userID , itemID)
            test : testing data
            userList : for training data , the list of all userID (discrete)
            itemList : for training data , the list of all itemID (discrete)
        """
        self.itemAll = []
        self.train = dict ()
        self.test = dict ()
        self.userList = set ()
        self.itemList = set ()
        self.readData (seed , M , k)

    def readData (self , seed , M , k) :
        """
        prepare the data
        """
        random.seed (seed)
        data = open ('../../data/MoviesLensSmall/u.data').readlines ()
        cnt = 0
        for each in data :
            each = each.split ('\t')[:2]
            cnt += 1
            if random.randint (0 , M - 1) == k :
                if each[0] not in self.test :
                    self.test[each[0]] = []
                self.test[each[0]].append (each[1])
            else :
                if each[0] not in self.train :
                    self.train[each[0]] = []
                self.train[each[0]].append (each[1])
                self.itemAll.append (each[1])
                self.itemList.add (each[1])
                self.userList.add (each[0])

        self.itemList = list (self.itemList)
        self.userList = list (self.userList)
        
    def randomSelectNegativeSample (self , user , ratio) :
        """
        for the training data , it just have the list of what items the user like
        in LFA , we need some negative sample , just like what the user don't like
        we choose some popularity items random that the user have no action in it
        the number of negative sample : the number of positive sample = ratio 
        paraments :
            
        return :
            data : the dictionary of the data , 
        """
        itemAlready = self.train[user]
        data = dict ()
        for item in itemAlready :
            data[item] = 1.0

        countItem = len (self.itemAll)
        countNegative = 0
        countPositive = len (itemAlready)
        while countNegative < countPositive * ratio :
            item = self.itemAll[random.randint (0 , countItem - 1)]
            if item in data :
                continue
            data[item] = 0.0
            countNegative += 1

        return data



