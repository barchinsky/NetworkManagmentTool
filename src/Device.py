#! /usr/bin/env python

class Device:
    def __init__(self,_devId,_name,_location,_freePorts="",_usedPorts="",_netUp="",_netDown="",_fanSpeed="",_voltage="",_temp="",_bandwidthload=""):
        self.name = _name
        self.location = _location
        self.uptime = _uptime
        self.temp = _temp
        self.bandwithload = _bandwidthload
        self.devId = _devId
        self.freePorts = _freePorts
    
    def getAttr(self):
        return [self.name, self.location, self.uptime,self.temp, self.bandwithload]
