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
        s = raw_input("statistic about:\n1)BROADBAND\n2)IPTV\n3)VOIP\n")
        print s
        if s=="1":
            self.cur.execute("select DELAY from BROADBAND")
            delay = self.cur.fetchall()
            #cur.execute("select TIMESTAMP from BROADBAND")
            #time = cur.fetchall()
            self.cur.execute("select STREAMUP from BROADBAND")
            s_up = self.cur.fetchall()
            self.cur.execute("select STREAMDOWN from BROADBAND")
            s_down = self.cur.fetchall()
            self.cur.execute("select PACKET_LOSS from BROADBAND")
            p_loss = self.cur.fetchall()


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
        
            self.grafic_BB(delay,avr,time,s_up,s_down,p_loss)

        elif s=="2":
            self.cur.execute("select PAYMENT from IPTV WHERE PAYMENT=0")
            channel = self.cur.fetchall()
            ch_free = len(channel)
            self.cur.execute("select PAYMENT from IPTV WHERE PAYMENT=1")
            channel = self.cur.fetchall()
            ch_paid = len(channel)
            self.grafic_IPTV(ch_free,ch_paid)

        elif s=="3":
            self.cur.execute("select DELAY from VOIP")
            delay_vo = self.cur.fetchall()
            tmp1 = 0
            count_d = 0
            avr_d = 0
            for el in delay_vo:
                tmp1+=el[0]
                count_d+=1
            avr_d=tmp1/count_d

            self.cur.execute("select ECHO from VOIP")
            echo = self.cur.fetchall()
            tmp_2 = 0
            count_e = 0
            avr_e = 0
            for el in echo:
                tmp_2+=el[0]
                count_e+=1
            avr_e=tmp_2/count_e

            self.cur.execute("select PACKET_LOSS from VOIP")
            p_loss_vo = self.cur.fetchall()


            self.grafic_VOIP(delay_vo,avr_d,echo,avr_e,p_loss_vo)




       
    def grafic_BB(self,delay,avr,time,s_up,s_down,p_loss):
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

    def grafic_IPTV(self,ch_free,ch_paid):
        x = [ch_free,ch_paid]
        labels = ['free channel', 'paid channel']
        explode = [0, 0]
        plt.pie(x, labels = labels, explode = explode, autopct = '%1.1f%%', shadow=True);
        plt.show()

    def grafic_VOIP(self,delay_vo,avr_d,echo,avr_e,p_loss_vo):
        
        subplot(3,1,1)
        y = avr_d
        #plt.figure(21)
        #subplot(2,1,1)
        plt.plot(delay_vo)  
        favr=[]
        limit_y = np.linspace(12,12,len(delay_vo))
        limit_x = np.arange(len(delay_vo))
        y = np.linspace(avr_d,avr_d,len(delay_vo))
        x = np.arange(len(delay_vo)) 
        plt.plot(x,y,'go-')
        plt.plot(limit_x,limit_y,'ro-')
        plt.xticks(range(len(delay_vo)), ['a', 'b', 'c', 'd', 'e', 'f','g','k'])
        plt.legend(['delay','average','limit'])
        plt.xlim(0,len(delay_vo))
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
        plt.plot(p_loss_vo)
        plt.legend(['packet loss'])
        plt.show()

 
   
      
obj = Statistic()

