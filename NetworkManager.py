#! /usr/bin/env python

from pysnmp.entity.rfc3413.oneliner import cmdgen

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
            cmdgen.MibVariable('SNMPv2-MIB', 'sysDescr', 0),
            cmdgen.MibVariable('SNMPv2-MIB', 'sysUpTime', 0),
            lookupNames=True, lookupValues=True)

            if errorIndication:
                print (errorIndication,port)
            elif errorStatus:
                print (errorStatus,port)
            else:
                self.devices.append(self.varBinds)

        self.printDeviceInfo()

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

nm = NetworkManager('192.168.111.138',(5322,162,163))
nm.getDeviceInfo()
nm.printToFile()
