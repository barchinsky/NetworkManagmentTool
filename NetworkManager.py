#! /usr/bin/env python

from pysnmp.entity.rfc3413.oneliner import cmdgen
import xml.etree.ElementTree as ET
#import DeviceActivi
from lxml import etree

class NetworkManager:
    def __init__(self,_ip,_ports):
        self.ip = _ip
        self.ports = _ports
        self.cmdGen = cmdgen.CommandGenerator()
        self.devices = []

    def getDeviceInfo(self):
        for port in self.ports:
            errorIndication, errorStatus, errorIndex, self.varBinds = self.cmdGen.getCmd(
            cmdgen.CommunityData('public'),
            cmdgen.UdpTransportTarget((self.ip, port)),
            '.1.3.6.1.2.1.3.6.0',
            '.1.3.6.1.2.1.1.1.0',
            '.1.3.6.1.2.1.5.8.0',
            '.1.3.6.1.2.1.2.1.0',
            '.1.3.6.1.2.1.2.2.0',
            '.1.3.6.1.2.1.4.1.0',
            '.1.3.6.1.2.1.4.2.0',
            '.1.3.6.1.2.1.3.7.0',
            '.1.3.6.1.2.1.3.1.0',
            '.1.3.6.1.2.1.3.1.0',
            '.1.3.6.1.2.1.4.3.0',
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
        output = open("device_info.txt",'r+')
        for dev in self.devices:
            for name,val in dev:
                output.write(str(name) + '\n' + str(val) + '\n' )
            output.write('\n--------------\n')

    def makeXml(self):
        devices = []
        xmlFile = open('device_info.xml','r+')
        out = open('out','r+')
        for dev in self.devices:
            for name,val in dev:
                out.write(str(val)+'&&')
            out.write('\n')

        out.close()
        infile = open('out','r+')
        devList = infile.readlines()

        performanceData = []
        for dev in devList:
            performanceData = dev.split('&&')
            
            root = etree.Element("Device")
            devId = etree.Element('Id')
            devId.text = performanceData[0]
            root.append(devId)

            sysDescr = etree.Element('sysDescr')
            sysDescr.text = performanceData[1]
            root.append(sysDescr)

            sysLocation = etree.Element('sysLocation')
            sysLocation.text = performanceData[2]
            root.append(sysLocation)

            freePorts = etree.Element('freePorts')
            freePorts.text = performanceData[3]
            root.append(freePorts)

            usedPorts = etree.Element('usedPorts')
            usedPorts.text = performanceData[4]
            root.append(usedPorts)

            net = etree.Element('net')
            netUp = etree.Element('netUp')
            netUp.text = performanceData[5]

            netDown = etree.Element('netDown')
            netDown.text = performanceData[6]

            net.append(netUp)
            net.append(netDown)
            root.append(net)

            fanSpeed = etree.Element('fanSpeed')
            fanSpeed.text = performanceData[7]
            root.append(fanSpeed)
            
            voltage = etree.Element('voltage')
            voltage.text = performanceData[8]
            root.append(voltage)

            temp = etree.Element('temp')
            temp.text = performanceData[9]
            root.append(temp)

            bandLoad = etree.Element('bandLoad')
            bandLoad.text = performanceData[10]
            root.append(bandLoad)
            
            #print etree.tostring(root, pretty_print=True)
            xmlFile.write(etree.tostring(root,pretty_print=True))

        #print performanceData

'''--------------------------debug zone-------------------------'''
nm = NetworkManager('192.168.111.138',(5323,5324,5324))
nm.getDeviceInfo()
#nm.printToFile()
