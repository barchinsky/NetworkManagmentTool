import cx_Oracle
from xml.dom.minidom import *
import sys
import logging

from CONST import *

class ConnectionDB:

    def __init__(self):

        #print sys.argv[1]
        self.logger = logging.getLogger('insert')
        hdlr = logging.FileHandler('data/insert.log')
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        hdlr.setFormatter(formatter)
        self.logger.addHandler(hdlr) 
        self.logger.setLevel(logging.WARNING)
        self.logger.setLevel(logging.INFO)

        self.con = cx_Oracle.connect('orcdb/passw0rd@192.168.111.138/orcl')
        self.logger.info('connect to db') 
        self.cur = self.con.cursor()
        self.parse()
        self.cur.close()
        print "End."
        self.con.close()
        self.logger.info('disconnect db')

    def parse(self):

        Id = []
        sysDescr = []
        sysLocation = []
        freePorts = []
        usedPorts = []
        netUp = []
        netDown = []
        fanSpeed = []
        voltage = []
        temp = []
        bandLoad = []

                
        xml = parse('data/xml/device_info.xml')

        iden = xml.getElementsByTagName(ID)
        descr = xml.getElementsByTagName(SYSDESCR)
        fports = xml.getElementsByTagName(FREEPORTS)
        uports = xml.getElementsByTagName(USEDPORTS)
        nU = xml.getElementsByTagName(NETUP)
        nD = xml.getElementsByTagName(NETDOWN)
        fSpeed = xml.getElementsByTagName(FANSPEED)
        volt = xml.getElementsByTagName(VOLTAGE)
        tmp = xml.getElementsByTagName(TEMP)
        bLoad = xml.getElementsByTagName(BANDLOAD)
        loc = xml.getElementsByTagName(SYSLOCATION)
       
        for node in iden:
           Id.append(node.childNodes[0].nodeValue)
        for node in descr:
           sysDescr.append(node.childNodes[0].nodeValue)
        for node in fports:
           freePorts.append(node.childNodes[0].nodeValue)
        for node in uports:
           usedPorts.append(node.childNodes[0].nodeValue)
        for node in nU:
           netUp.append(node.childNodes[0].nodeValue)
        for node in nD:
           netDown.append(node.childNodes[0].nodeValue)
        for node in fSpeed:
           fanSpeed.append(node.childNodes[0].nodeValue)
        for node in volt:
           voltage.append(node.childNodes[0].nodeValue)
        for node in tmp:
           temp.append(node.childNodes[0].nodeValue)
        for node in bLoad:
           bandLoad.append(node.childNodes[0].nodeValue)
        for node in loc:
           sysLocation.append(node.childNodes[0].nodeValue)

        self.insertDB(Id,sysDescr,sysLocation,usedPorts,netUp,netDown,voltage,fanSpeed,temp,bandLoad,freePorts)

    def insertDB(self,Id,sysDescr,sysLocation,usedPorts,netUp,netDown,voltage,fanSpeed,temp,bandLoad,freePorts):
        i=0
        while i<len(Id):

            #self.cur.execute("select * from SYSTEM.PERFORMANCE_DATA")
            #print self.cur.fetchall()
            try:
                self.cur.callproc("SYSTEM.add_performance_data",[Id[i],sysDescr[i],usedPorts[i],netUp[i],netDown[i],voltage[i],fanSpeed[i],temp[i],bandLoad[i],freePorts[i]])
                
                self.logger.info('call stored procedure')
                self.con.commit()
            except Exception:
                print 'Cant inserting!!!  already exist: ',sysDescr[i]
                self.logger.error('already exist '+Id[i])
            i+=1
        print "\nafter inserting"
        self.cur.execute("select * from SYSTEM.PERFORMANCE_DATA")
        print self.cur.fetchall()
obj=ConnectionDB()
