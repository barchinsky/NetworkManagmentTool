#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Manage

import sys
from pysnmp.entity.rfc3413.oneliner import cmdgen
import xml.etree.ElementTree as ET
from lxml import etree
import re
#from InsertDB import ConnectionDB
import logging
import time
from ftplib import FTP

sys.path.append("./src")
from CONST import *
from LogManager import Log
from ConfigManager import ConfigManager

class NetworkManager:
    def __init__(self,_ip):
        cm = ConfigManager()
        Log("Network manager started")
        
        self.ip = cm.getSnmpIp()
        self.ports = ()
        self.cmdGen = cmdgen.CommandGenerator()
        self.devices = []
        self.inventory = []

        self.getDevicePorts()
        self.callDevices()

    def callDevices(self):
        Log("Calling devices...")

        for port in self.ports:
            errorIndication, errorStatus, errorIndex, self.varBinds = self.cmdGen.getCmd(
            cmdgen.CommunityData('public'),
            cmdgen.UdpTransportTarget((self.ip, port)),
            O_ID,
            O_DESCR,
            O_FPORTS,
            O_UPORTS,
            O_NETUP,
            O_NETDOWN,
            O_FANSPEED,
            O_VOLTAGE,
            O_TEMP,
            O_BANDLOAD,
            lookupNames=True, lookupValues=True)

            if errorIndication:
                print "Calling device error:"+port
                #logging.warning("Call device error. Port:" + port)
                Log("Call device error. Port:" + port,1) 
                #raise Exception("Call device error.Port "+port)
            elif errorStatus:
                #print (errorStatus,port),"Call device Error."
                #raise Exception("Error occured: port-"+port+" status-"+errorStatus)
                Log("Error occured: port-"+port+" status-"+errorStatus,1) 
            else:
                self.devices.append(self.varBinds)

        Log("Finished")
        self.makeXml()

    def printDeviceInfo(self):
        for dev in self.devices:
            for name,val in dev:
                print( '%s = %s' % ( name.prettyPrint(), val.prettyPrint() ) )
            print "----------------------------------------------------"

    def printToFile(self):
        Log("Printing data to file(data/device_info.txt...") 

        output = open("data/device_info.txt",'r+')
        for dev in self.devices:
            for name,val in dev:
                output.write(str(name) + '\n' + str(val) + '\n' )
            output.write('\n--------------\n')
        Log("Finished.")

    def makeXml(self):
        Log("Start making xml...")
        devices = []
        xmlFile = open('data/xml/device_info.xml','w')
        
        out = open('data/out','r+')
        for dev in self.devices:
            for name,val in dev:
                out.write(str(val)+'&&')
            out.write('\n')

        out.close()

        xml = etree.Element('xml')
        performanceData = []

        with open('data/out','r') as infile:
            for line in infile:
                performanceData = line.split('&&')
            
                root = etree.Element("Device")
                devId = etree.Element("Id")
                devId.text = performanceData[0]
                root.append(devId)

                sysDescr = etree.Element(SYSDESCR)
                sysDescr.text = performanceData[1]
                root.append(sysDescr)
                self.inventory.append(performanceData[1])

                freePorts = etree.Element(FREEPORTS)
                freePorts.text = performanceData[2]
                root.append(freePorts)

                usedPorts = etree.Element(USEDPORTS)
                usedPorts.text = performanceData[3]
                root.append(usedPorts)

                netUp = etree.Element(NETUP)
                netUp.text = performanceData[4]
                root.append(netUp)

                netDown = etree.Element(NETDOWN)
                netDown.text = performanceData[5]
                root.append(netDown)

                fanSpeed = etree.Element(FANSPEED)
                fanSpeed.text = performanceData[6]
                root.append(fanSpeed)
            
                voltage = etree.Element(VOLTAGE)
                voltage.text = performanceData[7]
                root.append(voltage)

                temp = etree.Element(TEMP)
                temp.text = performanceData[8]
                root.append(temp)

                bandLoad = etree.Element(BANDLOAD)
                bandLoad.text = performanceData[9]
                root.append(bandLoad)

                xml.append(root)

            xmlFile.write(etree.tostring(xml,pretty_print=True))

            Log("Finished.")


    def getDevicePorts(self):
        Log("Getting device ports...")
        
        infile = open('src/devices.txt','r')

        data = infile.readline()

        ports = []
        ports = re.findall('\d+',data)
        self.ports = ports

        Log("Finished.")

    def printInventory(self):
        Log("Printing inventory data...") 
        ftp = FTP(self.ip)
        ftp.login()
        invent_file = open("inventory.txt",'wb')
        ftp.retrbinary('RETR inventory.txt',invent_file.write,8*1024)
        invent_file.close()
        
        with open("inventory.txt",'r') as f:
            for line in f:
                print line.rstrip()
        

        Log("Finished.")

    def printDataForDevice(self,info_type,device_id):
        dic = self.getDictionary()
        errorIndication, errorStatus, errorIndex, varBinds = self.cmdGen.getCmd(
            cmdgen.CommunityData('public'),
            cmdgen.UdpTransportTarget((self.ip, device_id)),
            dic[info_type],
            lookupNames=True, lookupValues=True)

        if errorIndication:
            raise Exception("Call device error.Port "+port)
            Log("Call device error. Port:" + port,1) 

        elif errorStatus:
            raise Exception("Error occured: port-"+port+" status-"+errorStatus)
            Log("Call device error. Port:" + port + "Error status:" + errorStatus,1) 
        else:
            self.printVarBinds(varBinds,0)

    def getDictionary(self):
        dictionary = {}
        with open("data/mib",'r') as f:
            for line in f:
                (val,key) = line.split('-')
                dictionary[str(key.rstrip())] = str(val)
        return dictionary

    def printVarBinds(self,varBinds,options): # option: 0 - print val, 1 - print all
        if not options:
            for name,val in varBinds:
                print '------------------------------\n',val

    def insert_data_to_db(self):
        #ConnectionDB()
        pass

'''--------------------------debug zone-------------------------'''
#nm = NetworkManager('192.168.111.138')
#nm.getDeviceInfo()
#nm.printToFile()
