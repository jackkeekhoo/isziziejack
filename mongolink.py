#27April2021
#11.21am

import pymongo
import csv
import sys
import datetime

print ("ttttttttttttttttttttttttttttt")
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
        print("connected to db")
        #print(self.myclient.list_database_names())
        return()
    def insertvalue(self,factory_id, serial_number, weight, gate_id):
        self.connectmongo()
        mydict = { "factory id": factory_id, "serial number": serial_number, "weight": weight , "gate id": gate_id}
        x = self.mytable.insert_one(mydict)
        return(x)
    
    def exportdata(newfilename,newlist):        
        import pandas as pd
        #newlist = self.mytable.find()
        df = pd.DataFrame(newlist, columns= self.tablefieldname)
        df.to_csv (r'C:\Users\iszizie.idzham\Desktop\python files\\'+newfilename+'.csv', index = False, header=True)
                   
    def search_cow_by_factory_serial(self,factory_id,serial_number):
        self.connectmongo()
        #myquery={"factory id": "1100ee00e20043b0cc8587" ,"serial number": "09eccd21b0ee35"}
        myquery={"factory id": factory_id, "serial number": serial_number}
        mydoc=mongodatabase.mytable.find(myquery).limit(1)
        for x in mydoc:
          print(x)
        #myquery={"factory id": factory_id, "serial number": serial_number}
        #return(mongodatabase.mytable.find(myquery))
    def search_cow_by_weight(self,minimum_weight,maximum_weight):
    
        #iszizie, don't let it count same cow twice
    
        myquery={"weight":{ "$gt" : minimum_weight, "$lt" : maximum_weight}}
        mydoc=mongodatabase.mytable.find(myquery)
        for x in mydoc:
          print(x)
    #### total difference number of cow that pass by gate id 
    def list_all_cow_in_grassarea3(gateid_in,gateid_out)
        mydoc = mongodatabase.mytable.distinct("serial number",{"gate id":gateid_in})

        for x in mydoc:
          print(x)
        totalx = len(mydoc)
        
        mydoc = mongodatabase.mytable.distinct("serial number",{"gate id":gateid_out})

        for x in mydoc:
          print(x)
        totaly = len(mydoc)
        print("Total cow at the grassarea3=",(totalx-totaly))
        


    def convert_list_to_htmltable(longlist):
        #### to print list/array  to html table format
        longstring="<tr>"
        for x in longlist:
            for key, value in x.items():
                longstring=longstring+"<td>"+ str(x[key])+"</td>"
        longstring=longstring+"</tr>"
        #print(longstring)
        return(longstring)


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




###### table for cow nicknames and remarks
##mongodatabase=LivestockDb()      
##mongodatabase.connectmongo()
##factory_id = "1100"
##serial_number = "2938"
##cow_nickname= "cow1"
##cow_remarks= "muscular, just vaccinated"
##
##mydict = { "factory id": factory_id, "serial number": serial_number, "cow nickname": cow_nickname, "cow remarks":cow_remarks}
##x = mongodatabase.mytablecow.insert_one(mydict)
##
##
##
###### table for gate id and location remarks
##mongodatabase=LivestockDb()      
##mongodatabase.connectmongo()
##gate_id=9
##location_remarks= "pantry sofa"
##mydict = { "gate id": gate_id, "location remarks":location_remarks}
##x = mongodatabase.mytablelocation.insert_one(mydict)




  

    
    



