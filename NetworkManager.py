#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from pysnmp.entity.rfc3413.oneliner import cmdgen
import xml.etree.ElementTree as ET
from lxml import etree
import re
#from src.MyLib import *

#sys.path.append("/home/max/TF/NetworkManagmentTool/src")
from CONST import *

class NetworkManager:
    def __init__(self,_ip):
        self.ip = _ip
        self.ports = ()
        self.cmdGen = cmdgen.CommandGenerator()
        self.devices = []

        self.getDevicePorts()
        self.callDevices()
        self.printDeviceInfo()

    def callDevices(self):
        for port in self.ports:
            errorIndication, errorStatus, errorIndex, self.varBinds = self.cmdGen.getCmd(
            cmdgen.CommunityData('public'),
            cmdgen.UdpTransportTarget((self.ip, port)),
            O_ID,
            O_DESCR,
            O_LOCATION,
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
                print (errorIndication,port)
            elif errorStatus:
                print (errorStatus,port)
            else:
                self.devices.append(self.varBinds)

        self.makeXml()

    def printDeviceInfo(self):
        for dev in self.devices:
            for name,val in dev:
                print( '%s = %s' % ( name.prettyPrint(), val.prettyPrint() ) )
            print "----------------------------------------------------"

    def printToFile(self):
        output = open("data/device_info.txt",'r+')
        for dev in self.devices:
            for name,val in dev:
                output.write(str(name) + '\n' + str(val) + '\n' )
            output.write('\n--------------\n')

    def makeXml(self):
        devices = []
        xmlFile = open('data/xml/device_info.xml','r+')
        out = open('data/out','r+')
        for dev in self.devices:
            for name,val in dev:
                out.write(str(val)+'&&')
            out.write('\n')

        out.close()
        infile = open('data/out','r+')
        devList = infile.readlines()

        xml = etree.Element('xml')
        performanceData = []

        for dev in devList:
            performanceData = dev.split('&&')
            
            root = etree.Element("Device")
            devId = etree.Element('Id')
            devId.text = performanceData[0]
            root.append(devId)

            sysDescr = etree.Element(SYSDESCR)
            sysDescr.text = performanceData[1]
            root.append(sysDescr)

            sysLocation = etree.Element(SYSLOCATION)
            sysLocation.text = performanceData[2]
            root.append(sysLocation)

            freePorts = etree.Element(FREEPORTS)
            freePorts.text = performanceData[3]
            root.append(freePorts)

            usedPorts = etree.Element(USEDPORTS)
            usedPorts.text = performanceData[4]
            root.append(usedPorts)

            #net = etree.Element('net')
            netUp = etree.Element(NETUP)
            netUp.text = performanceData[5]
            root.append(netUp)

            netDown = etree.Element(NETDOWN)
            netDown.text = performanceData[6]
            root.append(netDown)

            #net.append(netUp)
            #net.append(netDown)
            #root.append(net)

            fanSpeed = etree.Element(FANSPEED)
            fanSpeed.text = performanceData[7]
            root.append(fanSpeed)
            
            voltage = etree.Element(VOLTAGE)
            voltage.text = performanceData[8]
            root.append(voltage)

            temp = etree.Element(TEMP)
            temp.text = performanceData[9]
            root.append(temp)

            bandLoad = etree.Element(BANDLOAD)
            bandLoad.text = performanceData[10]
            root.append(bandLoad)

            xml.append(root)

            #print etree.tostring(root, pretty_print=True)
        xmlFile.write(etree.tostring(xml,pretty_print=True))

        #print performanceData

    def getDevicePorts(self):
        infile = open('src/devices.txt','r')

        data = infile.readline()

        ports = []
        ports = re.findall('\d+',data)
        self.ports = ports


'''--------------------------debug zone-------------------------'''
nm = NetworkManager('192.168.111.138')
#nm.getDeviceInfo()
#nm.printToFile()
