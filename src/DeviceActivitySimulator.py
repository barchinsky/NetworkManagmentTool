#! /usr/bin/env python

import re

class DeviceActivityEmulator:
    def __init__(self,_path=""):
        self.path = _path

    def emulate(self):
        f = open("devices/cisco/cisco_router_1.1.txt",'r+')

        data = f.readlines()

        for line in data:
            #print line
            pass

        self.getDeviceData(data)

    def parse(self,data):
        for line in data:
            pass

    def getDictionary(self):
        dictionary = {}
        with open("mib",'r+') as f:
            for line in f:
                (val,key) = line.split('-')
                dictionary[str(key.rstrip())] = str(val)
        return dictionary

    def getDeviceData(self,data):
        dictionary = self.getDictionary()
        deviceDictionary = {} #keep device performance
        for line in data:
            for key in dictionary.keys():
                if dictionary[key] in line:
                    #printprint line.rstrip().split(':')
                    (k,v) = line.rstrip().split(':')
                    deviceDictionary[key] = re.findall('\d+',v)

        print deviceDictionary


emulator = DeviceActivityEmulator()
emulator.emulate()
#emulator.getDictionary()

