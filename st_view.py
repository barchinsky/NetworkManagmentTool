import sys
from PyQt4 import QtGui, QtCore
from statistic import *
import cx_Oracle


class ComboBoxBasic(QtGui.QWidget):
    """
    An basic example combo box application
    """

    def __init__(self):

        self.obj = Statistic()
        self.text = ''
        # create GUI
        QtGui.QMainWindow.__init__(self)
        self.setWindowTitle('VIEW STATISTIC')
        # Set the window dimensions
        self.resize(250,290)
        
        # vertical layout for widgets
        self.vbox = QtGui.QVBoxLayout()
        self.setLayout(self.vbox)

        # Create a combo box and add it to our layout
        self.combo = QtGui.QComboBox()
        self.vbox.addWidget(self.combo)
        self.combo2 = QtGui.QComboBox()
        self.vbox.addWidget(self.combo2)

        self.combo3 = QtGui.QComboBox()
        self.vbox.addWidget(self.combo3)

        self.combo4 = QtGui.QComboBox()
        self.vbox.addWidget(self.combo4)
        
       

     

        # Or add a sequence in one call
        distrolist = ['BROADBAND','IPTV', 'VOIP']
        self.combo.addItems(distrolist)
        #self.t = self.combo.currentText()
        self.connect(self.combo, QtCore.SIGNAL('activated(QString)'), self.hello)
  
        con = cx_Oracle.connect('orcdb/passw0rd@192.168.111.138/orcl')
        self.cur = con.cursor()
        self.cur.execute("select METRIC_TYPE from METRICS WHERE IDSERVICE='BROADBAND'")
        data = self.cur.fetchall()
        for el in data:
            self.combo2.addItems(el)

        self.connect(self.combo, QtCore.SIGNAL('activated(QString)'), self.hello)
        
        distrolist3 = ['15 min','30 min', '60 min','1 day']
        self.combo3.addItems(distrolist3)

        distrolist4 = ['MAX','AVG', 'MIN']
        self.combo4.addItems(distrolist4)

        quit = QtGui.QPushButton('VIEW STATISTIC', self)
        quit.setGeometry(90, 250, 140, 35)
        self.connect(quit, QtCore.SIGNAL('clicked()'),self.combo_chosen)
        
    def combo_chosen(self):
        self.obj.select_dev(str(self.combo.currentText()),str(self.combo2.currentText()),str(self.combo3.currentText()),str(self.combo4.currentText()))
            
    def hello(self):
        self.t = self.combo.currentText()
        self.combo2.clear()
        if self.t == "IPTV":
            self.cur.execute("select METRIC_TYPE from METRICS WHERE IDSERVICE='IPTV'")
            data = self.cur.fetchall()
            for el in data:
                self.combo2.addItems(el)
        elif self.t == "VOIP":
            self.cur.execute("select METRIC_TYPE from METRICS WHERE IDSERVICE='VOIP'")
            data = self.cur.fetchall()
            for el in data:
               self.combo2.addItems(el)
        elif self.t == "BROADBAND":
            self.cur.execute("select METRIC_TYPE from METRICS WHERE IDSERVICE='BROADBAND'")
            data = self.cur.fetchall()
            for el in data:
               self.combo2.addItems(el)

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    obj = ComboBoxBasic()
    obj.show()
    app.exec_()

