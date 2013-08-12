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
  
        
    def select_dev(self,text,M_T,time_st,op_type,koef):
        print koef
        #tm = time.time()
        #print tm
        print "service is "+text
        print "metric is "+M_T
        #op_type = "MAX"

        con = cx_Oracle.connect('orcdb/passw0rd@192.168.111.138/orcl')
        self.cur = con.cursor()
        if text=="BROADBAND":
            self.metr_BB(M_T,time_st,op_type,koef)

        elif text=="IPTV":
            self.metr_IPTV()
        elif text=="VOIP":
            self.metr_VOIP(M_T,time_st,op_type,koef)
        
        self.cur.close()
        con.close()


    def metr_BB(self,M_T,time_st,op_type,koef):
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
        #op_type = "MAX"
        #t_str = "select "+r+" from BROADBAND WHERE TIMESTAMP>:tm AND TIMESTAMP<:ts"+",{'tm':tm,'ts':ts})"
        #print t_str
        if time_st == 15:
            tm = ts - 60
            for i in range(15):
                self.cur.execute("select "+koef+" from BROADBAND WHERE TIMESTAMP>:tm AND TIMESTAMP<:ts",{'tm':tm,'ts':ts})
                #self.cur.execute(":t_str",{'t_str':t_str})
                delay.append(self.cur.fetchall())
                ts = tm
                tm-=60

        elif time_st == 30:
            tm = ts - 180
            for i in range(10):
                self.cur.execute("select "+koef+" from BROADBAND WHERE TIMESTAMP>:tm AND TIMESTAMP<:ts",{'tm':tm,'ts':ts})
                #print self.cur
                delay.append(self.cur.fetchall())
                ts = tm
                tm-=180
        elif time_st == 60:
            tm = ts - 10*60
            for i in range(6):
                self.cur.execute("select "+koef+" from BROADBAND WHERE TIMESTAMP>:tm AND TIMESTAMP<:ts",{'tm':tm,'ts':ts})
                #print self.cur
                delay.append(self.cur.fetchall())
                ts = tm
                tm-=10*60
        elif time_st == 1:
            tm = ts - 60*60
            for i in range(24):
                self.cur.execute("select "+koef+" from BROADBAND WHERE TIMESTAMP>:tm AND TIMESTAMP<:ts",{'tm':tm,'ts':ts})
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
                self.cur.execute("select "+koef+" from BROADBAND WHERE TIMESTAMP>:tm AND TIMESTAMP<:ts",{'tm':tm,'ts':ts})
                #print self.cur.fetchall()
                s_up.append(self.cur.fetchall())
                ts = tm
                tm-=60

        elif time_st == 30:
            tm = ts - 180
            for i in range(10):
                self.cur.execute("select "+koef+" from BROADBAND WHERE TIMESTAMP>:tm AND TIMESTAMP<:ts",{'tm':tm,'ts':ts})
                #print self.cur
                s_up.append(self.cur.fetchall())
                ts = tm
                tm-=180
        elif time_st == 60:
            tm = ts - 10*60
            for i in range(6):
                self.cur.execute("select "+koef+" from BROADBAND WHERE TIMESTAMP>:tm AND TIMESTAMP<:ts",{'tm':tm,'ts':ts})
                #print self.cur
                s_up.append(self.cur.fetchall())
                ts = tm
                tm-=10*60
        elif time_st == 1:
            tm = ts - 60*60
            for i in range(24):
                self.cur.execute("select "+koef+" from BROADBAND WHERE TIMESTAMP>:tm AND TIMESTAMP<:ts",{'tm':tm,'ts':ts})
                #print self.cur
                s_up.append(self.cur.fetchall())
                ts = tm
                tm-=60*60
         
        s_down = []
        ts = time.time()
        if time_st == 15:
            tm =ts - 60
            for i in range(15):
                self.cur.execute("select "+koef+" from BROADBAND WHERE TIMESTAMP>:tm AND TIMESTAMP<:ts",{'tm':tm,'ts':ts})
                #print self.cur.fetchall()
                s_down.append(self.cur.fetchall())
                ts = tm
                tm-=60

        elif time_st == 30:
            tm = ts - 180
            for i in range(10):
                self.cur.execute("select "+koef+" from BROADBAND WHERE TIMESTAMP>:tm AND TIMESTAMP<:ts",{'tm':tm,'ts':ts})
                #print self.cur
                s_down.append(self.cur.fetchall())
                ts = tm
                tm-=180
        elif time_st == 60:
            tm = ts - 10*60
            for i in range(6):
                self.cur.execute("select "+koef+" from BROADBAND WHERE TIMESTAMP>:tm AND TIMESTAMP<:ts",{'tm':tm,'ts':ts})
                #print self.cur
                s_down.append(self.cur.fetchall())
                ts = tm
                tm-=10*60
        elif time_st == 1:
            tm = ts - 60*60
            for i in range(24):
                self.cur.execute("select "+koef+" from BROADBAND WHERE TIMESTAMP>:tm AND TIMESTAMP<:ts",{'tm':tm,'ts':ts})
                #print self.cur
                s_down.append(self.cur.fetchall())
                ts = tm
                tm-=60*60 
        p_loss = []
        ts = time.time()
        if time_st == 15:
            tm =ts - 60
            for i in range(15):
                self.cur.execute("select "+koef+" from BROADBAND WHERE TIMESTAMP>:tm AND TIMESTAMP<:ts",{'tm':tm,'ts':ts})
                #print self.cur.fetchall()
                p_loss.append(self.cur.fetchall())
                ts = tm
                tm-=60

        elif time_st == 30:
            tm = ts - 180
            for i in range(10):
                self.cur.execute("select "+koef+" from BROADBAND WHERE TIMESTAMP>:tm AND TIMESTAMP<:ts",{'tm':tm,'ts':ts})
                #print self.cur
                p_loss.append(self.cur.fetchall())
                ts = tm
                tm-=180
        elif time_st == 60:
            tm = ts - 10*60
            for i in range(6):
                self.cur.execute("select "+koef+" from BROADBAND WHERE TIMESTAMP>:tm AND TIMESTAMP<:ts",{'tm':tm,'ts':ts})
                #print self.cur
                p_loss.append(self.cur.fetchall())
                ts = tm
                tm-=10*60
        elif time_st == 1:
            tm = ts - 60*60
            for i in range(24):
                self.cur.execute("select "+koef+" from BROADBAND WHERE TIMESTAMP>:tm AND TIMESTAMP<:ts",{'tm':tm,'ts':ts})
                #print self.cur
                p_loss.append(self.cur.fetchall())
                ts = tm
                tm-=60*60 


        
        self.grafic_BB(delay,time,s_up,s_down,p_loss,lim,M_T)

    def metr_IPTV(self):
        self.cur.execute("select PAYMENT from IPTV WHERE PAYMENT=0")
        channel = self.cur.fetchall()
        ch_free = len(channel)
        self.cur.execute("select PAYMENT from IPTV WHERE PAYMENT=1")
        channel = self.cur.fetchall()
        ch_paid = len(channel)
        self.grafic_IPTV(ch_free,ch_paid)


    def metr_VOIP(self,M_T,time_st,op_type,koef):
        I_S = "VOIP"
        self.cur.execute("select MAX from METRICS WHERE IDSERVICE=:I_S AND METRIC_TYPE=:M_T",{'I_S':I_S,'M_T':M_T})
        data = self.cur.fetchall()
        lim = data[0][0]
        delay_vo = []
        time_st = re.findall('[0-9]+',time_st)
        time_st = int(time_st[0])

        ts = time.time()

        if time_st == 15:
            tm = ts - 60
            for i in range(15):
                self.cur.execute("select "+koef+" from VOIP WHERE TIMESTAMP>:tm AND TIMESTAMP<:ts",{'tm':tm,'ts':ts})
                #self.cur.execute(":t_str",{'t_str':t_str})
                delay_vo.append(self.cur.fetchall())
                ts = tm
                tm-=60

        elif time_st == 30:
            tm = ts - 180
            for i in range(10):
                self.cur.execute("select "+koef+" from VOIP WHERE TIMESTAMP>:tm AND TIMESTAMP<:ts",{'tm':tm,'ts':ts})
                #print self.cur
                delay_vo.append(self.cur.fetchall())
                ts = tm
                tm-=180
        elif time_st == 60:
            tm = ts - 10*60
            for i in range(6):
                self.cur.execute("select "+koef+" from VOIP WHERE TIMESTAMP>:tm AND TIMESTAMP<:ts",{'tm':tm,'ts':ts})
                #print self.cur
                delay_vo.append(self.cur.fetchall())
                ts = tm
                tm-=10*60
        elif time_st == 1:
            tm = ts - 60*60
            for i in range(24):
                self.cur.execute("select "+koef+" from VOIP WHERE TIMESTAMP>:tm AND TIMESTAMP<:ts",{'tm':tm,'ts':ts})
                #print self.cur
                delay_vo.append(self.cur.fetchall())
                ts = tm
                tm-=60*60

        echo = []
        ts = time.time()
        if time_st == 15:
            tm = ts - 60
            for i in range(15):
                self.cur.execute("select "+koef+" from VOIP WHERE TIMESTAMP>:tm AND TIMESTAMP<:ts",{'tm':tm,'ts':ts})
                #self.cur.execute(":t_str",{'t_str':t_str})
                echo.append(self.cur.fetchall())
                ts = tm
                tm-=60

        elif time_st == 30:
            tm = ts - 180
            for i in range(10):
                self.cur.execute("select "+koef+" from VOIP WHERE TIMESTAMP>:tm AND TIMESTAMP<:ts",{'tm':tm,'ts':ts})
                #print self.cur
                echo.append(self.cur.fetchall())
                ts = tm
                tm-=180
        elif time_st == 60:
            tm = ts - 10*60
            for i in range(6):
                self.cur.execute("select "+koef+" from VOIP WHERE TIMESTAMP>:tm AND TIMESTAMP<:ts",{'tm':tm,'ts':ts})
                #print self.cur
                echo.append(self.cur.fetchall())
                ts = tm
                tm-=10*60
        elif time_st == 1:
            tm = ts - 60*60
            for i in range(24):
                self.cur.execute("select "+koef+" from VOIP WHERE TIMESTAMP>:tm AND TIMESTAMP<:ts",{'tm':tm,'ts':ts})
                #print self.cur
                echo.append(self.cur.fetchall())
                ts = tm
                tm-=60*60


        p_loss_vo = []
        ts = time.time()
        if time_st == 15:
            tm = ts - 60
            for i in range(15):
                self.cur.execute("select "+koef+" from VOIP WHERE TIMESTAMP>:tm AND TIMESTAMP<:ts",{'tm':tm,'ts':ts})
                #self.cur.execute(":t_str",{'t_str':t_str})
                p_loss_vo.append(self.cur.fetchall())
                ts = tm
                tm-=60

        elif time_st == 30:
            tm = ts - 180
            for i in range(10):
                self.cur.execute("select "+koef+" from VOIP WHERE TIMESTAMP>:tm AND TIMESTAMP<:ts",{'tm':tm,'ts':ts})
                #print self.cur
                p_loss_vo.append(self.cur.fetchall())
                ts = tm
                tm-=180
        elif time_st == 60:
            tm = ts - 10*60
            for i in range(6):
                self.cur.execute("select "+koef+" from VOIP WHERE TIMESTAMP>:tm AND TIMESTAMP<:ts",{'tm':tm,'ts':ts})
                #print self.cur
                p_loss_vo.append(self.cur.fetchall())
                ts = tm
                tm-=10*60
        elif time_st == 1:
            tm = ts - 60*60
            for i in range(24):
                self.cur.execute("select "+koef+" from VOIP WHERE TIMESTAMP>:tm AND TIMESTAMP<:ts",{'tm':tm,'ts':ts})
                #print self.cur
                p_loss_vo.append(self.cur.fetchall())
                ts = tm
                tm-=60*60
        

        self.grafic_VOIP(delay_vo,echo,p_loss_vo,M_T,lim)

 


    def grafic_BB(self,delay,time,s_up,s_down,p_loss,lim,M_T):
        if M_T == "DELAY":

            
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

    def grafic_VOIP(self,delay_vo,echo,p_loss_vo,M_T,lim):
        
        if M_T == "DELAY":

            x = []
            y = []
            print delay_vo
            for el in delay_vo:
                if el[0][0] == None:
                    y.append(0)
                else:
                    y.append(el[0][0])
            print y
            for i in range(len(delay_vo)):
                x.append(i+1)
                
            print x
            plt.bar(x,y,1)
            plt.xticks(x)
            plt.legend(['limit is '+str(lim)])
            plt.show()



        elif M_T == "ECHO":
            x = []
            y = []
            print echo
            for el in echo:
                if el[0][0] == None:
                    y.append(0)
                else:
                    y.append(el[0][0])
            print y
            for i in range(len(echo)):
                x.append(i+1)
                
            print x
            plt.bar(x,y,1)
            plt.xticks(x)
            plt.legend(['limit is '+str(lim)])
            plt.show() 

        elif M_T == "PACKET_LOSS":
            x = []
            y = []
            print echo
            for el in p_loss_vo:
                if el[0][0] == None:
                    y.append(0)
                else:
                    y.append(el[0][0])
            print y
            for i in range(len(p_loss_vo)):
                x.append(i+1)
                
            print x
            plt.bar(x,y,1)
            plt.xticks(x)
            plt.legend(['limit is '+str(lim)])
            plt.show()  
obj = Statistic()

