import subprocess

subprocess.call('/usr/lib/oracle/11.2/client64/bin/sqlldr orcdb/passw0rd@//192.168.111.138/orcl control=loadTV.ctl', shell=True)
f = open('../data/iptv.csv','w')
f.write('')
f.close()

subprocess.call('/usr/lib/oracle/11.2/client64/bin/sqlldr orcdb/passw0rd@//192.168.111.138/orcl control=loadVO.ctl', shell=True)

f = open('../data/voip.csv','w')
f.write('')
f.close()

subprocess.call('/usr/lib/oracle/11.2/client64/bin/sqlldr orcdb/passw0rd@//192.168.111.138/orcl control=loadBB.ctl', shell=True)

f = open('../data/bb.csv','w')
f.write('')
f.close()
