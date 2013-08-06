import numpy as np
import matplotlib.pyplot as plt
import cx_Oracle
import re
from pylab import *
import time

class Statistic:

    def __init__(self):

        #ts = time.time()
        #last = ts-20*60*1000
        #print last
        con = cx_Oracle.connect('orcdb/passw0rd@192.168.111.138/orcl')
        self.cur = con.cursor()
        self.select_dev()
        self.cur.close()
        con.close()

    def select_dev(self):
        ID_SER = "BROADBAND"
        M_T = "DELAY"
        self.cur.execute("select MAX from METRICS WHERE IDSERVICE=:ID_SER AND METRIC_TYPE=:M_T",{'ID_SER':ID_SER,'M_T':M_T})
        data = self.cur.fetchall()
        limit = 0
        for d in data:
            limit = d[0]

        self.cur.execute("select %M_T from %ID_SER")
        delay = self.cur.fetchall()
        '''self.cur.execute("select STREAMUP from BROADBAND")
        s_up = self.cur.fetchall()
        self.cur.execute("select STREAMDOWN from BROADBAND")
        s_down = self.cur.fetchall()
        self.cur.execute("select PACKET_LOSS from BROADBAND")
        p_loss = self.cur.fetchall()'''

        tmp = 0
        count = 0
        avr = 0
        for el in delay:
            tmp+=el[0]
            count+=1
        if count==0:
            avr = 0
        else:
            avr=tmp/count
        
        self.grafic_BB(delay,avr,limit)

      



       
    def grafic_BB(self,delay,avr,limit):
        y = avr
        plt.figure(21)
        plt.plot(delay)  
        favr=[]
        limit_y = np.linspace(limit,limit,len(delay))
        limit_x = np.arange(len(delay))
        y = np.linspace(avr,avr,len(delay))
        x = np.arange(len(delay)) 
        plt.plot(x,y,'go-')
        plt.plot(limit_x,limit_y,'ro-')
        plt.xticks(range(len(delay)), ['a', 'b', 'c', 'd', 'e', 'f','g','k'])
        plt.legend(['delay','average','limit'])
        plt.xlim(0,len(delay))
        plt.ylim(0,10)
        plt.show()

    def grafic_IPTV(self,ch_free,ch_paid):
        x = [ch_free,ch_paid]
        labels = ['free channel', 'paid channel']
        explode = [0, 0]
        plt.pie(x, labels = labels, explode = explode, autopct = '%1.1f%%', shadow=True);
        plt.show()

     
   
      
obj = Statistic()

