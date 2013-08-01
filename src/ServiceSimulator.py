#!/usr/bin/env python

import time
import random

class ServiceSimulator:
    def __init__(self):
        pass

    def start(self):
        pass
    
    def generateVoIP(self):
        voip_file = open("voip.csv","a+")
        sep = ","

        user_id = "user id"
        ts = str(time.time())
        delay = str(random.uniform(0.1,10)) 
        sip1 = "user_1_id" 
        sip2 = "user_2_id" 
        codec = "codec_type" 
        echo = str(random.uniform(0.5,10))
        pack_loss = str(random.randint(0,100))
        ts_start = ts
        ts_end = str( (float(ts_start) + random.uniform(10,500)) )
        
        voip_file.write(user_id+sep+sip1+sep+sip2+sep+delay+sep+echo+sep+codec+sep+pack_loss+sep+ts+sep+ts_start+sep+ts_end+'\n')
        voip_file.close()

    def generateIPTV(self):
        iptv_file = open("iptv.csv","a+")
        sep = ","
 
        user_id = "user id"
        ts = str(time.time())
        chanel = str(random.uniform(10000,20000))
        stb_id = "some_stb_id"
        prev_chanel = str(random.uniform(10000,20000))
        payment = str(random.randint(0,1))
        chan_spec = "some_cahnel_specification"
        parent = str(random.randint(0,1))
        bandwidth = str(random.randint(0,100))
        codec = "codec_type"

        iptv_file.write(user_id+sep+chanel+sep+stb_id+sep+prev_chanel+sep+payment+sep+chan_spec+sep+parent+sep+bandwidth+sep+codec+'\n')
        iptv_file.close()

    def generateBroadband(self):
        bb_file = open("bb.csv",'a+')
        sep = ","

        customer_info = "customer info"
        ts = str(time.time())
        delay = str(random.uniform(0,10))
        pack_loss = str(random.randint(0,150))
        up_speed = str(random.uniform(0,10000))
        down_speed = str(random.uniform(0,10000))
        ip = "ip address"
        mac = "mac address"
        user_id = "user id"
        client_agent = "client type"

        bb_file.write(user_id+sep+ip+sep+mac+sep+up_speed+sep+down_speed+sep+delay+sep+pack_loss+sep+customer_info+sep+client_agent+sep+ts+'\n')
        bb_file.close()


obj = ServiceSimulator()

while(True):
    obj.generateVoIP()
    obj.generateIPTV()
    obj.generateBroadband()
    time.sleep(5)
