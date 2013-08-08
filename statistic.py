import numpy as np
import matplotlib.pyplot as plt
import cx_Oracle
import re
from pylab import *
import time
from PyQt4 import QtGui, QtCore
import sys
import numpy as np
import re

class Statistic:

    def __init__(self):
        pass
  
        
    def select_dev(self,text,M_T,time_st):
        #tm = time.time()
        #print tm
        print "service is "+text
        print "metric is "+M_T
        con = cx_Oracle.connect('orcdb/passw0rd@192.168.111.138/orcl')
        self.cur = con.cursor()
        if text=="BROADBAND":
            self.metr_BB(M_T,time_st)

        elif text=="IPTV":
            self.metr_IPTV()
        elif text=="VOIP":
            self.metr_VOIP(M_T)
        
        self.cur.close()
        con.close()


    def metr_BB(self,M_T,time_st):
        #M_T="STREAMUP"
        ts = time.time()
        print ts
        time_st = re.findall('[0-9]+',time_st)
        time_st = int(time_st[0])
        #tm = ts - (time_st*60)
        #print tm
        I_S = "BROADBAND"
        self.cur.execute("select MAX from METRICS WHERE IDSERVICE=:I_S AND METRIC_TYPE=:M_T",{'I_S':I_S,'M_T':M_T})
        data = self.cur.fetchall()
        lim = data[0][0]
        delay = []
        r = "MAX(DELAY)"
        t_str = "select "+r+" from BROADBAND WHERE TIMESTAMP>:tm AND TIMESTAMP<:ts"+",{'tm':tm,'ts':ts})"
        print t_str
        if time_st == 15:
            tm = ts - 60
            for i in range(15):
                self.cur.execute("select "+r+" from BROADBAND WHERE TIMESTAMP>:tm AND TIMESTAMP<:ts",{'tm':tm,'ts':ts})
                #self.cur.execute(":t_str",{'t_str':t_str})
                delay.append(self.cur.fetchall())
                ts = tm
                tm-=60

        elif time_st == 30:
            tm = ts - 180
            for i in range(10):
                self.cur.execute("select MAX(DELAY) from BROADBAND WHERE TIMESTAMP>:tm AND TIMESTAMP<:ts",{'tm':tm,'ts':ts})
                #print self.cur
                delay.append(self.cur.fetchall())
                ts = tm
                tm-=180
        elif time_st == 60:
            tm = ts - 10*60
            for i in range(6):
                self.cur.execute("select MAX(DELAY) from BROADBAND WHERE TIMESTAMP>:tm AND TIMESTAMP<:ts",{'tm':tm,'ts':ts})
                #print self.cur
                delay.append(self.cur.fetchall())
                ts = tm
                tm-=10*60
        elif time_st == 1:
            tm = ts - 60*60
            for i in range(24):
                self.cur.execute("select "+r+" from BROADBAND WHERE TIMESTAMP>:tm AND TIMESTAMP<:ts",{'tm':tm,'ts':ts})
                #print self.cur
                delay.append(self.cur.fetchall())
                ts = tm
                tm-=60*60


        #print delay[0][0][0]
        s_up = []
        ts = time.time()
        if time_st == 15:
            tm =ts - 60
            for i in range(15):
                self.cur.execute("select MAX(STREAMUP) from BROADBAND WHERE TIMESTAMP>:tm AND TIMESTAMP<:ts",{'tm':tm,'ts':ts})
                #print self.cur.fetchall()
                s_up.append(self.cur.fetchall())
                ts = tm
                tm-=60

        elif time_st == 30:
            tm = ts - 180
            for i in range(10):
                self.cur.execute("select MAX(STREAMUP) from BROADBAND WHERE TIMESTAMP>:tm AND TIMESTAMP<:ts",{'tm':tm,'ts':ts})
                #print self.cur
                s_up.append(self.cur.fetchall())
                ts = tm
                tm-=180
        elif time_st == 60:
            tm = ts - 10*60
            for i in range(6):
                self.cur.execute("select MAX(STREAMUP) from BROADBAND WHERE TIMESTAMP>:tm AND TIMESTAMP<:ts",{'tm':tm,'ts':ts})
                #print self.cur
                s_up.append(self.cur.fetchall())
                ts = tm
                tm-=10*60
        elif time_st == 1:
            tm = ts - 60*60
            for i in range(24):
                self.cur.execute("select MAX(STREAMUP) from BROADBAND WHERE TIMESTAMP>:tm AND TIMESTAMP<:ts",{'tm':tm,'ts':ts})
                #print self.cur
                s_up.append(self.cur.fetchall())
                ts = tm
                tm-=60*60
         
        s_down = []
        ts = time.time()
        if time_st == 15:
            tm =ts - 60
            for i in range(15):
                self.cur.execute("select MAX(STREAMDOWN) from BROADBAND WHERE TIMESTAMP>:tm AND TIMESTAMP<:ts",{'tm':tm,'ts':ts})
                #print self.cur.fetchall()
                s_down.append(self.cur.fetchall())
                ts = tm
                tm-=60

        elif time_st == 30:
            tm = ts - 180
            for i in range(10):
                self.cur.execute("select MAX(STREAMDOWN) from BROADBAND WHERE TIMESTAMP>:tm AND TIMESTAMP<:ts",{'tm':tm,'ts':ts})
                #print self.cur
                s_down.append(self.cur.fetchall())
                ts = tm
                tm-=180
        elif time_st == 60:
            tm = ts - 10*60
            for i in range(6):
                self.cur.execute("select MAX(STREAMDOWN) from BROADBAND WHERE TIMESTAMP>:tm AND TIMESTAMP<:ts",{'tm':tm,'ts':ts})
                #print self.cur
                s_down.append(self.cur.fetchall())
                ts = tm
                tm-=10*60
        elif time_st == 1:
            tm = ts - 60*60
            for i in range(24):
                self.cur.execute("select MAX(STREAMDOWN) from BROADBAND WHERE TIMESTAMP>:tm AND TIMESTAMP<:ts",{'tm':tm,'ts':ts})
                #print self.cur
                s_down.append(self.cur.fetchall())
                ts = tm
                tm-=60*60 
        p_loss = []
        ts = time.time()
        if time_st == 15:
            tm =ts - 60
            for i in range(15):
                self.cur.execute("select MAX(PACKET_LOSS) from BROADBAND WHERE TIMESTAMP>:tm AND TIMESTAMP<:ts",{'tm':tm,'ts':ts})
                #print self.cur.fetchall()
                p_loss.append(self.cur.fetchall())
                ts = tm
                tm-=60

        elif time_st == 30:
            tm = ts - 180
            for i in range(10):
                self.cur.execute("select MAX(PACKET_LOSS) from BROADBAND WHERE TIMESTAMP>:tm AND TIMESTAMP<:ts",{'tm':tm,'ts':ts})
                #print self.cur
                p_loss.append(self.cur.fetchall())
                ts = tm
                tm-=180
        elif time_st == 60:
            tm = ts - 10*60
            for i in range(6):
                self.cur.execute("select MAX(PACKET_LOSS) from BROADBAND WHERE TIMESTAMP>:tm AND TIMESTAMP<:ts",{'tm':tm,'ts':ts})
                #print self.cur
                p_loss.append(self.cur.fetchall())
                ts = tm
                tm-=10*60
        elif time_st == 1:
            tm = ts - 60*60
            for i in range(24):
                self.cur.execute("select MAX(PACKET_LOSS) from BROADBAND WHERE TIMESTAMP>:tm AND TIMESTAMP<:ts",{'tm':tm,'ts':ts})
                #print self.cur
                p_loss.append(self.cur.fetchall())
                ts = tm
                tm-=60*60 


        tmp = 0
        count = 0
        avr = 0
        '''for el in range(len(delay)):
            tmp+=delay[el]
            count+=1
        if count==0:
            avr = 0
        else:
            avr=tmp/count'''
        
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
            '''y = avr
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
            plt.show()'''
            
            #print delay
            x = []
            y = []
            for el in delay:
                if el[0][0] == None:
                    y.append(0)
                else:
                    y.append(el[0][0])
            print y
            for i in range(len(delay)):
                x.append(i+1)
                
            print x
            plt.bar(x,y,1)
            plt.xticks(x)
            plt.legend(['limit is '+str(lim)])
            plt.show()


        elif M_T == "STREAMUP":
          
            x = []
            y = []
            for el in s_up:
                if el[0][0] == None:
                    y.append(0)
                else:
                    y.append(el[0][0])
            print y
            for i in range(len(s_up)):
                x.append(i+1)
                
            print x
            plt.bar(x,y,1)
            plt.xticks(x)
            plt.legend(['limit is '+str(lim)])

            plt.show()


        elif M_T == "STREAMDOWN":
            x = []
            y = []
            for el in s_down:
                if el[0][0] == None:
                    y.append(0)
                else:
                    y.append(el[0][0])
            print y
            for i in range(len(s_down)):
                x.append(i+1)
                
            print x
            plt.bar(x,y,1)
            plt.xticks(x)
            plt.legend(['limit is '+str(lim)])

            plt.show() 

        elif M_T == "PACKET_LOSS":
            x = []
            y = []
            for el in p_loss:
                if el[0][0] == None:
                    y.append(0)
                else:
                    y.append(el[0][0])
            print y
            for i in range(len(p_loss)):
                x.append(i+1)
                
            print x
            plt.bar(x,y,1)
            plt.xticks(x)
            plt.legend(['limit is '+str(lim)])

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

