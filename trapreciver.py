from pysnmp.carrier.asynsock.dispatch import AsynsockDispatcher
from pysnmp.carrier.asynsock.dgram import udp, udp6
from pyasn1.codec.ber import decoder
from pysnmp.proto import api
import cx_Oracle
import logging
import sys
sys.path.append("./src")

from LogManager import *
from ConfigManager import ConfigManager


cm = ConfigManager()
print cm.getTrapIp()
def GetTrapData(varBinds):
    
    for val in varBinds:
      
        tmp=val.prettyPrint()
        if tmp.find("string-value")!=-1:
            i = tmp.rfind("string-value")
            l = len("string-value")
            index = l+i+1
            data = tmp[index:-1]
            Inf = data.split('|')
 
            try:
                cur.callproc("add_trap_info",[Inf[0],Inf[1],float(Inf[2].rstrip())])
                logger.info('insert trap in db')
                con.commit()
            except Exception:
                print 'cant insert.look log file'
                logger.error('not call stored procedure')

            #con.commit()
           
            
            #cur.execute("select * from SYSTEM.TRAP")
            #print cur.fetchall()

def cbFun(transportDispatcher, transportDomain, transportAddress, wholeMsg):
    
    while wholeMsg:
        msgVer = int(api.decodeMessageVersion(wholeMsg))
        if msgVer in api.protoModules:
            pMod = api.protoModules[msgVer]
        else:
            print('Unsupported SNMP version %s' % msgVer)
            return
        reqMsg, wholeMsg = decoder.decode(
            wholeMsg, asn1Spec=pMod.Message(),
            )
        print('Notification message from %s:%s: ' % (
            transportDomain, transportAddress
            )
        )
        reqPDU = pMod.apiMessage.getPDU(reqMsg)
        if reqPDU.isSameTypeWith(pMod.TrapPDU()):
            varBinds = pMod.apiPDU.getVarBindList(reqPDU)
            #print('Var-binds:')
    GetTrapData(varBinds)

    return wholeMsg

logger = logging.getLogger('trap')
hdlr = logging.FileHandler(cm.getTrapLog())
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr) 
logger.setLevel(logging.WARNING)
logger.setLevel(logging.INFO)

con = cx_Oracle.connect(cm.getDBConnection())

cur = con.cursor()
logger.info('connect to db')

transportDispatcher = AsynsockDispatcher()

transportDispatcher.registerRecvCbFun(cbFun)

# UDP/IPv4
transportDispatcher.registerTransport(
    udp.domainName, udp.UdpSocketTransport().openServerMode(("192.168.111.124", 5050))
)

transportDispatcher.jobStarted(1)

try:
    # Dispatcher will never finish as job#1 never reaches zero
    transportDispatcher.runDispatcher()
except:
    transportDispatcher.closeDispatcher()
    raise
cur.close() 
con.close()
logger.info('disconnect db') 
