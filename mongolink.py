#26April2021
#3.54pm

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
    def insertvalue(self,factory_id, serial_number, weight, gate_id):
        self.connectmongo()
        mydict = { "factory id": factory_id, "serial number": serial_number, "weight": weight , "gate id": gate_id}
        x = self.mytable.insert_one(mydict)
        return(x)
    def exportdata():
        x=5
    def search_cow_by_factory_serial(self,factory_id,serial_number):
        self.connectmongo()
        #iszizie, change this->myquery={"serial number": "89eccb561412c5"}
        return(mongodatabase.mytable.find(myquery))
        
        

#testing
dfgfghghjghhjg=0
if dfgfghghjghhjg==1:    
    mongodatabase=LivestockDb()      
    mytable = mongodatabase.connectmongo()
    mongodatabase.insertvalue("11100","2701",410,15)
    #myquery={"weight":{ "$gt" : 73000}}
    myquery={"serial number": "89eccb561412c5"}
    #db.inventory.find( { qty: { $gt: 20 } } )
    mydoc = mongodatabase.mytable.find(myquery)

    for x in mydoc:
      print(x)
#export data to csv file,




