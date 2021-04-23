#23April2021
#4.43PM

import pymongo

class LivestockDb:
    myclient=''
    mydb=''
    mytable=''
    def connectmongo(self):
        #do a function to connect to your computer mongo DB
        self.myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        self.mydb = myclient["project"]
        self.mytable = mydb["rfid_livestock"]
        print("connected")
        print(myclient.list_database_names())
        return()
    def insertvalue(self):
        mydict = { "factory id": "1100", "serial number": "2626", "weight":"400" }
        x = self.mytable.insert_one(mydict)
        return(x)
    
mytable = connectmongo()
insertvalue(mytable)

#iszizie, the insertvalue need to accept 3 parameter,
#def insertvalue(self,weight,tagID)
#and insrt the value to the table
