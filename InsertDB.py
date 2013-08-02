import cx_Oracle
from xml.dom.minidom import *
import sys
import logging

from CONST import *
from ConfigManager import ConfigManager

class ConnectionDB:

    def __init__(self):

        self.cm = ConfigManager()
        #print sys.argv[1]
        self.logger = logging.getLogger('insert')
        hdlr = logging.FileHandler(self.cm.getInsertLog())
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        hdlr.setFormatter(formatter)
        self.logger.addHandler(hdlr) 
        self.logger.setLevel(logging.WARNING)
        self.logger.setLevel(logging.INFO)

        self.con = cx_Oracle.connect(self.cm.getDBConnection())
        self.logger.info('connect to db') 
        self.cur = self.con.cursor()
        self.parse()
        self.cur.close()
        #print "End."
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

                
        xml = parse(self.cm.getDeviceInfoFile())

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

        self.insertDB(Id,sysDescr,usedPorts,netUp,netDown,voltage,fanSpeed,temp,bandLoad,freePorts)

    def insertDB(self,Id,sysDescr,usedPorts,netUp,netDown,voltage,fanSpeed,temp,bandLoad,freePorts):
        i=0
        while i<len(Id):

            #self.cur.execute("select * from SYSTEM.PERFORMANCE_DATA")
            #print self.cur.fetchall()
            try:
                self.cur.callproc("add_performance_data",[Id[i],sysDescr[i],usedPorts[i],netUp[i],netDown[i],voltage[i],fanSpeed[i],temp[i],bandLoad[i],freePorts[i]])
                
                self.logger.info('call stored procedure')
                self.con.commit()
            except Exception,f:
                print f
                print 'Cant inserting!!! '+Id[i]
                self.logger.error('Can not inserting '+Id[i])
            i+=1
        #print "\nafter inserting"
        #self.cur.execute("select * from SYSTEM.PERFORMANCE_DATA")
        #print self.cur.fetchall()
obj=ConnectionDB()
