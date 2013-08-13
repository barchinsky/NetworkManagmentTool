import sys
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QLineEdit
from statistic import *
import cx_Oracle

class Trap_statistic(QtGui.QWidget):

    def __init__(self):
        super(Trap_statistic,self).__init__()
        self.obj = Statistic()
        self.text = ''
        # create GUI
        #QtGui.QMainWindow.__init__(self)
        #self.setWindowTitle('VIEW STATISTIC')
        # Set the window dimensions
        #self.resize(250,290)]
        self.setFixedSize(350,90)

        
        # vertical layout for widgets
        self.vbox = QtGui.QGridLayout()
        self.setLayout(self.vbox)

        # Create a combo box and add it to our layout
        self.combo = QtGui.QComboBox()
        self.vbox.addWidget(self.combo,1,0)
        con = cx_Oracle.connect('orcdb/passw0rd@192.168.111.138/orcl')
        self.cur = con.cursor()
        self.cur.execute("select ID from DEVICE")
        data = self.cur.fetchall()
        for el in data:
            self.combo.addItems(el)
        self.combo2 = QtGui.QComboBox()
        self.vbox.addWidget(self.combo2,2,0)

        #self.le = QLineEdit(self)
        #self.le.setGeometry(1,200,75,35)
        #self.vbox.addWidget(self.le,4,0)
        self.select_trap()

        self.connect(self.combo, QtCore.SIGNAL('activated(QString)'),self.select_trap)


    def select_trap(self):
        trap = {'lowVolatage','fanStatus Fail','temp Hight','linkDown','shutDown','coldStart','hardReset','CRC Frame','DDoS detected','hard Reset','fanFail'}
        
        Id = str(self.combo.currentText())
        print Id
        self.cur.execute("select TRAP,TIMESTAMP from TRAP WHERE IDDEVICE=:Id",{'Id':Id})
        data = self.cur.fetchall()
        #print data
        #self.cur.execute("select TIMESTAMP from TRAP WHERE IDDEVICE=:Id",{'Id':Id})
        #tmp = self.cur.fetchall()
        self.combo2.clear()
        if data == []:
            print 'No such device in DB'
        else:
            print 'Errors: '
            for row in data :
                print row[0]
                if row[0] in trap:
                    #print row[1]

                    self.combo2.addItem(str(row[0])+" -- "+time.ctime(row[1]))
                    #tmp.append(row[0])
        '''print tmp
        for el in tmp:
            #i=str(row[0])
            self.combo2.addItems(str(el)+"\n")
            #i = '''

'''---------------- debug zone -----------------------'''

#if __name__ == "__main__":
#    app = QtGui.QApplication(sys.argv)
#    obj = Trap_statistic()
#    obj.show()
#    app.exec_()

