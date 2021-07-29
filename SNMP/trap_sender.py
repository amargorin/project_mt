from pysnmp.hlapi import *

iterator = sendNotification(
    SnmpEngine(),
    CommunityData('public', mpModel=1), #версия протокола mpModel  0=v1, 1=v2
    UdpTransportTarget(('localhost', 162)),
    ContextData(),
    'trap',
    NotificationType(
        ObjectIdentity('1.3.6.1.4.1.2789.2005.1')
    ).addVarBinds(
        ('1.3.6.1.4.1.2789.2005.1.0', Integer32(61))
    ).loadMibs(
        'SNMPv2-MIB'
    )
)

errorIndication, errorStatus, errorIndex, varBinds = next(iterator)

if errorIndication:
    print(errorIndication)
