import subprocess

subprocess.call('/usr/lib/oracle/11.2/client64/bin/sqlldr orcdb/passw0rd@//192.168.111.138/orcl control=employe1.ctl', shell=True)
