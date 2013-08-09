load data
	infile '../data/bb.csv'
	append into table BROADBAND
	fields terminated by ","
	( id, ip, mac, streamup, streamdown, delay, packet_loss, castom_info, user_agent, timestamp)


