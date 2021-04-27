#27April2021
#11.21am

import pymongo
import csv
import sys
import datetime

class LivestockDb:
    myclient=''
    mydb=''
    mytable=''
    def connectmongo(self):
        #do a function to connect to your computer mongo DB
        self.myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        self.mydb = self.myclient["project"]
        self.mytable = self.mydb["rfid_livestock"]
        self.tablefieldname=['_id', 'factory id', 'serial number', 'weight','gate id']
        print("connected")
        #print(self.myclient.list_database_names())
        return()
    def insertvalue(self,factory_id, serial_number, weight, gate_id):
        self.connectmongo()
        mydict = { "factory id": factory_id, "serial number": serial_number, "weight": weight , "gate id": gate_id}
        x = self.mytable.insert_one(mydict)
        return(x)
    def exportdata():
        
        ###Todo : need to change the file name , user set
        
        import pandas as pd
        mydoc = self.mytable.find()
        df = pd.DataFrame(mydoc, columns= self.tablefieldname)
        df.to_csv (r'C:\Users\iszizie.idzham\Desktop\python files\rfid.csv', index = False, header=True)
    def search_cow_by_factory_serial(self,factory_id,serial_number):
        self.connectmongo()
        #myquery={"factory id": "1100ee00e20043b0cc8587" ,"serial number": "09eccd21b0ee35"}
        myquery={"factory id": factory_id, "serial number": serial_number}
        mydoc=mongodatabase.mytable.find(myquery).limit(1)
        for x in mydoc:
          print(x)
        #myquery={"factory id": factory_id, "serial number": serial_number}
        #return(mongodatabase.mytable.find(myquery))
    def search_cow_by_weight(self,minimum_weight,maximum_weight)
    
        #iszizie, don't let it count same cow twice
    
        myquery={"weight":{ "$gt" : minimum_weight, "$lt" : maximum_weight}}
        mydoc=mongodatabase.mytable.find(myquery)
        for x in mydoc:
          print(x)
        

    #mongodatabase=LivestockDb()      
    #mongodatabase.connectmongo()
#print(ObjectId("60863591655e02a510c4966d").getTimestamp())
    #mongodatabase.mytable.insert({ 'created_on' : new Date() })

    #d = datetime.datetime.strptime("2017-10-13T10:53:53.000Z", "%Y-%m-%dT%H:%M:%S.000Z")

    #with MongoClient() as mongo:
        #db = mongo.get_database("test")
        #db['dates'].insert({"date" : d})

#testing
dfgfghghjghhjg=0
if dfgfghghjghhjg==1:    
    mongodatabase=LivestockDb()      
    mongodatabase.connectmongo()
    
    #mongodatabase.search_cow_by_factory_serial("1100ee00e20043b0cbc37b","89eccb561412c5")

    #mydict = { "factory id": "78", "serial number": "789", "weight": 65 , "gate id": 43,"dtime": new Timestamp()}
    #x = self.mytable.insert_one(mydict)
    #mongodatabase.insertvalue("11100","2701",410,15,"dtime": new Timestamp())



        

#### find cow by gate ID
findcowbygate=0
if findcowbygate==1:
    myquery={"gate id": "15"}
    mydoc=mongodatabase.mytable.find(myquery)
    for x in mydoc:
      print(x)


  

    
    



