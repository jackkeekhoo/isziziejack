#26April2021
#10.36am

import sys
from PyQt5.Qt import *
#iszizie find icon and add icon , https://zetcode.com/gui/pyqt5/firstprograms/

import sys
from PyQt5.QtWidgets import QWidget, QDesktopWidget, QApplication
#from PyQt5.QtCore import Qt, QBasicTimer, pyqtSignal
from PyQt5 import QtCore, QtGui, QtNetwork


from mongolink import *
from comport_class_sensor import *
#import requests


class livestock_data_desktop(QWidget):
    wyuanrfid_latestid="1100EE00E20043B0CB852489ECCA5CB8FBEF"
    wyuanrfid_array=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
    snowscale_latestweight=400
    snowscale_array = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
    global wyuanrfid
    global snowscale
    
    def __init__(self):
        super().__init__()        
        self.initUI()
        wyuanrfid=SensorRFID()
        snowscale=SensorWeight()
        wyuanrfid.serialport=serial.Serial('COM3',57600)
        snowscale.serialport=serial.Serial('COM5',9600)
        self.mongodatabase=LivestockDb
    
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
        self.wyuanrfid_latestid=self.wyuanrfid_latestid+"spam"
        self.rightarrayEdit.setText(str(self.wyuanrfid_latestid))
        
        finalweight=0
        finalfactoryid=0
        finalserialid=0
        while mainloop==1:
            snowscale.loop()
            wyuanrfid.clearbuffer()
            if snowscale.returnvalue is not None:
                if int(snowscale.returnvalue) >0:
                    snowscale.millislastread=snowscale.current_milli_time()
                    wyuanrfid.loop()
                    if wyuanrfid.returnvalue !='':
                        finalweight=snowscale.countmode()
                        finalfactoryid=wyuanrfid.returnvalue_factory
                        finalserialid=wyuanrfid.returnvalue_serial
                        #record to 2d array
            if snowscale.millislastread != 0:
                if int(snowscale.current_milli_time())-int(snowscale.millislastread) >3000:
                    #print("weight now is " +str(finalweight) + " and rfid factory is "+str(finalfactoryid)+",card serial ="+str(finalserialid))
                    self.wyuanrfid_latestid=self.wyuanrfid_latestid+"weight now is " +str(finalweight) + " and rfid factory is "+str(finalfactoryid)+",card serial ="+str(finalserialid)
                    self.rightarrayEdit.setText(str(self.wyuanrfid_latestid))
                    snowscale.millislastread=0
                    finalweight=0
                    finalfactoryid=0
                    finalserialid=0

                    
    def mystarttimer(self):
        self.time_id = self.startTimer(200)
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
