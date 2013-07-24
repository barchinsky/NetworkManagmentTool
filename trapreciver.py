from pysnmp.carrier.asynsock.dispatch import AsynsockDispatcher
from pysnmp.carrier.asynsock.dgram import udp, udp6
from pyasn1.codec.ber import decoder
from pysnmp.proto import api
import cx_Oracle


def GetTrapData(varBinds):
    con = cx_Oracle.connect('orcdb/passw0rd@192.168.111.138/orcl')

    cur = con.cursor()
 
    for oid, val in varBinds:
      
        tmp=val.prettyPrint()
       
        if tmp.find("string-value")!=-1:
            i = tmp.rfind("string-value")
            l = len("string-value")
            index = l+i+1
            data = tmp[index:-1]
            #print data
            Inf = data.split('|')
            print Inf[0]
            cur.callproc("SYSTEM.add_trap_info",[Inf[0],Inf[1],float(Inf[2].rstrip())])
            con.commit()
           
            
            cur.execute("select * from SYSTEM.TRAP")
            print cur.fetchall()
 
    cur.close() 
    con.close()
 

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
            print('Var-binds:')
            GetTrapData(varBinds)

    return wholeMsg

transportDispatcher = AsynsockDispatcher()

transportDispatcher.registerRecvCbFun(cbFun)

# UDP/IPv4
transportDispatcher.registerTransport(
    udp.domainName, udp.UdpSocketTransport().openServerMode(('192.168.111.130', 5050))
)

transportDispatcher.jobStarted(1)

try:
    # Dispatcher will never finish as job#1 never reaches zero
    transportDispatcher.runDispatcher()
except:
    transportDispatcher.closeDispatcher()
    raise
