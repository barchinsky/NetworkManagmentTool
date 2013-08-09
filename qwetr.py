import cx_Oracle
import time


con = cx_Oracle.connect('orcdb/passw0rd@192.168.111.138/orcl')
cur = con.cursor()
t = time.time()
tm = t - 30*60
cur.execute("select STREAMUP FROM BROADBAND WHERE TIMESTAMP>:tm",{'tm':tm})
data = cur.fetchall()
print data
