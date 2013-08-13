#!/usr/bin/env python

import ConfigParser
import os

class ConfigManager():
	def __init__(self):
		self.config = ConfigParser.RawConfigParser()
		self.config.read(self.getConfFilePath())

	def getConfFilePath(self):
		if os.path.exists('../conf/'):
			return '../conf/configs.cfg'
		else:
			return 'conf/configs.cfg' 

	def CreateConfFile(self):
		#create config file
		self.config.add_section('logging')
		#self.config.set('logging', 'log_lvl', '/data/xml/device_info.xml')
		#self.config.set('logging', 'format', '')
		self.config.set('logging', 'insert_log', 'data/insert.log')
		self.config.set('logging', 'trap_log', 'data/trap.log')

		self.config.add_section('trap')
		self.config.set('trap', 'ip', "192.168.111.124")
		self.config.set('trap', 'trap_list', 'data/traps.txt')
		self.config.set('trap', 'connection', 'orcdb/passw0rd@192.168.111.138/orcl')

		self.config.add_section('network_maneger')
		self.config.set('network_maneger', 'output_file', 'data/device_info.txt')
		self.config.set('network_maneger', 'xml_file', 'data/xml/device_info.xml')
		self.config.set('network_maneger', 'device_list_file', 'src/devices.txt')
		self.config.set('network_maneger', 'snmp_ip', '192.168.111.138') 

		self.config.add_section('device')
		#self.config.set('device', 'devices', '~/Documents/vxsnmpsimulator-1.3.6/device/cisco/')
		#self.config.set('device', 'conf_file', '../conf/')
		self.config.set('device', 'inventory_date', '/home/Den/ftp/')

		self.config.add_section('service')
		self.config.set('service', 'iptv', '../data/iptv.csv')
		self.config.set('service', 'voip', '../data/voip.csv')
		self.config.set('service', 'bb', '../data/bb.csv')


		with open(self.getConfFilePath(), 'wb') as configfile:

			self.config.write(configfile)

	def PrintConfFile(self):
		self.sections = self.config.sections()
		for section in self.sections:
			print '-----------------------------------------------------------------------'
			print 'Section: ' + section
			items = self.config.items(section)
			for item in items:
				print item 
		print '-----------------------------------------------------------------------'
	
	def getLogFormat(self):
		return self.config.get('logging', 'format')

	#get file insert.log
	def getInsertLog(self):
		return self.config.get('logging', 'insert_log')

	#get file trap.log
	def getTrapLog(self):
		return self.config.get('logging', 'trap_log')

	#get ip for trap manager
	def getTrapIp(self):
		return self.config.get('trap', 'ip')

	#get trap list
	def getTrapList(self):
		return self.config.get('trap', 'trap_list')

	#database connection
	def getDBConnection(self):
		return self.config.get('trap', 'connection')

	#path to file device.txt
	def getOutputFile(self):
		return self.config.get('network_maneger', 'output_file')

	#path to file device.xml
	def getDeviceInfoFile(self):
		return self.config.get('network_maneger', 'xml_file')

	#path to file devices_list
	def getDevicesFile(self):
		return self.config.get('network_maneger', 'device_list_file')

	#simulator snmp, get ip server
	def getSnmpIp(self):
		return self.config.get('network_maneger', 'snmp_ip')

	#path to devices for snmp simulator
	def getDevicePath(self):
		return self.config.get('device', 'devices')

	#path to file inventory.txt
	def getInventory(self):
		return self.config.get('device', 'inventory_date')

	#path to configuration file
	def getConfFile(self):
		return self.config.get('device', 'conf_file')

	#path to iptv.csv file
	def getIptvFile(self):
		return self.config.get('service', 'iptv')


	#path to voip.csv file
	def getVoipFile(self):
		return self.config.get('service', 'voip')


	#path to bb.csv file
	def getBbFile(self):
		return self.config.get('service', 'bb')

