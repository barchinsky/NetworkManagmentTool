import numpy as np
import matplotlib.pyplot as plt
import cx_Oracle
import re
from pylab import *
import time

class Statistic_BB:

    def __init__(self):

        ts = time.time()
        last = ts-20*60*10
        #print last
        con = cx_Oracle.connect('orcdb/passw0rd@192.168.111.138/orcl')
        cur = con.cursor()
        cur.execute("select DELAY from BROADBAND WHERE TIMESTAMP>:last",{'last':last})
        delay = cur.fetchall()
        #cur.execute("select TIMESTAMP from BROADBAND")
        #time = cur.fetchall()
        cur.execute("select STREAMUP from BROADBAND")
        s_up = cur.fetchall()
        cur.execute("select STREAMDOWN from BROADBAND")
        s_down = cur.fetchall()
        cur.execute("select PACKET_LOSS from BROADBAND")
        p_loss = cur.fetchall()


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

        self.grafic(delay,avr,time,s_up,s_down,p_loss)
   
        cur.close()
        con.close()
       
    def grafic(self,delay,avr,time,s_up,s_down,p_loss):
        y = avr
        plt.figure(21)
        subplot(3,1,1)
        plt.plot(delay)  
        favr=[]
        limit_y = np.linspace(5,5,len(delay))
        limit_x = np.arange(len(delay))
        y = np.linspace(avr,avr,len(delay))
        x = np.arange(len(delay)) 
        plt.plot(x,y,'go-')
        plt.plot(limit_x,limit_y,'ro-')
        plt.xticks(range(len(delay)), ['a', 'b', 'c', 'd', 'e', 'f','g','k'])
        plt.legend(['delay','average','limit'])
        plt.xlim(0,len(delay))
        plt.ylim(0,10)

        subplot(3,1,2)
        plt.plot(s_up,'g')
        plt.plot(s_down,'r')
        plt.legend(['stream_up','stream_down'])
        plt.xlim(0,len(s_up))
        plt.ylim(0,10000)

        subplot(3,1,3)
        plt.plot(p_loss,'g')
        plt.legend(['p_loss'])
        plt.xlim(0,len(p_loss))
        plt.ylim(0,200)

        plt.show()
   
      
obj = Statistic_BB()

