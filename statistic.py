import numpy as np
import matplotlib.pyplot as plt
import cx_Oracle

class Statistic:

    def __init__(self):

        con = cx_Oracle.connect('orcdb/passw0rd@192.168.111.138/orcl')
        cur = con.cursor()
        cur.execute("select NETUP from SYSTEM.PERFORMANCE_DATA")
        data = cur.fetchall()

        self.grafic(data)
        cur.close()
        con.close()

    def grafic(self,data):
        print data
        plt.figure(21)
        plt.plot(data)
        plt.xticks(range(len(data)), ['a', 'b', 'c', 'd', 'e', 'f'])
        plt.show()
      
obj = Statistic()

