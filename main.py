#!/usr/bin/python
# simple.py

import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import cx_Oracle
import subprocess
from st_view import *
from trap_view import *


sys.path.append("src/")

from LogManager import *

class MyMainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MyMainWindow,self).__init__(parent)
        #self.form_widget = MetricManagmentWidget(self)
        self.form_widget = MainMenuWidget(self)
        self.setCentralWidget(self.form_widget)
        self.setWindowTitle('Metric manager')
        Log("Gui started.")

        self.connect(self.form_widget.close,SIGNAL("clicked()"),self,SLOT("close()"))

class MainMenuWidget(QWidget):
    def __init__(self,parent):
        super(MainMenuWidget,self).__init__(parent)

        self.metric_widget = MetricManagmentWidget()
        self.statistic_widget = ComboBoxBasic()
        self.trap_widget = Trap_statistic()

        self.layout = QGridLayout()

        self.start_service_btn = QPushButton("Start service")
        self.show_device_info_btn = QPushButton("Show device info(no widget yet)")
        self.show_device_traps_btn = QPushButton("Show traps")
        self.show_statistic_btn = QPushButton("Show statistic")
        self.metric_btn = QPushButton("Metric")
        self.close = QPushButton("Exit")

        self.layout.addWidget(self.start_service_btn)
        self.layout.addWidget(self.show_device_info_btn)
        self.layout.addWidget(self.show_device_traps_btn)
        self.layout.addWidget(self.show_statistic_btn)
        self.layout.addWidget(self.metric_btn)
        self.layout.addWidget(self.close)

        self.setLayout(self.layout)

        self.connect(self.metric_btn,SIGNAL("clicked()"),self,SLOT("start_metric_widget()"))
        self.connect(self.show_statistic_btn,SIGNAL("clicked()"),self,SLOT("start_statistic_widget()"))
        self.connect(self.show_device_traps_btn,SIGNAL("clicked()"),self,SLOT("start_trap_widget()"))
        self.connect(self.start_service_btn,SIGNAL("clicked()"),self,SLOT("start_services()"))

    @pyqtSlot()
    def start_metric_widget(self):
        try:
            self.metric_widget.show()
            Log("Metric widget start.")
        except Exception,e:
            Log("Metric widget start failed."+e,1)


    @pyqtSlot()
    def start_statistic_widget(self):
        try:
            self.statistic_widget.show()
            Log("Statistic widget start.")
        except Exception,e:
            Log("Statistic widget start failed."+e,1)

    @pyqtSlot()
    def start_trap_widget(self):
        try:
            self.trap_widget.show()
            Log("Trap widget start.")
        except Exception,e:
            Log("Trap widget start failed."+e,1)


    @pyqtSlot()
    def start_services(self):
        try:
            subprocess.Popen("src/start_services.sh",shell=True)
            Log("Services started.")
            print "Services started succesfull:"
            self.show_info("Services started succesfull.")
            self.start_service_btn.setEnabled(False)
        except Exception,e:
            print "Application close."
            Log("Start services failed."+e,1)
            sys.exit()

    def show_info(self,e):
        msgBox = QMessageBox()
        msgBox.setText(str(e))
        msgBox.setStandardButtons(QMessageBox.Ok)
        ret = msgBox.exec_();

class AddMetricWidget(QWidget):
    def __init__(self,service_type,service_available_metric=""):
        super(AddMetricWidget,self).__init__()

        # connect to database
        try:
            self.con = cx_Oracle.connect('orcdb/passw0rd@192.168.111.138/orcl')
        except Exception,e:
            print e
            Log("Databace connection refused.\n"+str(e),1)
            sys.exit()

        self.cur = self.con.cursor()

        self.layout = QVBoxLayout()
        self._service_type = service_type
        self._service_available_metric = service_available_metric

        self.setWindowTitle("Add metric")
        self.metric_name = QComboBox()
        for metric in self._service_available_metric:
            self.metric_name.addItem(QString(metric))

        self.lab1 = QLabel('Choose metric:')

        self.l_min = QLineEdit()
        self.l_max = QLineEdit()

        self.lab2 = QLabel("Minimum value")
        self.lab3 = QLabel("Maximum value")

        self.add= QPushButton('Add')
        self.cancel = QPushButton('Cancel')


        self.layout.addWidget(self.lab1)
        self.layout.addWidget(self.metric_name)
        self.layout.addWidget(self.lab2)
        self.layout.addWidget(self.l_min)
        self.layout.addWidget(self.lab3)
        self.layout.addWidget(self.l_max)
        self.layout.addWidget(self.add)
        self.layout.addWidget(self.cancel)

        self.setLayout(self.layout)

        self.connect(self.add,SIGNAL("clicked()"),self,SLOT("ok_pressed()"))
        self.connect(self.add,SIGNAL("clicked()"),self,SLOT("close()"))

        self.connect(self.cancel,SIGNAL("clicked()"),self,SLOT("close()"))

        Log("Widget closed.")

    @pyqtSlot()
    def ok_pressed(self):
        #print 'Service', self._service_type,'\nMin',self.l_min.text(),'\nMax',self.l_max.text()
        try:
            arg1 = str(self._service_type)
            arg2 = int(self.l_min.text())
            arg3 = int(self.l_max.text())
            arg4 = str(self.metric_name.currentText())
        
            self.cur.callproc("add_metrics",[arg1,arg4,arg2,arg3])
            Log("Call 'add_metric' procedure.")
            self.con.commit()
            self.show_info("Operation Success.")

        except Exception,e:
            print e
            self.show_info(e)
            Log("Add metric failed.\n"+e,1)

    def validate_name(self):
        pass

    def validate_limits(self):
        pass
    
    def show_info(self,e):
        msgBox = QMessageBox()
        msgBox.setText(str(e))
        msgBox.setStandardButtons(QMessageBox.Ok)
        ret = msgBox.exec_();


class MetricManagmentWidget(QWidget):
    def __init__(self):
        super(MetricManagmentWidget,self).__init__()
        Log("Metric managment widget started.")
        self.iptv_m = []
        self.bb_m = []
        self.voip_m = []

        self.actual_iptv_metric = []
        self.actual_voip_metric = []
        self.actual_bb_metric = []
        
        # connect to database
        try:
            self.con = cx_Oracle.connect('orcdb/passw0rd@192.168.111.138/orcl')
        except Exception,e:
            print e
            Log("Databace connection refused.\n"+str(e),1)
            sys.exit()

        self.cur = self.con.cursor()

        services = ["","IPTV","VOIP","BROADBAND"]

        self.load_metrics()
        
        self.layout = QGridLayout(self)
        self.service_type_combo = QComboBox()
        
        for item in services:
            self.service_type_combo.addItem(item)
        
        self.metric_type_combo = QComboBox()
        self.action_type_combo = QComboBox()

        actions = ["","Remove","Add","View"]

        for action in actions:
            self.action_type_combo.addItem(action)

        self.wid = AddMetricWidget("",[])
        self.statistic_widget = ComboBoxBasic()

        self.l_min = QLineEdit()
        self.l_max = QLineEdit()

        self.layout.addWidget(self.service_type_combo,0,1)
        self.layout.addWidget(QLabel("Service:"),0,0)

        self.layout.addWidget(self.action_type_combo,1,1)
        self.layout.addWidget(QLabel("Action:"),1,0)
        
        self.ok = QPushButton("Ok")
        self.cancel = QPushButton("Cancel")

        self.connect(self.cancel, SIGNAL('clicked()'),qApp,SLOT('quit()'))
        self.connect(self.ok,SIGNAL('clicked()'),self,SLOT('delete_item()'))
        #show add metric widget and disable base widget
        self.connect(self.action_type_combo,SIGNAL("activated(int)"),self,SLOT("addMetric(int)"))
        self.connect(self.action_type_combo,SIGNAL("activated(int)"),self,SLOT("disable(int)"))
        #fill metric combo
        self.connect(self.service_type_combo,SIGNAL("activated(int)"),self,SLOT("fill_metric_combo(int)"))
        self.connect(self.action_type_combo,SIGNAL("activated(int)"),self,SLOT("show_remove_widget(int)"))

    @pyqtSlot(int)
    def show_remove_widget(self,opt):
        if opt == 1: # if remove action choosed add metric combo
            self.load_actual_metrics()

            service = self.service_type_combo.currentText()
            self.metric_type_combo = QComboBox()
            print service

            if service == "IPTV": # fill metric combo with actual params
                for item in self.actual_iptv_metric:
                    self.metric_type_combo.addItem(item)
                    #print item+'============='
                #print self.actual_iptv_metric
            elif service == "VOIP":
                for item in self.actual_voip_metric:
                    self.metric_type_combo.addItem(item)
            else:
                for item in self.actual_bb_metric:
                    self.metric_type_combo.addItem(item)

            self.layout.addWidget(self.metric_type_combo)
            self.layout.addWidget(self.ok)
            
 
    @pyqtSlot(int)
    def fill_metric_combo(self,opt):
        self.action_type_combo.setCurrentIndex(0)
        if opt == 1: # iptv service
            for item in self.iptv_m:
                self.metric_type_combo.addItem(QString(item))
        elif opt == 2: #void service
            for item in self.voip_m:
                self.metric_type_combo.addItem(QString(item))
        elif opt == 3: #bb service
            for item in self.bb_m:
                self.metric_type_combo.addItem(QString(item))

    @pyqtSlot(int)
    def disable(self,opt):
        if opt==2:
            self.setDisabled(True)

    @pyqtSlot()
    def enable(self):
        self.setDisabled(False)

    @pyqtSlot()
    def delete_item(self):
        print "Saved\n"
        m = str(self.metric_type_combo.currentText())
        try:
            self.cur.execute("delete from METRICS where METRIC_TYPE=:m",{"m":m})
            self.con.commit()
            self.show_info("Item deleted succesfull.")
            #self = MetricManagmentWidget()
        except Exception,e:
            self.show_info(e)
            Log(e,1)


    @pyqtSlot(int)
    def addMetric(self,choice):
        services = [None,self.iptv_m,self.voip_m,self.bb_m]
        if choice==2:
            self.wid = AddMetricWidget(self.service_type_combo.currentText(), services[ self.service_type_combo.currentIndex() ] )
            self.wid.show()

            self.connect(self.wid.cancel,SIGNAL("clicked()"),self,SLOT("enable()"))
            self.connect(self.wid.add,SIGNAL("clicked()"),self,SLOT("enable()"))
        if choice==3:
            self.statistic_widget.show()
            print "View option choosed"

    def get_iptv_metrics(self):
        self.cur.execute("select * from IPTV")
        for column_desc in self.cur.description:
            self.iptv_m.append(column_desc[0])
        print "Iptv\n", self.iptv_m

    def get_voip_metrics(self):
        self.cur.execute("select * from VOIP")
        for column_desc in self.cur.description:
            self.voip_m.append(column_desc[0])
        print "Voip", self.voip_m

    def get_bb_metrics(self):
        self.cur.execute("select * from BROADBAND")
        for column_desc in self.cur.description:
            self.bb_m.append(column_desc[0])

    def get_actual_iptv_metric(self):
        self.cur.execute("select * from METRICS where IDSERVICE='IPTV'")
        for metric in self.cur.fetchall():
            self.actual_iptv_metric.append(metric[1])
        print self.actual_iptv_metric

    def get_actual_voip_metric(self):
        self.cur.execute("select * from METRICS where IDSERVICE='VOIP'")
        for metric in self.cur.fetchall():
            self.actual_voip_metric.append(metric[1])
        print self.actual_iptv_metric

    def get_actual_bb_metric(self):
        self.cur.execute("select * from METRICS where IDSERVICE='BROADBAND'")
        for metric in self.cur.fetchall():
            self.actual_bb_metric.append(metric[1])
        print self.actual_iptv_metric
    
    def load_actual_metrics(self):
        self.get_actual_iptv_metric()
        self.get_actual_voip_metric()
        self.get_actual_bb_metric()

    def load_metrics(self):
        self.get_iptv_metrics()
        self.get_bb_metrics()
        self.get_voip_metrics()

    def show_info(self,e):
        msgBox = QMessageBox()
        msgBox.setText(str(e))
        msgBox.setStandardButtons(QMessageBox.Ok)
        ret = msgBox.exec_();




app = QApplication([])
metrics = MyMainWindow()
metrics.show()

sys.exit(app.exec_())
