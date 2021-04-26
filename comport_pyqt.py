#26April2021
#12.47pm

import sys
from PyQt5.Qt import *
#iszizie find icon and add icon , https://zetcode.com/gui/pyqt5/firstprograms/

import sys
from PyQt5.QtWidgets import QWidget, QDesktopWidget, QApplication
#from PyQt5.QtCore import Qt, QBasicTimer, pyqtSignal
from PyQt5 import QtCore, QtGui, QtNetwork


from mongolink import *
from comport_class_sensor import *
import requests


class livestock_data_desktop(QWidget):
    wyuanrfid_latestid=""
    wyuanrfid_array=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
    snowscale_latestweight=400
    snowscale_array = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
    #global wyuanrfid
    #global snowscale
    
    def __init__(self):
        super().__init__()        
        self.initUI()
        self.wyuanrfid=SensorRFID()
        self.snowscale=SensorWeight()
        self.wyuanrfid.serialport=serial.Serial('COM3',57600)
        self.snowscale.serialport=serial.Serial('COM5',9600)
        self.mongodatabase=LivestockDb()
        self.finalweight=0
        self.finalfactoryid=0
        self.finalserialid=0
    
    def initUI(self):
        rightlabel=QLabel("Weighting Scale",self)
        rightresult=QLabel(str(self.snowscale_latestweight),self)
        rightarray=QLabel("previous 20")
        self.rightarrayEdit = QTextEdit()
        
        leftlabel=QLabel("RFID Reader",self)
        leftresult=QLabel(self.wyuanrfid_latestid,self)
        leftarray=QLabel("previous 20")
        self.leftarrayEdit = QTextEdit()

        grid = QGridLayout()
        grid.setSpacing(10)
        grid.addWidget(rightlabel, 1, 1)#iszizit please change all these widget position
        grid.addWidget(rightresult, 2, 1)
        grid.addWidget(rightarray, 3, 1)
        grid.addWidget(self.rightarrayEdit, 4, 1, 5, 1)
        grid.addWidget(leftlabel, 1, 0)
        grid.addWidget(leftresult, 2, 0)
        grid.addWidget(leftarray, 3, 0)
        grid.addWidget(self.leftarrayEdit, 4, 0, 5, 1)

        self.setLayout(grid)
        
        self.resize(650, 550)
        self.center()

        self.setWindowTitle('RFID Livestock')
        self.show()
        self.mystarttimer()

    def center(self):

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def sensorloop(self):
        #finalweight=0
        #finalfactoryid=0
        #finalserialid=0
        #while mainloop==1:
        self.snowscale.loop()
        #self.time_id=0
        #self.time_id = self.startTimer(200)
        try :
            self.wyuanrfid.clearbuffer()
        except:
            k=0
        if self.snowscale.returnvalue is not None:
            if int(self.snowscale.returnvalue) >0:
                self.snowscale.millislastread=self.snowscale.current_milli_time()
                self.wyuanrfid.loop()
                if self.wyuanrfid.returnvalue !='':
                    self.finalweight=self.snowscale.countmode()
                    self.finalfactoryid=self.wyuanrfid.returnvalue_factory
                    self.finalserialid=self.wyuanrfid.returnvalue_serial
                    #record to 2d array
                    
        if self.snowscale.millislastread != 0:
            if int(self.snowscale.current_milli_time())-int(self.snowscale.millislastread) >3000:
                self.mongodatabase.insertvalue(str(self.finalfactoryid),str(self.finalserialid),str(self.finalweight))
                #print("weight now is " +str(finalweight) + " and rfid factory is "+str(finalfactoryid)+",card serial ="+str(finalserialid))
                requests.get("https://sf.redtone.com:2288/serverdata/central.php?thismodelname=rfid_livestock&thisdevicename=rfid_livestock&macaddress=isziziejack&weight="+str(self.finalweight)+"&factory="+str(self.finalfactoryid)+"&card="+str(self.finalserialid))
                self.wyuanrfid_latestid=self.wyuanrfid_latestid+"\nweight now is " +str(self.finalweight) + " and rfid factory is "+str(self.finalfactoryid)+",card serial ="+str(self.finalserialid)
                self.rightarrayEdit.setText(str(self.wyuanrfid_latestid))
                self.snowscale.millislastread=0
                self.finalweight=0
                self.finalfactoryid=0
                self.finalserialid=0

                    
    def mystarttimer(self):
        self.time_id = self.startTimer(300)
    def timerEvent(self, QTimerEvent):
        self.sensorloop()
        
def main():
    app = QApplication(sys.argv)
    ex = livestock_data_desktop()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()


#now = QDate.currentDate()
#print(now.toString(Qt.ISODate))
#print(now.toString(Qt.DefaultLocaleLongDate))
#datetime = QDateTime.currentDateTime()
#print(datetime.toString())
#time = QTime.currentTime()
#print(time.toString(Qt.DefaultLocaleLongDate))
