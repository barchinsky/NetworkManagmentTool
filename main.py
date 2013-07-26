#!/usr/bin/env python

import sys
from NetworkManager import NetworkManager
sys.path.append("./src/")
from CONST import *

def menu():
    options = {1:"network inventory info.",2:" all devices info.",3:"device info.",4:"device description."}
    print "------------------------------"
    print "MENU"
    print "------------------------------"
    for key in options.keys():
        print  str(key) + ")Print " + options[key]
    choise = raw_input("Enter: ")

    return int(choise)

if __name__ == "__main__":
    #print "Starting network manager..."
    try:
        print "Starting network manager..."
        nm = NetworkManager('192.168.111.138')
        print "Network manager started."
        
        while(1):
            option = menu()
            if option == 1:
                nm.printInventory()
            elif option == 2:
                nm.printDeviceInfo()
            elif option == 3:
                info_type = raw_input("Enter information type: ")
                device_id = raw_input("Enter device_id: ")
                nm.printDataForDevice(info_type.rstrip(),device_id.rstrip())
            else:
                exit()
    except Exception,exception:
        print exception

