#!/usr/bin/env python
# Generate device data for vxsimulator
import random

class DeviceManager:
    def __init__(self):
        self.oids = []
        self.getOID()

    def generate(self,dev_type,number,silly):
        if dev_type.rstrip() == 'router':
            self.generate_router(silly)
        elif dev_type.rstrip() == 'bras':
            self.generate_bras()
        elif dev_type.rstrip() == 'dslam':
            self.generate_dslam()

    def generate_router(self,silly):
        f = open(silly+'.txt','w')
        data = self.generateData(silly)
        
        for el in xrange(len(self.oids)):
            f.write(self.oids[el] + ' = ' + str(data[el]) + '\n')
        f.close()

    def getOID(self):
        with open("oid",'r') as f:
            for line in f:
                self.oids.append(line.rstrip())

    def generateData(self,_silly):

        silly = "STRING: " + _silly
        sysDescr = "STRING: Some name"
        buf1 = "OID: .1.3.6.1.4.1.9.1.620" 
        buf2 = "Timeticks: (898734042) 104 days, 0:29:00.42" 
        buf3 = "STRING: "
        buf4 = "STRING: cisco-router-1800-//^int.unq()^//" 
        buf5 = "STRING: cisco - Cisco 600 Router" 
        buf6 = "STRING: Ruoter"
        freePorts = "STRING: " + str(random.randint(0,40))
        usedPorts = "STRING: " + str(40)
        netUp = "STRING: " + str(random.randint(0,100000000))
        netDown = "STRING: "  +str(random.randint(0,100000000))
        fanSpeed = "STRING: " + str(random.randint(200,1000))
        voltage = "STRING: " +str(random.randint(0,15))
        temp = "STRING: " + str(random.randint(40,80))
        bandLoad = "STRING: " + str(random.randint(0,100))

        return (sysDescr,buf1,buf2,buf3,buf4,buf5,buf6,silly,freePorts,usedPorts,netUp,netDown,fanSpeed,voltage,temp,bandLoad)

ob = DeviceManager()
ob.generate('router',1,"UA5120012")
