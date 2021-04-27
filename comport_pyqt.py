#27April2021
#10.33am

import sys
from PyQt5.Qt import *
#iszizie find icon and add icon , https://zetcode.com/gui/pyqt5/firstprograms/

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtNetwork
from PyQt5.QtGui import QIcon
#import qrc_resources

import datetime as dt


from mongolink import *
from comport_class_sensor import *
import requests





class livestock_data_desktop(QWidget):
    wyuanrfid_latestid=""
    displaywindow_body=""
    wyuanrfid_array=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
    snowscale_latestweight=400
    snowscale_array = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
    #global wyuanrfid
    #global snowscale
    device_id=1
    
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
        self.displaywindow = QTextEdit()
        
        grid = QGridLayout()
        grid.setSpacing(10)
        grid.addWidget(rightlabel, 1, 1)#iszizit please change all these widget position
        grid.addWidget(rightresult, 2, 1)
        grid.addWidget(rightarray, 3, 1)
        grid.addWidget(self.displaywindow, 4, 1, 5, 1)
        
        self.btn_checklivereading = QPushButton("Check Live Reading")
        self.btn_checklivereading.clicked.connect(self.btn_checklivereading_clicked)
        grid.addWidget(self.btn_checklivereading,1,0)
        self.btn_grassarea1 = QPushButton("Grass area 1")
        self.btn_grassarea1.clicked.connect(self.btn_grassarea1_clicked)
        grid.addWidget(self.btn_grassarea1,2,0)
        self.btn_grassarea2 = QPushButton("Grass area 2")
        self.btn_grassarea2.clicked.connect(self.btn_grassarea2_clicked)
        grid.addWidget(self.btn_grassarea2,3,0)
        self.btn_grassarea3 = QPushButton("Grass area 3")
        self.btn_grassarea3.clicked.connect(self.btn_grassarea3_clicked)
        grid.addWidget(self.btn_grassarea3,4,0)

        self.menubar = QMenuBar()
        grid.addWidget(self.menubar,0,0)
        self.actionFile = self.menubar.addMenu("File")
        self.actionFile.addAction("New")
        self.actionFile.addAction("Open")
        self.actionFile.addAction("Save")
        self.actionFile.addSeparator()
        self.actionFile.addAction("Quit")
        self.menubar.addMenu("Edit")
        self.menubar.addMenu("View")
        self.menubar.addMenu("Help")
        
        
        
        self.setLayout(grid)
        self.resize(750, 650)
        self.center()

        self.setWindowTitle('RFID Livestock')
        self.setWindowIcon(QtGui.QIcon('cow.png'))
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
                print(self.snowscale.countmode())
                self.snowscale.millislastread=self.snowscale.current_milli_time()
                self.wyuanrfid.loop()
                if self.wyuanrfid.returnvalue !='':
                    self.finalweight=self.snowscale.countmode()
                    self.finalfactoryid=self.wyuanrfid.returnvalue_factory
                    self.finalserialid=self.wyuanrfid.returnvalue_serial
                    self.device_id=dt.datetime.now().hour
                    self.dt=dt.datetime.now
                    #record to 2d array
                    
        if self.snowscale.millislastread != 0:
            if int(self.snowscale.current_milli_time())-int(self.snowscale.millislastread) >3000:
                self.mongodatabase.insertvalue(str(self.finalfactoryid),str(self.finalserialid),self.finalweight,self.device_id,self.dt)
                #print("weight now is " +str(finalweight) + " and rfid factory is "+str(finalfactoryid)+",card serial ="+str(finalserialid))
                requests.get("https://sf.redtone.com:2288/serverdata/central.php?thismodelname=rfid_livestock&thisdevicename=rfid_livestock&macaddress=isziziejack&weight="+str(self.finalweight)+"&factory="+str(self.finalfactoryid)+"&card="+str(self.finalserialid)+"&device_id="+str(self.device_id)+"&dt="+str(self.dt))
                #self.wyuanrfid_latestid=self.wyuanrfid_latestid+"\nweight now is " +str(self.finalweight) + " and rfid factory is "+str(self.finalfactoryid)+",card serial ="+str(self.finalserialid+",device_id="+str(self.device_id))
                self.displaywindow_body="<tr><td>" +str(self.finalweight) + " </td><td>"+str(self.finalfactoryid)+"</td><td>"+str(self.finalserialid+",device_id="+str(self.device_id)+"</td><td>"+str(self.dt)+"</td></tr>"+self.wyuanrfid_latestid)
                self.displaywindow.setHtml("<table border=2><tr><td>weight</td><td>factory ID</td><td>serial num</td><td>datetime</td>"+self.displaywindow_body+"<table>")
                self.snowscale.millislastread=0
                self.finalweight=0
                self.finalfactoryid=0
                self.finalserialid=0

    def btn_checklivereading_clicked(self):
        #self.textEdit.setPlainText("Hello PyQt5!\nfrom pythonpyqt.com")
        #self.wyuanrfid_latestid=self.wyuanrfid_latestid+"<tr><td>" +str(self.finalweight) + " </td><td>"+str(self.finalfactoryid)+"</td><td>"+str(self.finalserialid+",device_id="+str(self.device_id)+"</td></tr>")
        self.displaywindow.setHtml("Hello PyQt5!\nfrom pythonpyqt.com")
    def btn_grassarea1_clicked(self):
        #self.textEdit.setPlainText("Hello PyQt5!\nfrom pythonpyqt.com")
        #self.wyuanrfid_latestid=self.wyuanrfid_latestid+"<tr><td>" +str(self.finalweight) + " </td><td>"+str(self.finalfactoryid)+"</td><td>"+str(self.finalserialid+",device_id="+str(self.device_id)+"</td></tr>")
        self.displaywindow.setHtml("Hello PyQt5!\nfrom pythonpyqt.com")
    def btn_grassarea2_clicked(self):
        #self.textEdit.setPlainText("Hello PyQt5!\nfrom pythonpyqt.com")
        #self.wyuanrfid_latestid=self.wyuanrfid_latestid+"<tr><td>" +str(self.finalweight) + " </td><td>"+str(self.finalfactoryid)+"</td><td>"+str(self.finalserialid+",device_id="+str(self.device_id)+"</td></tr>")
        self.displaywindow.setHtml("Hello PyQt5!\nfrom pythonpyqt.com")
    def btn_grassarea3_clicked(self):
        #self.textEdit.setPlainText("Hello PyQt5!\nfrom pythonpyqt.com")
        #self.wyuanrfid_latestid=self.wyuanrfid_latestid+"<tr><td>" +str(self.finalweight) + " </td><td>"+str(self.finalfactoryid)+"</td><td>"+str(self.finalserialid+",device_id="+str(self.device_id)+"</td></tr>")
        self.displaywindow.setHtml("Hello PyQt5!\nfrom pythonpyqt.com")
        
                    
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
