import numpy as np
import matplotlib.pyplot as plt
import cx_Oracle
import re
from pylab import *
import time

class Statistic_IPTV:

    def __init__(self):


        ts = time.time()
        last = ts-10*60
        con = cx_Oracle.connect('orcdb/passw0rd@192.168.111.138/orcl')
        cur = con.cursor()
        cur.execute("select PAYMENT from IPTV WHERE PAYMENT=0 AND TIMESTAMP>:last",{'last':last})
        tmp = cur.fetchall()
        ch_free = len(tmp)
        cur.execute("select PAYMENT from IPTV WHERE PAYMENT=1")
        tmp = cur.fetchall()
        ch_paid = len(tmp)
        self.grafic(ch_free,ch_paid)
        cur.close()
        con.close()
       
    def grafic(self,ch_free,ch_paid):
        x = [ch_free,ch_paid]
        labels = ['free channel', 'paid channel']
        explode = [0, 0]
        plt.pie(x, labels = labels, explode = explode, autopct = '%1.1f%%', shadow=True);
        plt.show()
   
      
obj = Statistic_IPTV()

