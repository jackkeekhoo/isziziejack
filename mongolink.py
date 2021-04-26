#26April2021
#10.45am

import pymongo

class LivestockDb:
    myclient=''
    mydb=''
    mytable=''
    def connectmongo(self):
        #do a function to connect to your computer mongo DB
        self.myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        self.mydb = self.myclient["project"]
        self.mytable = self.mydb["rfid_livestock"]
        print("connected")
        print(self.myclient.list_database_names())
        return()
    def insertvalue(self,factory_id, serial_number, weight):
        mydict = { "factory id": factory_id, "serial number": serial_number, "weight": weight }
        x = self.mytable.insert_one(mydict)
        return(x)
    
#mongodatabase=LivestockDb()      
#mytable = mongodatabase.connectmongo()
#mongodatabase.insertvalue("11100","2701","410")





