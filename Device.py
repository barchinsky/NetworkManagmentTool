#! /usr/bin/env python

class Device:
    def __init__(self,_name,_location,_uptime="",_temp="",_bandwidthload=""):
        self.name = _name
        self.location = _location
        self.uptime = _uptime
        self.temp = _temp
        self.bandwithload = _bandwidthload
    
    def getAttr(self):
        return [self.name, self.location, self.uptime,self.temp, self.bandwithload]
