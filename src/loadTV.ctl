load data
	infile '/home/max/TF/NetworkManagmentTool/data/iptv.csv'
	append into table IPTV
	fields terminated by ","
	( id, channel, idstb, channel_prev, payment,ganre,parent_control, bandwidth,codec,timestamp)
