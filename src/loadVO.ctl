load data
	infile '/home/max/TF/NetworkManagmentTool/data/voip.csv'
	append into table VOIP
	fields terminated by ","
	( id, sip_1, sip_2, delay,echo, codec, packet_loss,timestamp,timestamp_start,timestamp_end)
