#!/usr/bin/env python
import subprocess

subprocess.call('/usr/lib/oracle/11.2/client64/bin/sqlldr orcdb/passw0rd@//192.168.111.138/orcl control=/home/max/TF/NetworkManagmentTool/src/loadTV.ctl', shell=True)
f = open('/home/max/TF/NetworkManagmentTool/data/iptv.csv','w')
f.write('')
f.close()

subprocess.call('/usr/lib/oracle/11.2/client64/bin/sqlldr orcdb/passw0rd@//192.168.111.138/orcl control=/home/max/TF/NetworkManagmentTool/src/loadVO.ctl', shell=True)

f = open('/home/max/TF/NetworkManagmentTool/data/voip.csv','w')
f.write('')
f.close()

subprocess.call('/usr/lib/oracle/11.2/client64/bin/sqlldr orcdb/passw0rd@//192.168.111.138/orcl control=/home/max/TF/NetworkManagmentTool/src/loadBB.ctl', shell=True)

f = open('/home/max/TF/NetworkManagmentTool/data/bb.csv','w')
f.write('')
f.close()
