import sys
import time
from PyQt4.QtGui import *
from PyQt4.QtCore import *

class MyFrame(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        self.le = QLineEdit(self)
        self.le.setGeometry(200,200,75,35)

        i=0
        self.le.setText(str(i))

        self.connect(self.le, SIGNAL("textChanged(QString)"),self.updatedvalue)

    def updatedvalue(self):

        for i in range(1,5):
            self.le.setText(str(i))
            print(i)
            time.sleep(1)

app=QApplication(sys.argv)
f=MyFrame()
f.show()
app.exec_()

