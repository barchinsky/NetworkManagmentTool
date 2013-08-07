import numpy as np
import matplotlib.pyplot as plt
import cx_Oracle
import re
from pylab import *
import time
from PyQt4 import QtGui, QtCore
import sys

class Statistic:

    def __init__(self):
        pass
  
        
    def select_dev(self,text,M_T):
        
        print "service is "+text
        print "metric is "+M_T
        con = cx_Oracle.connect('orcdb/passw0rd@192.168.111.138/orcl')
        self.cur = con.cursor()
        if text=="BROADBAND":
            self.metr_BB(M_T)

        elif text=="IPTV":
            self.metr_IPTV()
        elif text=="VOIP":
            self.metr_VOIP(M_T)
        
        self.cur.close()
        con.close()


    def metr_BB(self,M_T):
        #M_T="STREAMUP"
        I_S = "BROADBAND"
        self.cur.execute("select MAX from METRICS WHERE IDSERVICE=:I_S AND METRIC_TYPE=:M_T",{'I_S':I_S,'M_T':M_T})
        data = self.cur.fetchall()
        lim = data[0][0]
        self.cur.execute("select DELAY from BROADBAND")
        delay = self.cur.fetchall()
        
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
        
        self.grafic_BB(delay,avr,time,s_up,s_down,p_loss,lim,M_T)

    def metr_IPTV(self):
        self.cur.execute("select PAYMENT from IPTV WHERE PAYMENT=0")
        channel = self.cur.fetchall()
        ch_free = len(channel)
        self.cur.execute("select PAYMENT from IPTV WHERE PAYMENT=1")
        channel = self.cur.fetchall()
        ch_paid = len(channel)
        self.grafic_IPTV(ch_free,ch_paid)


    def metr_VOIP(self,M_T):
        I_S = "VOIP"
        self.cur.execute("select MAX from METRICS WHERE IDSERVICE=:I_S AND METRIC_TYPE=:M_T",{'I_S':I_S,'M_T':M_T})
        data = self.cur.fetchall()
        lim = data[0][0]

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

        self.grafic_VOIP(delay_vo,avr_d,echo,avr_e,p_loss_vo,M_T,lim)

 


    def grafic_BB(self,delay,avr,time,s_up,s_down,p_loss,lim,M_T):
        if M_T == "DELAY":
            y = avr
            plt.figure(21)
            plt.plot(delay)  
            favr=[]
            limit_y = np.linspace(lim,lim,len(delay))
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

        elif M_T == "STREAMUP":
            plt.plot(s_up,'g')
            plt.legend(['stream_up'])
            plt.xlim(0,len(s_up))
            plt.ylim(0,10000)
            plt.show()

        elif M_T == "STREAMDOWN":
            plt.plot(s_down,'r')
            plt.legend(['stream_down'])
            plt.xlim(0,len(s_up))
            plt.ylim(0,10000)
            plt.show()


        elif M_T == "PACKET_LOSS":
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

    def grafic_VOIP(self,delay_vo,avr_d,echo,avr_e,p_loss_vo,M_T,lim):
        
        if M_T == "DELAY":
            y = avr_d
            plt.plot(delay_vo)  
            favr=[]
            limit_y = np.linspace(lim,lim,len(delay_vo))
            limit_x = np.arange(len(delay_vo))
            y = np.linspace(avr_d,avr_d,len(delay_vo))
            x = np.arange(len(delay_vo)) 
            plt.plot(x,y,'go-')
            plt.plot(limit_x,limit_y,'ro-')
            plt.xticks(range(len(delay_vo)), ['a', 'b', 'c', 'd', 'e', 'f','g','k'])
            plt.legend(['delay','average','limit'])
            plt.xlim(0,len(delay_vo))
            plt.ylim(0,20)
            plt.show()


        elif M_T == "ECHO":
            y_1 = avr_e
            plt.plot(echo)  
            favr=[]
            limit_y = np.linspace(lim,lim,len(echo))
            limit_x = np.arange(len(echo))
            y_1 = np.linspace(avr_e,avr_e,len(echo))
            x_1 = np.arange(len(echo)) 
            plt.plot(x_1,y_1,'go-')
            plt.plot(limit_x,limit_y,'ro-')
            plt.xticks(range(len(echo)), ['a', 'b', 'c', 'd', 'e', 'f','g','k'])
            plt.legend(['echo','average','limit'])
            plt.xlim(0,len(echo))
            plt.ylim(0,20)
            plt.show()


        elif M_T == "PACKET_LOSS":
            plt.plot(p_loss_vo)
            plt.legend(['packet loss'])
            plt.show()

obj = Statistic()

