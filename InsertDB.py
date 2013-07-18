import cx_Oracle
from xml.dom.minidom import *
import sys

class ConnectionDB:

    def __init__(self):
        

        print sys.argv[1]
        self.con = cx_Oracle.connect('orcdb/passw0rd@192.168.111.138/orcl')

        self.cur = self.con.cursor()
        self.parse()
        self.cur.close()
        print "End."
        self.con.close()



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

        xml = parse(sys.argv[1])

        iden = xml.getElementsByTagName('Id')
        descr = xml.getElementsByTagName('sysDescr')
        fports = xml.getElementsByTagName('freePorts')
        uports = xml.getElementsByTagName('usedPorts')
        nU = xml.getElementsByTagName('netUp')
        nD = xml.getElementsByTagName('netDown')
        fSpeed = xml.getElementsByTagName('fanSpeed')
        volt = xml.getElementsByTagName('voltage')
        tmp = xml.getElementsByTagName('temp')
        bLoad = xml.getElementsByTagName('bandLoad')
        loc = xml.getElementsByTagName('sysLocation')
  
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

            self.cur.execute("select * from SYSTEM.PERFORMANCE_DATA")
            print self.cur.fetchall()

            self.cur.execute("insert into SYSTEM.PERFORMANCE_DATA(ID,SYSDESCR,SYSLOC,USEDPORTS,NETUP,NETDOWN,VOLTAGE,FAN,TEMPERATURE,BANDWIDTHLOAD,FREEPORTS) values(:Id,:sysD,:sysL,:uP,:nU,:nD,:vol,:fan,:t,:bwl,:fP)",{'Id':Id[i],'sysD':sysDescr[i],'sysL':sysLocation[i],'uP':usedPorts[i],'nU':netUp[i],'nD':netDown[i],'vol':voltage[i],'fan':fanSpeed[i],'t':temp[i],'bwl':bandLoad[i],'fP':freePorts[i]})
            self.con.commit()
            print "\nafter inserting"
            self.cur.execute("select * from SYSTEM.PERFORMANCE_DATA")
            print self.cur.fetchall()
            i+=1
obj=ConnectionDB()
