#!/usr/bin/env python

import time
import random
#import os.path
import os
import sys
import cx_Oracle
from ConfigManager import ConfigManager

class ServiceSimulator:
    def __init__(self):
        cm = ConfigManager()
        self.voip_path = cm.getVoipFile()
        self.bb_path = cm.getBbFile()
        self.iptv_path = cm.getIptvFile()
        self.con = cx_Oracle.connect('orcdb/passw0rd@192.168.111.138/orcl')
        self.cur = self.con.cursor()

        self.sep = ','

    def start(self):
        pass
    
    def generate_voip(self):
        #voip_file = open(os.path.dirname(__file__)+self.voip_path,"a+")
        voip_file = open(self.voip_path,'a+')

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
        
        voip_file.write(user_id+self.sep+sip1+self.sep+sip2+self.sep+delay+self.sep+echo+self.sep+codec+self.sep+pack_loss+self.sep+ts+self.sep+ts_start+self.sep+ts_end+'\n')
        voip_file.close()

    def generate_iptv(self):
        #iptv_file = open(os.path.dirname(__file__)+self.iptv_path,"a+")
        iptv_file = open(self.iptv_path,'a+')
 
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

        iptv_file.write(user_id+self.sep+chanel+self.sep+stb_id+self.sep+prev_chanel+self.sep+payment+self.sep+chan_spec+self.sep+parent+self.sep+bandwidth+self.sep+codec+self.sep+ts+'\n')
        iptv_file.close()

    def generate_broadband(self):
        #bb_file = open(os.path.dirname(__file__)+self.bb_path,'a+')
        bb_file = open(self.bb_path,'a+')

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

        bb_file.write(user_id+self.sep+ip+self.sep+mac+self.sep+up_speed+self.sep+down_speed+self.sep+delay+self.sep+pack_loss+self.sep+customer_info+self.sep+client_agent+self.sep+ts+'\n')
        bb_file.close()

    def generate(self):
        self.generate_voip()
        self.generate_iptv()
        self.generate_broadband()

obj = ServiceSimulator()
indicator = "Simulator is working."
print indicator
records = 0 
while(True):
    #print "Record:",records
    obj.generate()
    time.sleep(1)
    records += 1
