import numpy as np
import matplotlib.pyplot as plt
import cx_Oracle
import re
from pylab import *

class Statistic_VOIP:

    def __init__(self):

        con = cx_Oracle.connect('orcdb/passw0rd@192.168.111.138/orcl')
        cur = con.cursor()
        cur.execute("select DELAY from VOIP")
        delay = cur.fetchall()
        tmp = 0
        count_d = 0
        avr_d = 0
        for el in delay:
            tmp+=el[0]
            count_d+=1
        avr_d=tmp/count_d

        cur.execute("select ECHO from VOIP")
        echo = cur.fetchall()
        tmp_2 = 0
        count_e = 0
        avr_e = 0
        for el in echo:
            tmp_2+=el[0]
            count_e+=1
        avr_e=tmp_2/count_e

        cur.execute("select PACKET_LOSS from VOIP")
        p_loss = cur.fetchall()


        self.grafic(delay,avr_d,echo,avr_e,p_loss)
        cur.close()
        con.close()
       
    def grafic(self,delay,avr_d,echo,avr_e,p_loss):
        
        subplot(3,1,1)
        y = avr_d
        #plt.figure(21)
        #subplot(2,1,1)
        plt.plot(delay)  
        favr=[]
        limit_y = np.linspace(12,12,len(delay))
        limit_x = np.arange(len(delay))
        y = np.linspace(avr_d,avr_d,len(delay))
        x = np.arange(len(delay)) 
        plt.plot(x,y,'go-')
        plt.plot(limit_x,limit_y,'ro-')
        plt.xticks(range(len(delay)), ['a', 'b', 'c', 'd', 'e', 'f','g','k'])
        plt.legend(['delay','average','limit'])
        plt.xlim(0,len(delay))
        plt.ylim(0,20)

        subplot(3,1,2)
        y_1 = avr_e
        plt.plot(echo)  
        favr=[]
        limit_y = np.linspace(12,12,len(echo))
        limit_x = np.arange(len(echo))
        y_1 = np.linspace(avr_e,avr_e,len(echo))
        x_1 = np.arange(len(echo)) 
        plt.plot(x_1,y_1,'go-')
        plt.plot(limit_x,limit_y,'ro-')
        plt.xticks(range(len(echo)), ['a', 'b', 'c', 'd', 'e', 'f','g','k'])
        plt.legend(['echo','average','limit'])
        plt.xlim(0,len(echo))
        plt.ylim(0,20)

        subplot(3,1,3)
        plt.plot(p_loss)
        plt.legend(['packet loss'])
        plt.show()
   
      
obj = Statistic_VOIP()

