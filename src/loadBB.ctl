load data
	infile '/home/max/TF/NetworkManagmentTool/data/bb.csv'
	append into table BROADBAND
	fields terminated by ","
	( id, ip, mac, streamup, streamdown, delay, packet_loss, castom_info, user_agent, timestamp)


