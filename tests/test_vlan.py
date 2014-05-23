import pytest
from pynetworking import Device
from time import sleep
from paramiko.rsakey import RSAKey

def setup_dut(dut):
    dut.reset()
    dut.add_cmd({'cmd':'show version',        'state':-1, 'action': 'PRINT','args':["""
AlliedWare Plus (TM) 5.4.2 09/25/13 12:57:26

Build name : x600-5.4.2-3.14.rel
Build date : Wed Sep 25 12:57:26 NZST 2013
Build type : RELEASE
    """]})
#     dut.add_cmd({'cmd':'show running-config', 'state':-1, 'action': 'PRINT','args':["""
# !
# interface port1.0.1-1.0.50
#  switchport
#  switchport mode access
# !
# vlan database
#  vlan 10 name "marketing vlan"
#  vlan 10 state enable
#  vlan 7 name admin state enable
#  vlan 8-100 mtu 1200
#  vlan 6,7 mtu 1000
# !
# end
#     """]})
#     dut.add_cmd({'cmd': 'show vlan all',                        'state':-1, 'action':'PRINT','args':["""
# VLAN ID  Name            Type    State   Member ports
#                                          (u)-Untagged, (t)-Tagged
# ======= ================ ======= ======= ====================================
# 1       default          STATIC  ACTIVE  port1.0.1(u) port1.0.2(u) port1.0.3(u)
#                                          port1.0.4(u) port1.0.5(u) port1.0.6(u)
#                                          port1.0.7(u) port1.0.8(u) port1.0.9(u)
#                                          port1.0.10(u) port1.0.11(u)
#                                          port1.0.12(t) port1.0.13(u)
#                                          port1.0.14(u) port1.0.15(u)
#                                          port1.0.16(u) port1.0.17(u)
#                                          port1.0.18(u) port1.0.19(u)
#                                          port1.0.20(t) port1.0.21(u)
#                                          port1.0.22(u) port1.0.23(u)
#                                          port1.0.24(u) port1.0.25(u)
#                                          port1.0.26(u) port1.0.27(u)
#                                          port1.0.28(u) port1.0.29(u)
#                                          port1.0.31(u)
#                                          port1.0.32(u) port1.0.33(u)
#                                          port1.0.34(u) port1.0.35(u)
#                                          port1.0.36(u) port1.0.37(u)
#                                          port1.0.38(u) port1.0.39(u)
#                                          port1.0.40(u) port1.0.41(u)
#                                          port1.0.44(u) port1.0.45(u)
#                                          port1.0.46(u) port1.0.47(u)
#                                          port1.0.48(u) port1.0.49(u)
#                                          port1.0.50(u)
# 7       VLAN0007         STATIC  ACTIVE  port1.0.28(t) port1.0.29(u)
# 20      "this is a long vlan name"
#                          STATIC  ACTIVE  port1.0.42(u) port1.0.43(t)
# 10      VLAN0010         STATIC  ACTIVE  port1.0.28(t) port1.0.29(u)
#                                          port1.0.19(t) port1.0.30(t)
#     """]})


def test_get_vlan(dut, log_level):
    setup_dut(dut)
    dut.add_cmd({'cmd':'show running-config', 'state':0, 'action': 'PRINT','args':["""
!
interface port1.0.1-1.0.50
switchport
switchport mode access
!
vlan database
vlan 10 name "marketing vlan"
vlan 10 state enable
vlan 7 name admin state enable
vlan 8-100 mtu 1200
vlan 6,7 mtu 1000
!
end
    """]})
    dut.add_cmd({'cmd': 'show vlan all'    , 'state':0, 'action': 'PRINT','args':["""
VLAN ID  Name            Type    State   Member ports
                                         (u)-Untagged, (t)-Tagged
======= ================ ======= ======= ====================================
1       default          STATIC  ACTIVE  port1.0.1(u) port1.0.2(u) port1.0.3(u)
                                         port1.0.4(u) port1.0.5(u) port1.0.6(u)
                                         port1.0.7(u) port1.0.8(u) port1.0.9(u)
                                         port1.0.10(u) port1.0.11(u)
                                         port1.0.12(t) port1.0.13(u)
                                         port1.0.14(u) port1.0.15(u)
                                         port1.0.16(u) port1.0.17(u)
                                         port1.0.18(u) port1.0.19(u)
                                         port1.0.20(t) port1.0.21(u)
                                         port1.0.22(u) port1.0.23(u)
                                         port1.0.24(u) port1.0.25(u)
                                         port1.0.26(u) port1.0.27(u)
                                         port1.0.28(u) port1.0.29(u)
                                         port1.0.31(u)
                                         port1.0.32(u) port1.0.33(u)
                                         port1.0.34(u) port1.0.35(u)
                                         port1.0.36(u) port1.0.37(u)
                                         port1.0.38(u) port1.0.39(u)
                                         port1.0.40(u) port1.0.41(u)
                                         port1.0.44(u) port1.0.45(u)
                                         port1.0.46(u) port1.0.47(u)
                                         port1.0.48(u) port1.0.49(u)
                                         port1.0.50(u)
7       VLAN0007         STATIC  ACTIVE  port1.0.28(t) port1.0.29(u)
20      "this is a long vlan name"
                         STATIC  ACTIVE  port1.0.42(u) port1.0.43(t)
10      VLAN0010         STATIC  ACTIVE  port1.0.28(t) port1.0.29(u)
                                         port1.0.19(t) port1.0.30(t)
    """]})
    d=Device(host=dut.host,port=dut.port,protocol=dut.protocol, log_level=log_level)
    d.open()
    if dut.mode == 'emulated':
        assert d.vlan[1]['tagged'] == ("1.0.12", "1.0.20")
        assert d.vlan[1]['untagged'] == ("1.0.1", "1.0.2", "1.0.3", "1.0.4", "1.0.5", "1.0.6", "1.0.7", "1.0.8", "1.0.9", "1.0.10",
                                         "1.0.11",           "1.0.13", "1.0.14", "1.0.15", "1.0.16", "1.0.17", "1.0.18", "1.0.19",
                                         "1.0.21", "1.0.22", "1.0.23", "1.0.24", "1.0.25", "1.0.26", "1.0.27", "1.0.28", "1.0.29",
                                         "1.0.31", "1.0.32", "1.0.33", "1.0.34", "1.0.35", "1.0.36", "1.0.37", "1.0.38", "1.0.39", "1.0.40",
                                         "1.0.41",                     "1.0.44", "1.0.45", "1.0.46", "1.0.47", "1.0.48", "1.0.49", "1.0.50")
        assert "1.0.28" in d.vlan[7]['tagged']
        assert "1.0.29" in d.vlan[7]['untagged']
        assert d.vlan[7]['state'] == 'enable'
        assert d.vlan[7]['name'] == 'admin'
        assert d.vlan[7]['mtu'] == 1000
        assert d.vlan[10]['tagged'] == ("1.0.28", "1.0.19", "1.0.30")
        assert "1.0.29" in d.vlan[10]['untagged']
        assert d.vlan[10]['state'] == 'enable'
        assert d.vlan[10]['name'] == 'marketing vlan'
        assert d.vlan[10]['mtu'] == 1200
        assert "1.0.43" in d.vlan[20]['tagged']
        assert "1.0.42" in d.vlan[20]['untagged']
        assert d.vlan[20]['name'] == 'this is a long vlan name'
    else:
        assert d.vlan[1]['tagged'] == ()
        assert d.vlan[1]['untagged'] != ()
        assert d.vlan[1]['name'] == 'default'
        str(d.vlan)
    with pytest.raises(KeyError) as excinfo:
        d.vlan[1111]
        assert 'vlan id 1111 does not exist' in excinfo.value
    d.close()


def test_create_vlan_1(dut, log_level):
    setup_dut(dut)
    dut.add_cmd({'cmd':'show running-config', 'state':0, 'action': 'PRINT','args':["""
!
interface port1.0.1-1.0.50
switchport
switchport mode access
!
vlan database
vlan 7 name admin state enable
vlan 8-100 mtu 1200
vlan 6,7 mtu 1000
!
end
    """]})
    dut.add_cmd({'cmd': 'show vlan all'    , 'state':0, 'action': 'PRINT','args':["""
VLAN ID  Name            Type    State   Member ports
                                         (u)-Untagged, (t)-Tagged
======= ================ ======= ======= ====================================
1       default          STATIC  ACTIVE  port1.0.1(u) port1.0.2(u) port1.0.3(u)
                                         port1.0.4(u) port1.0.5(u) port1.0.6(u)
                                         port1.0.7(u) port1.0.8(u) port1.0.9(u)
                                         port1.0.10(u) port1.0.11(u)
                                         port1.0.12(t) port1.0.13(u)
                                         port1.0.14(u) port1.0.15(u)
                                         port1.0.16(u) port1.0.17(u)
                                         port1.0.18(u) port1.0.19(u)
                                         port1.0.20(t) port1.0.21(u)
                                         port1.0.22(u) port1.0.23(u)
                                         port1.0.24(u) port1.0.25(u)
                                         port1.0.26(u) port1.0.27(u)
                                         port1.0.28(u) port1.0.29(u)
                                         port1.0.31(u)
                                         port1.0.32(u) port1.0.33(u)
                                         port1.0.34(u) port1.0.35(u)
                                         port1.0.36(u) port1.0.37(u)
                                         port1.0.38(u) port1.0.39(u)
                                         port1.0.40(u) port1.0.41(u)
                                         port1.0.44(u) port1.0.45(u)
                                         port1.0.46(u) port1.0.47(u)
                                         port1.0.48(u) port1.0.49(u)
                                         port1.0.50(u)
7       VLAN0007         STATIC  ACTIVE  port1.0.28(t) port1.0.29(u)
    """]})
    dut.add_cmd({'cmd': 'vlan database'              , 'state':0, 'action':'SET_PROMPT','args':['(config-vlan)#']})
    dut.add_cmd({'cmd': 'vlan database'              , 'state':0, 'action':'SET_STATE','args':[1]})
    dut.add_cmd({'cmd': 'vlan 20 name admin'         , 'state':1, 'action':'SET_STATE','args':[2]})
    dut.add_cmd({'cmd': 'vlan 20 mtu 1300'           , 'state':2, 'action':'SET_STATE','args':[3]})
    dut.add_cmd({'cmd': 'show running-config'        , 'state':3, 'action':'PRINT'    ,'args':["""
!
vlan database
 vlan 20 name admin state enable mtu 1300
! 
    """]})
    dut.add_cmd({'cmd': 'show vlan all'              , 'state':3, 'action': 'PRINT','args':["""
VLAN ID  Name            Type    State   Member ports
                                         (u)-Untagged, (t)-Tagged
======= ================ ======= ======= ====================================
1       default          STATIC  ACTIVE  port1.0.1(u) port1.0.2(u) port1.0.3(u)
                                         port1.0.4(u) port1.0.5(u) port1.0.6(u)
                                         port1.0.7(u) port1.0.8(u) port1.0.9(u)
                                         port1.0.10(u) port1.0.11(u)
                                         port1.0.12(t) port1.0.13(u)
                                         port1.0.14(u) port1.0.15(u)
                                         port1.0.16(u) port1.0.17(u)
                                         port1.0.18(u) port1.0.19(u)
                                         port1.0.20(t) port1.0.21(u)
                                         port1.0.22(u) port1.0.23(u)
                                         port1.0.24(u) port1.0.25(u)
                                         port1.0.26(u) port1.0.27(u)
                                         port1.0.28(u) port1.0.29(u)
                                         port1.0.31(u)
                                         port1.0.32(u) port1.0.33(u)
                                         port1.0.34(u) port1.0.35(u)
                                         port1.0.36(u) port1.0.37(u)
                                         port1.0.38(u) port1.0.39(u)
                                         port1.0.40(u) port1.0.41(u)
                                         port1.0.44(u) port1.0.45(u)
                                         port1.0.46(u) port1.0.47(u)
                                         port1.0.48(u) port1.0.49(u)
                                         port1.0.50(u)
7       VLAN0007         STATIC  ACTIVE  port1.0.28(t) port1.0.29(u)
10      VLAN0010         STATIC  ACTIVE  port1.0.28(t) port1.0.29(u)
                                         port1.0.19(t) port1.0.30(t)
20      admin            STATIC  ACTIVE  port1.0.42(u) port1.0.43(t)
    """]})

    d=Device(host=dut.host,port=dut.port,protocol=dut.protocol, log_level=log_level)
    d.open()
    d.vlan.create(20, name='admin', mtu=1300)
    assert d.vlan[20]['state'] == 'enable'
    assert d.vlan[20]['name'] == 'admin'
    assert d.vlan[20]['mtu'] == 1300
    d.close()


def test_create_vlan_2(dut, log_level):
    setup_dut(dut)
    dut.add_cmd({'cmd':'show running-config', 'state':0, 'action': 'PRINT','args':["""
!
interface port1.0.1-1.0.50
switchport
switchport mode access
!
vlan database
vlan 7 name admin state enable
vlan 8-100 mtu 1200
vlan 6,7 mtu 1000
vlan 20 name admin state enable mtu 1300
!
end
    """]})
    dut.add_cmd({'cmd': 'show vlan all'              , 'state':0, 'action': 'PRINT','args':["""
VLAN ID  Name            Type    State   Member ports
                                         (u)-Untagged, (t)-Tagged
======= ================ ======= ======= ====================================
1       default          STATIC  ACTIVE  port1.0.1(u) port1.0.2(u) port1.0.3(u)
                                         port1.0.4(u) port1.0.5(u) port1.0.6(u)
                                         port1.0.7(u) port1.0.8(u) port1.0.9(u)
                                         port1.0.10(u) port1.0.11(u)
                                         port1.0.12(t) port1.0.13(u)
                                         port1.0.14(u) port1.0.15(u)
                                         port1.0.16(u) port1.0.17(u)
                                         port1.0.18(u) port1.0.19(u)
                                         port1.0.20(t) port1.0.21(u)
                                         port1.0.22(u) port1.0.23(u)
                                         port1.0.24(u) port1.0.25(u)
                                         port1.0.26(u) port1.0.27(u)
                                         port1.0.28(u) port1.0.29(u)
                                         port1.0.31(u)
                                         port1.0.32(u) port1.0.33(u)
                                         port1.0.34(u) port1.0.35(u)
                                         port1.0.36(u) port1.0.37(u)
                                         port1.0.38(u) port1.0.39(u)
                                         port1.0.40(u) port1.0.41(u)
                                         port1.0.44(u) port1.0.45(u)
                                         port1.0.46(u) port1.0.47(u)
                                         port1.0.48(u) port1.0.49(u)
                                         port1.0.50(u)
7       VLAN0007         STATIC  ACTIVE  port1.0.28(t) port1.0.29(u)
20      admin            STATIC  ACTIVE  port1.0.42(u) port1.0.43(t)
    """]})
    dut.add_cmd({'cmd': 'vlan database'                           , 'state':0, 'action':'SET_PROMPT','args':['(config-vlan)#']})
    dut.add_cmd({'cmd': 'vlan database'                           , 'state':0, 'action':'SET_STATE','args':[1]})
    dut.add_cmd({'cmd': 'vlan 10 name "this is a long vlan name"' , 'state':1, 'action':'SET_STATE','args':[2]})
    dut.add_cmd({'cmd': 'vlan 10 mtu 1200'                        , 'state':2, 'action':'SET_STATE','args':[3]})
    dut.add_cmd({'cmd': 'show running-config'                     , 'state':3, 'action':'PRINT'    ,'args':["""
!
vlan database
 vlan 10 name "this is a long vlan name" state enable mtu 1200
!
    """]})
    dut.add_cmd({'cmd': 'show vlan all'              , 'state':3, 'action': 'PRINT','args':["""
VLAN ID  Name            Type    State   Member ports
                                         (u)-Untagged, (t)-Tagged
======= ================ ======= ======= ====================================
1       default          STATIC  ACTIVE  port1.0.1(u) port1.0.2(u) port1.0.3(u)
                                         port1.0.4(u) port1.0.5(u) port1.0.6(u)
                                         port1.0.7(u) port1.0.8(u) port1.0.9(u)
                                         port1.0.10(u) port1.0.11(u)
                                         port1.0.12(t) port1.0.13(u)
                                         port1.0.14(u) port1.0.15(u)
                                         port1.0.16(u) port1.0.17(u)
                                         port1.0.18(u) port1.0.19(u)
                                         port1.0.20(t) port1.0.21(u)
                                         port1.0.22(u) port1.0.23(u)
                                         port1.0.24(u) port1.0.25(u)
                                         port1.0.26(u) port1.0.27(u)
                                         port1.0.28(u) port1.0.29(u)
                                         port1.0.31(u)
                                         port1.0.32(u) port1.0.33(u)
                                         port1.0.34(u) port1.0.35(u)
                                         port1.0.36(u) port1.0.37(u)
                                         port1.0.38(u) port1.0.39(u)
                                         port1.0.40(u) port1.0.41(u)
                                         port1.0.44(u) port1.0.45(u)
                                         port1.0.46(u) port1.0.47(u)
                                         port1.0.48(u) port1.0.49(u)
                                         port1.0.50(u)
7       VLAN0007         STATIC  ACTIVE  port1.0.28(t) port1.0.29(u)
10      "this is a long vlan name"
                         STATIC  ACTIVE  port1.0.42(u) port1.0.43(t)
20      admin            STATIC  ACTIVE  port1.0.42(u) port1.0.43(t)
    """]})
    d=Device(host=dut.host,port=dut.port,protocol=dut.protocol, log_level=log_level)
    d.open()
    d.vlan.create(10, name='this is a long vlan name', mtu=1200)
    assert d.vlan[10]['state'] == 'enable'
    assert d.vlan[10]['name'] == 'this is a long vlan name'
    assert d.vlan[10]['mtu'] == 1200
    with pytest.raises(KeyError) as excinfo:
        d.vlan.update(30,name='does not exist')
        assert '30 vlans do not exist' in excinfo.value
    with pytest.raises(ValueError):
        d.vlan.update(10,state='idle')
        assert 'idle state makes no sense for vlans'
    d.close()


def test_create_vlan_3(dut, log_level):
    setup_dut(dut)
    dut.add_cmd({'cmd':'show running-config', 'state':0, 'action': 'PRINT','args':["""
!
interface port1.0.1-1.0.50
 switchport
 switchport mode access
!
interface vlan1
 ip address 10.17.39.253/24
!
end
    """]})
    dut.add_cmd({'cmd': 'show vlan all'              , 'state':0, 'action': 'PRINT','args':["""
VLAN ID  Name            Type    State   Member ports
                                         (u)-Untagged, (t)-Tagged
======= ================ ======= ======= ====================================
1       default          STATIC  ACTIVE  port1.0.1(u) port1.0.2(u) port1.0.3(u)
                                         port1.0.4(u) port1.0.5(u) port1.0.6(u)
                                         port1.0.7(u) port1.0.8(u) port1.0.9(u)
                                         port1.0.10(u) port1.0.11(u)
                                         port1.0.12(u) port1.0.13(u)
                                         port1.0.14(u) port1.0.15(u)
                                         port1.0.16(u) port1.0.17(u)
                                         port1.0.18(u) port1.0.19(u)
                                         port1.0.20(u) port1.0.21(u)
                                         port1.0.22(u) port1.0.23(u)
                                         port1.0.24(u) port1.0.25(u)
                                         port1.0.26(u) port1.0.27(u)
                                         port1.0.28(u) port1.0.29(u)
                                         port1.0.30(u) port1.0.31(u)
                                         port1.0.32(u) port1.0.33(u)
                                         port1.0.34(u) port1.0.35(u)
                                         port1.0.36(u) port1.0.37(u)
                                         port1.0.38(u) port1.0.39(u)
                                         port1.0.40(u) port1.0.41(u)
                                         port1.0.44(u) port1.0.45(u)
                                         port1.0.46(u) port1.0.47(u)
                                         port1.0.48(u) port1.0.49(u)
                                         port1.0.50(u)
    """]})
    dut.add_cmd({'cmd': 'vlan database'                           , 'state':0, 'action':'SET_PROMPT','args':['(config-vlan)#']})
    dut.add_cmd({'cmd': 'vlan database'                           , 'state':0, 'action':'SET_STATE','args':[1]})
    dut.add_cmd({'cmd': 'vlan 99 state disable'                   , 'state':1, 'action':'SET_STATE','args':[2]})
    dut.add_cmd({'cmd': 'show running-config'                     , 'state':2, 'action':'PRINT'    ,'args':["""
!
interface port1.0.1-1.0.50
 switchport
 switchport mode access
!
interface vlan1
 ip address 10.17.39.253/24
!
vlan database
 vlan 99 state disable
!
end
    """]})
    dut.add_cmd({'cmd': 'show vlan all'              , 'state':2, 'action': 'PRINT','args':["""
VLAN ID  Name            Type    State   Member ports
                                         (u)-Untagged, (t)-Tagged
======= ================ ======= ======= ====================================
1       default          STATIC  ACTIVE  port1.0.1(u) port1.0.2(u) port1.0.3(u)
                                         port1.0.4(u) port1.0.5(u) port1.0.6(u)
                                         port1.0.7(u) port1.0.8(u) port1.0.9(u)
                                         port1.0.10(u) port1.0.11(u)
                                         port1.0.12(u) port1.0.13(u)
                                         port1.0.14(u) port1.0.15(u)
                                         port1.0.16(u) port1.0.17(u)
                                         port1.0.18(u) port1.0.19(u)
                                         port1.0.20(u) port1.0.21(u)
                                         port1.0.22(u) port1.0.23(u)
                                         port1.0.24(u) port1.0.25(u)
                                         port1.0.26(u) port1.0.27(u)
                                         port1.0.28(u) port1.0.29(u)
                                         port1.0.30(u) port1.0.31(u)
                                         port1.0.32(u) port1.0.33(u)
                                         port1.0.34(u) port1.0.35(u)
                                         port1.0.36(u) port1.0.37(u)
                                         port1.0.38(u) port1.0.39(u)
                                         port1.0.40(u) port1.0.41(u)
                                         port1.0.44(u) port1.0.45(u)
                                         port1.0.46(u) port1.0.47(u)
                                         port1.0.48(u) port1.0.49(u)
                                         port1.0.50(u)
99      VLAN0099         STATIC  SUSPEND

    """]})
    d=Device(host=dut.host,port=dut.port,protocol=dut.protocol, log_level=log_level)
    d.open()
    d.vlan.create(99, state='disable')
    assert d.vlan[99]['state'] == 'disable'
    d.close()


def test_get_interface_config(dut, log_level):
    if dut.mode != 'emulated':
        pytest.skip("only on emulated")
    setup_dut(dut)
    dut.add_cmd({'cmd':'show running-config', 'state':0, 'action':'PRINT','args':["""
vlan database
vlan 10
vlan 1000
exit
!
interface port1.0.14
switchport mode trunk
switchport trunk allowed vlan add 10
exit
!
interface port1.0.15
switchport mode access
switchport access vlan 1000
exit
!
    """]})

    d=Device(host=dut.host,port=dut.port,protocol=dut.protocol, log_level=log_level)
    d.open()
    assert d.vlan._interface_config['1.0.14']['switchport mode'] == 'trunk'
    assert d.vlan._interface_config['1.0.15']['switchport mode'] == 'access'
    d.close()


def test_exist(dut, log_level):
    if dut.mode != 'emulated':
        pytest.skip("only on emulated")
    setup_dut(dut)
    dut.add_cmd({'cmd': 'show running-config'                     , 'state':0, 'action':'PRINT'    ,'args':["""
!
vlan database
 vlan 7 name admin state enable mtu 1200
 vlan 10 name 'marketing vlan' state enable mtu 1200
!
    """]})
    dut.add_cmd({'cmd': 'show vlan all'              , 'state':0, 'action': 'PRINT','args':["""
VLAN ID  Name            Type    State   Member ports
                                         (u)-Untagged, (t)-Tagged
======= ================ ======= ======= ====================================
1       default          STATIC  ACTIVE  port1.0.1(u) port1.0.2(u) port1.0.3(u)
                                         port1.0.4(u) port1.0.5(u) port1.0.6(u)
                                         port1.0.7(u) port1.0.8(u) port1.0.9(u)
                                         port1.0.10(u) port1.0.11(u)
                                         port1.0.12(t) port1.0.13(u)
                                         port1.0.14(u) port1.0.15(u)
                                         port1.0.16(u) port1.0.17(u)
                                         port1.0.18(u) port1.0.19(u)
                                         port1.0.20(t) port1.0.21(u)
                                         port1.0.22(u) port1.0.23(u)
                                         port1.0.24(u) port1.0.25(u)
                                         port1.0.26(u) port1.0.27(u)
                                         port1.0.28(u) port1.0.29(u)
                                         port1.0.31(u)
                                         port1.0.32(u) port1.0.33(u)
                                         port1.0.34(u) port1.0.35(u)
                                         port1.0.36(u) port1.0.37(u)
                                         port1.0.38(u) port1.0.39(u)
                                         port1.0.40(u) port1.0.41(u)
                                         port1.0.44(u) port1.0.45(u)
                                         port1.0.46(u) port1.0.47(u)
                                         port1.0.48(u) port1.0.49(u)
                                         port1.0.50(u)
7       admin            STATIC  ACTIVE  port1.0.28(t) port1.0.29(u)
10      "marketing vlan" STATIC  ACTIVE  port1.0.42(u) port1.0.43(t)
20      VLAN0020         STATIC  ACTIVE  port1.0.42(u) port1.0.43(t)
    """]})
    d=Device(host=dut.host,port=dut.port,protocol=dut.protocol, log_level=log_level)
    d.open()
    assert d.vlan[7]['state'] == 'enable'
    assert d.vlan[7]['name'] == 'admin'
    assert d.vlan[10]['name'] == 'marketing vlan'
    d.close()


def test_update(dut, log_level):
    setup_dut(dut)
    dut.add_cmd({'cmd':'show running-config', 'state':0, 'action': 'PRINT','args':["""
!
interface port1.0.1-1.0.50
switchport
switchport mode access
!
vlan database
vlan 10 name "marketing vlan"
vlan 10 state enable
vlan 7 name admin state enable
vlan 8-100 mtu 1200
vlan 6,7 mtu 1000
!
end
    """]})
    dut.add_cmd({'cmd': 'show vlan all',                        'state':0, 'action':'PRINT','args':["""
VLAN ID  Name            Type    State   Member ports
                                         (u)-Untagged, (t)-Tagged
======= ================ ======= ======= ====================================
1       default          STATIC  ACTIVE  port1.0.1(u) port1.0.2(u) port1.0.3(u)
                                         port1.0.4(u) port1.0.5(u) port1.0.6(u)
                                         port1.0.7(u) port1.0.8(u) port1.0.9(u)
                                         port1.0.10(u) port1.0.11(u)
                                         port1.0.12(t) port1.0.13(u)
                                         port1.0.14(u) port1.0.15(u)
                                         port1.0.16(u) port1.0.17(u)
                                         port1.0.18(u) port1.0.19(u)
                                         port1.0.20(t) port1.0.21(u)
                                         port1.0.22(u) port1.0.23(u)
                                         port1.0.24(u) port1.0.25(u)
                                         port1.0.26(u) port1.0.27(u)
                                         port1.0.28(u) port1.0.29(u)
                                         port1.0.31(u)
                                         port1.0.32(u) port1.0.33(u)
                                         port1.0.34(u) port1.0.35(u)
                                         port1.0.36(u) port1.0.37(u)
                                         port1.0.38(u) port1.0.39(u)
                                         port1.0.40(u) port1.0.41(u)
                                         port1.0.44(u) port1.0.45(u)
                                         port1.0.46(u) port1.0.47(u)
                                         port1.0.48(u) port1.0.49(u)
                                         port1.0.50(u)
7       VLAN0007         STATIC  ACTIVE  port1.0.28(t) port1.0.29(u)
20      "this is a long vlan name"
                         STATIC  ACTIVE  port1.0.42(u) port1.0.43(t)
10      VLAN0010         STATIC  ACTIVE  port1.0.28(t) port1.0.29(u)
                                         port1.0.19(t) port1.0.30(t)
    """]})
    dut.add_cmd({'cmd': 'vlan database'                  , 'state':0, 'action':'SET_PROMPT','args':['(config-vlan)#']})
    dut.add_cmd({'cmd': 'vlan database'                  , 'state':0, 'action':'SET_STATE','args':[1]})
    dut.add_cmd({'cmd': 'vlan 20 name vlan_name'         , 'state':1, 'action':'SET_STATE','args':[2]})
    dut.add_cmd({'cmd': 'vlan 20 mtu 1300',                'state':2, 'action':'SET_STATE','args':[3]})
    dut.add_cmd({'cmd': 'show running-config',             'state':3, 'action':'PRINT','args':["""
!
vlan database
vlan 20 name vlan_name state enable mtu 1300
!
    """]})
    dut.add_cmd({'cmd': 'show vlan all',                        'state':3, 'action':'PRINT','args':["""
VLAN ID  Name            Type    State   Member ports
                                         (u)-Untagged, (t)-Tagged
======= ================ ======= ======= ====================================
1       default          STATIC  ACTIVE  port1.0.1(u) port1.0.2(u) port1.0.3(u)
                                         port1.0.4(u) port1.0.5(u) port1.0.6(u)
                                         port1.0.7(u) port1.0.8(u) port1.0.9(u)
                                         port1.0.10(u) port1.0.11(u)
                                         port1.0.12(t) port1.0.13(u)
                                         port1.0.14(u) port1.0.15(u)
                                         port1.0.16(u) port1.0.17(u)
                                         port1.0.18(u) port1.0.19(u)
                                         port1.0.20(t) port1.0.21(u)
                                         port1.0.22(u) port1.0.23(u)
                                         port1.0.24(u) port1.0.25(u)
                                         port1.0.26(u) port1.0.27(u)
                                         port1.0.28(u) port1.0.29(u)
                                         port1.0.31(u)
                                         port1.0.32(u) port1.0.33(u)
                                         port1.0.34(u) port1.0.35(u)
                                         port1.0.36(u) port1.0.37(u)
                                         port1.0.38(u) port1.0.39(u)
                                         port1.0.40(u) port1.0.41(u)
                                         port1.0.44(u) port1.0.45(u)
                                         port1.0.46(u) port1.0.47(u)
                                         port1.0.48(u) port1.0.49(u)
                                         port1.0.50(u)
7       VLAN0007         STATIC  ACTIVE  port1.0.28(t) port1.0.29(u)
20      vlan_name        STATIC  ACTIVE  port1.0.42(u) port1.0.43(t)
10      VLAN0010         STATIC  ACTIVE  port1.0.28(t) port1.0.29(u)
                                         port1.0.19(t) port1.0.30(t)
    """]})
    dut.add_cmd({'cmd': 'vlan database'                    , 'state':3, 'action':'SET_PROMPT','args':['(config-vlan)#']})
    dut.add_cmd({'cmd': 'vlan database'                    , 'state':3, 'action':'SET_STATE','args':[4]})
    dut.add_cmd({'cmd': 'vlan 20 name "vlan name"'         , 'state':4, 'action':'SET_STATE','args':[5]})
    dut.add_cmd({'cmd': 'vlan 20 mtu 1400'                 , 'state':5, 'action':'SET_STATE','args':[6]})
    dut.add_cmd({'cmd': 'show running-config',               'state':6, 'action':'PRINT','args':["""
!
vlan database
vlan 20 name "vlan name" state enable mtu 1400
!
    """]})
    dut.add_cmd({'cmd': 'show vlan all',                   'state':6, 'action':'PRINT','args':["""
VLAN ID  Name            Type    State   Member ports
                                         (u)-Untagged, (t)-Tagged
======= ================ ======= ======= ====================================
1       default          STATIC  ACTIVE  port1.0.1(u) port1.0.2(u) port1.0.3(u)
                                         port1.0.4(u) port1.0.5(u) port1.0.6(u)
                                         port1.0.7(u) port1.0.8(u) port1.0.9(u)
                                         port1.0.10(u) port1.0.11(u)
                                         port1.0.12(t) port1.0.13(u)
                                         port1.0.14(u) port1.0.15(u)
                                         port1.0.16(u) port1.0.17(u)
                                         port1.0.18(u) port1.0.19(u)
                                         port1.0.20(t) port1.0.21(u)
                                         port1.0.22(u) port1.0.23(u)
                                         port1.0.24(u) port1.0.25(u)
                                         port1.0.26(u) port1.0.27(u)
                                         port1.0.28(u) port1.0.29(u)
                                         port1.0.31(u)
                                         port1.0.32(u) port1.0.33(u)
                                         port1.0.34(u) port1.0.35(u)
                                         port1.0.36(u) port1.0.37(u)
                                         port1.0.38(u) port1.0.39(u)
                                         port1.0.40(u) port1.0.41(u)
                                         port1.0.44(u) port1.0.45(u)
                                         port1.0.46(u) port1.0.47(u)
                                         port1.0.48(u) port1.0.49(u)
                                         port1.0.50(u)
7       VLAN0007         STATIC  ACTIVE  port1.0.28(t) port1.0.29(u)
20      "vlan name"      STATIC  ACTIVE  port1.0.42(u) port1.0.43(t)
10      VLAN0010         STATIC  ACTIVE  port1.0.28(t) port1.0.29(u)
                                         port1.0.19(t) port1.0.30(t)
    """]})
    d=Device(host=dut.host,port=dut.port,protocol=dut.protocol, log_level=log_level)
    d.open()
    d.vlan.create(20, mtu=1300, name='vlan_name')
    assert d.vlan[20]['mtu'] == 1300
    assert d.vlan[20]['name'] == 'vlan_name'
    d.vlan.update(20, mtu=1400, name='vlan name')
    assert d.vlan[20]['mtu'] == 1400
    assert d.vlan[20]['name'] == 'vlan name'
    d.close()


def test_add_interface_1(dut, log_level):
    setup_dut(dut)
    dut.add_cmd({'cmd':'show running-config', 'state':0, 'action': 'PRINT','args':["""
!
interface port1.0.1-1.0.50
switchport
switchport mode access
!
vlan database
vlan 10 state enable
!
end
    """]})
    dut.add_cmd({'cmd': 'show vlan all',                        'state':0, 'action':'PRINT','args':["""
VLAN ID  Name            Type    State   Member ports
                                         (u)-Untagged, (t)-Tagged
======= ================ ======= ======= ====================================
1       default          STATIC  ACTIVE  port1.0.1(u) port1.0.2(u) port1.0.3(u)
                                         port1.0.4(u) port1.0.5(u) port1.0.6(u)
                                         port1.0.7(u) port1.0.8(u) port1.0.9(u)
                                         port1.0.10(u) port1.0.11(u)
                                         port1.0.12(t) port1.0.13(u)
                                         port1.0.14(u) port1.0.15(u)
                                         port1.0.16(u) port1.0.17(u)
                                         port1.0.18(u) port1.0.19(u)
                                         port1.0.20(t) port1.0.21(u)
                                         port1.0.22(u) port1.0.23(u)
                                         port1.0.24(u) port1.0.25(u)
                                         port1.0.26(u) port1.0.27(u)
                                         port1.0.28(u) port1.0.29(u)
                                         port1.0.30(u) port1.0.31(u)
                                         port1.0.32(u) port1.0.33(u)
                                         port1.0.34(u) port1.0.35(u)
                                         port1.0.36(u) port1.0.37(u)
                                         port1.0.38(u) port1.0.39(u)
                                         port1.0.40(u) port1.0.41(u)
                                         port1.0.44(u) port1.0.45(u)
                                         port1.0.46(u) port1.0.47(u)
                                         port1.0.48(u) port1.0.49(u)
                                         port1.0.50(u)
10      VLAN0010         STATIC  ACTIVE  port1.0.28(t)
    """]})
    dut.add_cmd({'cmd': 'interface port1.0.14',      'state':0, 'action':'SET_PROMPT','args':['(config-if)#']})
    dut.add_cmd({'cmd': 'interface port1.0.14',      'state':0, 'action':'SET_STATE','args':[1]})
    dut.add_cmd({'cmd': 'switchport access vlan 10', 'state':1, 'action':'SET_STATE','args':[2]})
    dut.add_cmd({'cmd': 'show vlan all',             'state':2, 'action':'PRINT','args':["""
VLAN ID  Name            Type    State   Member ports                   
                                         (u)-Untagged, (t)-Tagged
======= ================ ======= ======= ====================================
1       default          STATIC  ACTIVE  port1.0.1(u) port1.0.2(u) port1.0.3(u) 
                                         port1.0.4(u) port1.0.5(u) port1.0.6(u) 
                                         port1.0.7(u) port1.0.8(u) port1.0.9(u) 
                                         port1.0.10(u) port1.0.11(u) 
                                         port1.0.12(t) port1.0.13(u)
                                         port1.0.15(u)
                                         port1.0.16(u) port1.0.17(u) 
                                         port1.0.18(u) port1.0.19(u) 
                                         port1.0.20(t) port1.0.21(u)
                                         port1.0.22(u) port1.0.23(u) 
                                         port1.0.24(u) port1.0.25(u) 
                                         port1.0.26(u) port1.0.27(u) 
                                         port1.0.28(u) port1.0.29(u) 
                                         port1.0.30(u) port1.0.31(u)
                                         port1.0.32(u) port1.0.33(u) 
                                         port1.0.34(u) port1.0.35(u) 
                                         port1.0.36(u) port1.0.37(u) 
                                         port1.0.38(u) port1.0.39(u) 
                                         port1.0.40(u) port1.0.41(u) 
                                         port1.0.44(u) port1.0.45(u) 
                                         port1.0.46(u) port1.0.47(u) 
                                         port1.0.48(u) port1.0.49(u) 
                                         port1.0.50(u) 
10      VLAN0010         STATIC  ACTIVE  port1.0.28(t) port1.0.14(u)
"""]})
    d=Device(host=dut.host,port=dut.port,protocol=dut.protocol, log_level=log_level)
    d.open()
    d.vlan.add_interface(10,'1.0.14')
    assert '1.0.14' in d.vlan[10]['untagged']
    assert '1.0.14' not in d.vlan[1]['untagged']
    with pytest.raises(ValueError) as excinfo:
        d.vlan.add_interface(11,'1.0.20')
        assert '{0} is not a valid vlan id' in excinfo.value
    with pytest.raises(ValueError) as excinfo:
        d.vlan.add_interface(10,'1.0.51')
        assert '{0} is not a valid interface' in excinfo.value
    d.close()


def test_delete_interface_1(dut, log_level):
    setup_dut(dut)
    dut.add_cmd({'cmd':'show running-config', 'state':0, 'action': 'PRINT','args':["""
!
interface port1.0.1-1.0.50
switchport
switchport mode access
!
vlan database
vlan 10 state enable
!
end
    """]})
    dut.add_cmd({'cmd': 'show vlan all'               , 'state':0, 'action':'PRINT','args':["""
VLAN ID  Name            Type    State   Member ports
                                         (u)-Untagged, (t)-Tagged
======= ================ ======= ======= ====================================
1       default          STATIC  ACTIVE  port1.0.1(u) port1.0.2(u) port1.0.3(u)
                                         port1.0.4(u) port1.0.5(u) port1.0.6(u)
                                         port1.0.7(u) port1.0.8(u) port1.0.9(u)
                                         port1.0.10(u) port1.0.11(u)
                                         port1.0.12(t) port1.0.13(u)
                                         port1.0.14(u) port1.0.15(u)
                                         port1.0.16(u) port1.0.17(u)
                                         port1.0.18(u) port1.0.19(u)
                                         port1.0.20(t) port1.0.21(u)
                                         port1.0.22(u) port1.0.23(u)
                                         port1.0.24(u) port1.0.25(u)
                                         port1.0.26(u) port1.0.27(u)
                                         port1.0.28(u) port1.0.29(u)
                                         port1.0.30(u) port1.0.31(u)
                                         port1.0.32(u) port1.0.33(u)
                                         port1.0.34(u) port1.0.35(u)
                                         port1.0.36(u) port1.0.37(u)
                                         port1.0.38(u) port1.0.39(u)
                                         port1.0.40(u) port1.0.41(u)
                                         port1.0.44(u) port1.0.45(u)
                                         port1.0.46(u) port1.0.47(u)
                                         port1.0.48(u) port1.0.49(u)
                                         port1.0.50(u)
10      VLAN0010         STATIC  ACTIVE  port1.0.28(t) port1.0.19(t)
                                         port1.0.14(u)
"""]})

    dut.add_cmd({'cmd': 'interface port1.0.14'        , 'state':0, 'action':'SET_PROMPT','args':['(config-if)#']})
    dut.add_cmd({'cmd': 'interface port1.0.14'        , 'state':0, 'action':'SET_STATE','args':[1]})
    dut.add_cmd({'cmd': 'no switchport access vlan'   , 'state':1, 'action':'SET_STATE','args':[2]})
    dut.add_cmd({'cmd': 'show vlan all'               , 'state':2, 'action':'PRINT','args':["""
VLAN ID  Name            Type    State   Member ports
                                         (u)-Untagged, (t)-Tagged
======= ================ ======= ======= ====================================
1       default          STATIC  ACTIVE  port1.0.1(u) port1.0.2(u) port1.0.3(u)
                                         port1.0.4(u) port1.0.5(u) port1.0.6(u)
                                         port1.0.7(u) port1.0.8(u) port1.0.9(u)
                                         port1.0.10(u) port1.0.11(u)
                                         port1.0.12(t) port1.0.13(u)
                                         port1.0.14(u) port1.0.15(u)
                                         port1.0.16(u) port1.0.17(u)
                                         port1.0.18(u) port1.0.19(u)
                                         port1.0.20(t) port1.0.21(u)
                                         port1.0.22(u) port1.0.23(u)
                                         port1.0.24(u) port1.0.25(u)
                                         port1.0.26(u) port1.0.27(u)
                                         port1.0.28(u) port1.0.29(u)
                                         port1.0.30(u) port1.0.31(u)
                                         port1.0.32(u) port1.0.33(u)
                                         port1.0.34(u) port1.0.35(u)
                                         port1.0.36(u) port1.0.37(u)
                                         port1.0.38(u) port1.0.39(u)
                                         port1.0.40(u) port1.0.41(u)
                                         port1.0.44(u) port1.0.45(u)
                                         port1.0.46(u) port1.0.47(u)
                                         port1.0.48(u) port1.0.49(u)
                                         port1.0.50(u)
10      VLAN0010         STATIC  ACTIVE  port1.0.28(t) port1.0.19(t)
"""]})
    d=Device(host=dut.host,port=dut.port,protocol=dut.protocol, log_level=log_level)
    d.open()
    d.vlan.delete_interface(10,'1.0.14')
    assert '1.0.14' not in d.vlan[10]['untagged']
    assert '1.0.14' in d.vlan[1]['untagged']
    with pytest.raises(ValueError) as excinfo:
        d.vlan.delete_interface(11,'1.0.20')
        assert '{0} is not a valid vlan id' in excinfo.value
    with pytest.raises(ValueError) as excinfo:
        d.vlan.delete_interface(10,'1.0.18')
        assert 'interface {0} does not belong to vlan {1}' in excinfo.value
    with pytest.raises(ValueError) as excinfo:
        d.vlan.delete_interface(10,'1.0.51')
        assert '{0} is not a valid interface' in excinfo.value
    d.close()


def test_add_interface_2(dut, log_level):
    setup_dut(dut)
    dut.add_cmd({'cmd':'show running-config', 'state':0, 'action': 'PRINT','args':["""
!
interface port1.0.1-1.0.50
 switchport
 switchport mode access
!
vlan database
 vlan 7 name admin state enable
 vlan 10 state enable
 vlan 20 "this is a long vlan name" state enable
!
end
    """]})
    dut.add_cmd({'cmd': 'show vlan all',                        'state':0, 'action':'PRINT','args':["""
VLAN ID  Name            Type    State   Member ports
                                         (u)-Untagged, (t)-Tagged
======= ================ ======= ======= ====================================
1       default          STATIC  ACTIVE  port1.0.1(u) port1.0.2(u) port1.0.3(u)
                                         port1.0.4(u) port1.0.5(u) port1.0.6(u)
                                         port1.0.7(u) port1.0.8(u) port1.0.9(u)
                                         port1.0.10(u) port1.0.11(u)
                                         port1.0.12(t) port1.0.13(u)
                                         port1.0.14(u) port1.0.15(u)
                                         port1.0.16(u) port1.0.17(u)
                                         port1.0.18(u) port1.0.19(u)
                                         port1.0.20(t) port1.0.21(u)
                                         port1.0.22(u) port1.0.23(u)
                                         port1.0.24(u) port1.0.25(u)
                                         port1.0.26(u) port1.0.27(u)
                                         port1.0.28(u) port1.0.29(u)
                                         port1.0.31(u)
                                         port1.0.32(u) port1.0.33(u)
                                         port1.0.34(u) port1.0.35(u)
                                         port1.0.36(u) port1.0.37(u)
                                         port1.0.38(u) port1.0.39(u)
                                         port1.0.40(u) port1.0.41(u)
                                         port1.0.44(u) port1.0.45(u)
                                         port1.0.46(u) port1.0.47(u)
                                         port1.0.48(u) port1.0.49(u)
                                         port1.0.50(u)
7       VLAN0007         STATIC  ACTIVE  port1.0.28(t) port1.0.29(u)
20      "this is a long vlan name"
                         STATIC  ACTIVE  port1.0.42(u) port1.0.43(t)
10      VLAN0010         STATIC  ACTIVE  port1.0.28(t) port1.0.29(u)
                                         port1.0.19(t)
    """]})
    dut.add_cmd({'cmd': 'interface port1.0.15'                , 'state':0, 'action':'SET_PROMPT','args':['(config-if)#']})
    dut.add_cmd({'cmd': 'interface port1.0.15'                , 'state':0, 'action':'SET_STATE','args':[1]})
    dut.add_cmd({'cmd': 'switchport mode trunk'               , 'state':1, 'action':'SET_STATE','args':[2]})
    dut.add_cmd({'cmd': 'switchport trunk allowed vlan add 10', 'state':2, 'action':'SET_STATE','args':[3]})
    dut.add_cmd({'cmd':'show running-config', 'state':3, 'action': 'PRINT','args':["""
!
interface port1.0.1-1.0.50
 switchport
 switchport mode access
!
interface port1.0.15
 switchport
 switchport mode trunk
!
vlan database
 vlan 7 name admin state enable
 vlan 10 state enable
 vlan 20 "this is a long vlan name" state enable
!
end
    """]})
    dut.add_cmd({'cmd': 'show vlan all'                       , 'state':3, 'action':'PRINT','args':["""
VLAN ID  Name            Type    State   Member ports
                                         (u)-Untagged, (t)-Tagged
======= ================ ======= ======= ====================================
1       default          STATIC  ACTIVE  port1.0.1(u) port1.0.2(u) port1.0.3(u)
                                         port1.0.4(u) port1.0.5(u) port1.0.6(u)
                                         port1.0.7(u) port1.0.8(u) port1.0.9(u)
                                         port1.0.10(u) port1.0.11(u)
                                         port1.0.12(t) port1.0.13(u)
                                         port1.0.14(u) port1.0.15(u)
                                         port1.0.16(u) port1.0.17(u)
                                         port1.0.18(u) port1.0.19(u)
                                         port1.0.20(t) port1.0.21(u)
                                         port1.0.22(u) port1.0.23(u)
                                         port1.0.24(u) port1.0.25(u)
                                         port1.0.26(u) port1.0.27(u)
                                         port1.0.28(u) port1.0.29(u)
                                         port1.0.30(u) port1.0.31(u)
                                         port1.0.32(u) port1.0.33(u)
                                         port1.0.34(u) port1.0.35(u)
                                         port1.0.36(u) port1.0.37(u)
                                         port1.0.38(u) port1.0.39(u)
                                         port1.0.40(u) port1.0.41(u)
                                         port1.0.44(u) port1.0.45(u)
                                         port1.0.46(u) port1.0.47(u)
                                         port1.0.48(u) port1.0.49(u)
                                         port1.0.50(u)
7       VLAN0007         STATIC  ACTIVE  port1.0.28(t) port1.0.29(u)
20      "this is a long vlan name"
                         STATIC  ACTIVE  port1.0.42(u) port1.0.43(t)
10      VLAN0010         STATIC  ACTIVE  port1.0.28(t) port1.0.29(u)
                                         port1.0.19(t) port1.0.15(t)
"""]})
    d=Device(host=dut.host,port=dut.port,protocol=dut.protocol, log_level=log_level)
    d.open()
    assert '1.0.15' in d.vlan[1]['untagged']
    assert '1.0.15' not in d.vlan[10]['tagged']
    d.vlan.add_interface(10,'1.0.15',tagged=True)
    assert '1.0.15' in d.vlan[1]['untagged']
    assert '1.0.15' in d.vlan[10]['tagged']
    d.close()


def test_delete_interface_2(dut, log_level):
    setup_dut(dut)
    dut.add_cmd({'cmd':'show running-config', 'state':0, 'action': 'PRINT','args':["""
!
interface port1.0.1-1.0.50
switchport
switchport mode access
!
interface port1.0.15
 switchport
 switchport mode trunk
!
vlan database
 vlan 7 name admin state enable
 vlan 10 state enable
 vlan 20 "this is a long vlan name" state enable
!
end
    """]})
    dut.add_cmd({'cmd': 'show vlan all'               , 'state':0, 'action':'PRINT','args':["""
VLAN ID  Name            Type    State   Member ports
                                         (u)-Untagged, (t)-Tagged
======= ================ ======= ======= ====================================
1       default          STATIC  ACTIVE  port1.0.1(u) port1.0.2(u) port1.0.3(u)
                                         port1.0.4(u) port1.0.5(u) port1.0.6(u)
                                         port1.0.7(u) port1.0.8(u) port1.0.9(u)
                                         port1.0.10(u) port1.0.11(u)
                                         port1.0.12(t) port1.0.13(u)
                                         port1.0.14(u) port1.0.15(u)
                                         port1.0.16(u) port1.0.17(u)
                                         port1.0.18(u) port1.0.19(u)
                                         port1.0.20(t) port1.0.21(u)
                                         port1.0.22(u) port1.0.23(u)
                                         port1.0.24(u) port1.0.25(u)
                                         port1.0.26(u) port1.0.27(u)
                                         port1.0.28(u) port1.0.29(u)
                                         port1.0.30(u) port1.0.31(u)
                                         port1.0.32(u) port1.0.33(u)
                                         port1.0.34(u) port1.0.35(u)
                                         port1.0.36(u) port1.0.37(u)
                                         port1.0.38(u) port1.0.39(u)
                                         port1.0.40(u) port1.0.41(u)
                                         port1.0.44(u) port1.0.45(u)
                                         port1.0.46(u) port1.0.47(u)
                                         port1.0.48(u) port1.0.49(u)
                                         port1.0.50(u)
7       VLAN0007         STATIC  ACTIVE  port1.0.28(t) port1.0.29(u)
20      "this is a long vlan name"
                         STATIC  ACTIVE  port1.0.42(t) port1.0.43(t)
10      VLAN0010         STATIC  ACTIVE  port1.0.28(t) port1.0.29(u)
                                         port1.0.19(t) port1.0.15(t)
"""]})
    dut.add_cmd({'cmd': 'interface port1.0.15'                   , 'state':0, 'action':'SET_PROMPT','args':['(config-if)#']})
    dut.add_cmd({'cmd': 'interface port1.0.15'                   , 'state':0, 'action':'SET_STATE','args':[1]})
    dut.add_cmd({'cmd': 'switchport trunk allowed vlan remove 10', 'state':1, 'action':'SET_STATE','args':[2]})
    dut.add_cmd({'cmd': 'show running-config'                    , 'state':2, 'action':'PRINT','args':["""
!
interface port1.0.1-1.0.50
switchport
switchport mode access
!
interface port1.0.15
 switchport
 switchport mode trunk
!
vlan database
 vlan 7 name admin state enable
 vlan 10 state enable
 vlan 20 "this is a long vlan name" state enable
!
end
    """]})
    dut.add_cmd({'cmd': 'show vlan all'                          , 'state':2, 'action':'PRINT','args':["""
VLAN ID  Name            Type    State   Member ports
                                         (u)-Untagged, (t)-Tagged
======= ================ ======= ======= ====================================
1       default          STATIC  ACTIVE  port1.0.1(u) port1.0.2(u) port1.0.3(u)
                                         port1.0.4(u) port1.0.5(u) port1.0.6(u)
                                         port1.0.7(u) port1.0.8(u) port1.0.9(u)
                                         port1.0.10(u) port1.0.11(u)
                                         port1.0.12(t) port1.0.13(u)
                                         port1.0.14(u) port1.0.15(u)
                                         port1.0.16(u) port1.0.17(u)
                                         port1.0.18(u) port1.0.19(u)
                                         port1.0.20(t) port1.0.21(u)
                                         port1.0.22(u) port1.0.23(u)
                                         port1.0.24(u) port1.0.25(u)
                                         port1.0.26(u) port1.0.27(u)
                                         port1.0.28(u) port1.0.29(u)
                                         port1.0.30(u) port1.0.31(u)
                                         port1.0.32(u) port1.0.33(u)
                                         port1.0.34(u) port1.0.35(u)
                                         port1.0.36(u) port1.0.37(u)
                                         port1.0.38(u) port1.0.39(u)
                                         port1.0.40(u) port1.0.41(u)
                                         port1.0.44(u) port1.0.45(u)
                                         port1.0.46(u) port1.0.47(u)
                                         port1.0.48(u) port1.0.49(u)
                                         port1.0.50(u)
7       VLAN0007         STATIC  ACTIVE  port1.0.28(t) port1.0.29(u)
20      "this is a long vlan name"
                         STATIC  ACTIVE  port1.0.42(t) port1.0.43(t)
10      VLAN0010         STATIC  ACTIVE  port1.0.28(t) port1.0.29(u)
                                         port1.0.19(t)
    """]})

    d=Device(host=dut.host,port=dut.port,protocol=dut.protocol, log_level=log_level)
    d.open()
    assert '1.0.15' in d.vlan[1]['untagged']
    assert '1.0.15' in d.vlan[10]['tagged']
    d.vlan.delete_interface(10,'1.0.15')
    # assert '1.0.15' in d.vlan[1]['untagged']
    # assert '1.0.15' not in d.vlan[10]['tagged']
    d.close()


def test_add_interface_3(dut, log_level):
    setup_dut(dut)
    dut.add_cmd({'cmd':'show running-config', 'state':0, 'action': 'PRINT','args':["""
!
interface port1.0.1-1.0.15
switchport
switchport mode access
exit
!
interface port1.0.16
switchport
switchport mode trunk
exit
!
interface port1.0.17-1.0.50
switchport
switchport mode access
exit
!
interface vlan 1
ip address 10.17.39.253 255.255.255.0
exit
!
vlan database
vlan 10 name "marketing vlan"
vlan 10 state enable
vlan 7 name admin state enable
exit
!
end
    """]})
    dut.add_cmd({'cmd': 'show vlan all'               , 'state':0, 'action':'PRINT','args':["""
VLAN ID  Name            Type    State   Member ports
                                         (u)-Untagged, (t)-Tagged
======= ================ ======= ======= ====================================
1       default          STATIC  ACTIVE  port1.0.1(u) port1.0.2(u) port1.0.3(u)
                                         port1.0.4(u) port1.0.5(u) port1.0.6(u)
                                         port1.0.7(u) port1.0.8(u) port1.0.9(u)
                                         port1.0.10(u) port1.0.11(u)
                                         port1.0.12(t) port1.0.13(u)
                                         port1.0.14(u) port1.0.15(u)
                                         port1.0.16(u) port1.0.17(u)
                                         port1.0.18(u) port1.0.19(u)
                                         port1.0.20(t) port1.0.21(u)
                                         port1.0.22(u) port1.0.23(u)
                                         port1.0.24(u) port1.0.25(u)
                                         port1.0.26(u) port1.0.27(u)
                                         port1.0.28(u) port1.0.29(u)
                                         port1.0.30(u) port1.0.31(u)
                                         port1.0.32(u) port1.0.33(u)
                                         port1.0.34(u) port1.0.35(u)
                                         port1.0.36(u) port1.0.37(u)
                                         port1.0.38(u) port1.0.39(u)
                                         port1.0.40(u) port1.0.41(u)
                                         port1.0.44(u) port1.0.45(u)
                                         port1.0.46(u) port1.0.47(u)
                                         port1.0.48(u) port1.0.49(u)
                                         port1.0.50(u)
7       VLAN0007         STATIC  ACTIVE  port1.0.28(t) port1.0.29(u)
20      "this is a long vlan name"
                         STATIC  ACTIVE  port1.0.42(t) port1.0.43(t)
10      VLAN0010         STATIC  ACTIVE  port1.0.28(t) port1.0.19(t)
                                         port1.0.15(t)
"""]})
    dut.add_cmd({'cmd': 'interface port1.0.16'                , 'state':0, 'action':'SET_PROMPT','args':['(config-if)#']})
    dut.add_cmd({'cmd': 'interface port1.0.16'                , 'state':0, 'action':'SET_STATE','args':[1]})
    dut.add_cmd({'cmd': 'switchport mode trunk'               , 'state':1, 'action':'SET_STATE','args':[2]})
    dut.add_cmd({'cmd': 'switchport trunk native vlan 10'     , 'state':2, 'action':'SET_STATE','args':[3]})
    dut.add_cmd({'cmd': 'show running-config'                 , 'state':3, 'action':'PRINT','args':["""
!
interface port1.0.1-1.0.15
switchport
switchport mode access
exit
!
interface port1.0.16
switchport
switchport mode trunk
switchport trunk native vlan 10
exit
!
interface port1.0.17-1.0.50
switchport
switchport mode access
exit
!
interface vlan 1
ip address 10.17.39.253 255.255.255.0
exit
!
vlan database
vlan 10 name "marketing vlan"
vlan 10 state enable
vlan 7 name admin state enable
exit
!
end
    """]})
    dut.add_cmd({'cmd': 'show vlan all'                       , 'state':3, 'action':'PRINT','args':["""
VLAN ID  Name            Type    State   Member ports
                                         (u)-Untagged, (t)-Tagged
======= ================ ======= ======= ====================================
1       default          STATIC  ACTIVE  port1.0.1(u) port1.0.2(u) port1.0.3(u)
                                         port1.0.4(u) port1.0.5(u) port1.0.6(u)
                                         port1.0.7(u) port1.0.8(u) port1.0.9(u)
                                         port1.0.10(u) port1.0.11(u)
                                         port1.0.12(t) port1.0.13(u)
                                         port1.0.14(u) port1.0.15(u)
                                         port1.0.17(u)
                                         port1.0.18(u) port1.0.19(u)
                                         port1.0.20(t) port1.0.21(u)
                                         port1.0.22(u) port1.0.23(u)
                                         port1.0.24(u) port1.0.25(u)
                                         port1.0.26(u) port1.0.27(u)
                                         port1.0.28(u) port1.0.29(u)
                                         port1.0.30(u) port1.0.31(u)
                                         port1.0.32(u) port1.0.33(u)
                                         port1.0.34(u) port1.0.35(u)
                                         port1.0.36(u) port1.0.37(u)
                                         port1.0.38(u) port1.0.39(u)
                                         port1.0.40(u) port1.0.41(u)
                                         port1.0.44(u) port1.0.45(u)
                                         port1.0.46(u) port1.0.47(u)
                                         port1.0.48(u) port1.0.49(u)
                                         port1.0.50(u)
7       VLAN0007         STATIC  ACTIVE  port1.0.28(t) port1.0.29(u)
20      "this is a long vlan name"
                         STATIC  ACTIVE  port1.0.42(t) port1.0.43(t)
10      VLAN0010         STATIC  ACTIVE  port1.0.28(t) port1.0.19(t)
                                         port1.0.15(t) port1.0.16(u)
"""]})
    d=Device(host=dut.host,port=dut.port,protocol=dut.protocol, log_level=log_level)
    d.open()
    assert '1.0.16' in d.vlan[1]['untagged']
    assert '1.0.16' not in d.vlan[10]['untagged']
    d.vlan.add_interface(10,'1.0.16')
    # assert '1.0.16' not in d.vlan[1]['untagged']
    # assert '1.0.16' in d.vlan[10]['untagged']
    d.close()


def test_delete_interface_3(dut, log_level):
    setup_dut(dut)
    dut.add_cmd({'cmd': 'show running-config'                 , 'state':0, 'action':'PRINT','args':["""
!
interface port1.0.1-1.0.50
switchport
switchport mode access
!
interface port1.0.16
switchport mode trunk
switchport trunk native vlan 10
!
vlan database
vlan 10 name "marketing vlan"
vlan 10 state enable
vlan 7 name admin state enable
!
end
    """]})
    dut.add_cmd({'cmd': 'show vlan all'               , 'state':0, 'action':'PRINT','args':["""
VLAN ID  Name            Type    State   Member ports
                                         (u)-Untagged, (t)-Tagged
======= ================ ======= ======= ====================================
1       default          STATIC  ACTIVE  port1.0.1(u) port1.0.2(u) port1.0.3(u)
                                         port1.0.4(u) port1.0.5(u) port1.0.6(u)
                                         port1.0.7(u) port1.0.8(u) port1.0.9(u)
                                         port1.0.10(u) port1.0.11(u)
                                         port1.0.12(t) port1.0.13(u)
                                         port1.0.14(u) port1.0.15(u)
                                         port1.0.17(u)
                                         port1.0.18(u) port1.0.19(u)
                                         port1.0.20(t) port1.0.21(u)
                                         port1.0.22(u) port1.0.23(u)
                                         port1.0.24(u) port1.0.25(u)
                                         port1.0.26(u) port1.0.27(u)
                                         port1.0.28(u) port1.0.29(u)
                                         port1.0.30(u) port1.0.31(u)
                                         port1.0.32(u) port1.0.33(u)
                                         port1.0.34(u) port1.0.35(u)
                                         port1.0.36(u) port1.0.37(u)
                                         port1.0.38(u) port1.0.39(u)
                                         port1.0.40(u) port1.0.41(u)
                                         port1.0.44(u) port1.0.45(u)
                                         port1.0.46(u) port1.0.47(u)
                                         port1.0.48(u) port1.0.49(u)
                                         port1.0.50(u)
7       VLAN0007         STATIC  ACTIVE  port1.0.28(t) port1.0.29(u)
20      "this is a long vlan name"
                         STATIC  ACTIVE  port1.0.42(t) port1.0.43(t)
10      VLAN0010         STATIC  ACTIVE  port1.0.28(t) port1.0.19(t)
                                         port1.0.15(t) port1.0.16(u)
"""]})
    dut.add_cmd({'cmd': 'interface port1.0.16'                   , 'state':0, 'action':'SET_PROMPT','args':['(config-if)#']})
    dut.add_cmd({'cmd': 'interface port1.0.16'                   , 'state':0, 'action':'SET_STATE','args':[1]})
    dut.add_cmd({'cmd': 'no switchport trunk native vlan'        , 'state':1, 'action':'SET_STATE','args':[2]})
    dut.add_cmd({'cmd': 'show running-config'                    , 'state':2, 'action':'PRINT','args':["""
!
interface port1.0.1-1.0.50
switchport
switchport mode access
!
interface port1.0.16
switchport mode trunk
!
vlan database
vlan 10 name "marketing vlan"
vlan 10 state enable
vlan 7 name admin state enable
!
end
    """]})
    dut.add_cmd({'cmd': 'show vlan all'                          , 'state':2, 'action':'PRINT','args':["""
VLAN ID  Name            Type    State   Member ports
                                         (u)-Untagged, (t)-Tagged
======= ================ ======= ======= ====================================
1       default          STATIC  ACTIVE  port1.0.1(u) port1.0.2(u) port1.0.3(u)
                                         port1.0.4(u) port1.0.5(u) port1.0.6(u)
                                         port1.0.7(u) port1.0.8(u) port1.0.9(u)
                                         port1.0.10(u) port1.0.11(u)
                                         port1.0.12(t) port1.0.13(u)
                                         port1.0.14(u) port1.0.15(u)
                                         port1.0.16(u) port1.0.17(u)
                                         port1.0.18(u) port1.0.19(u)
                                         port1.0.20(t) port1.0.21(u)
                                         port1.0.22(u) port1.0.23(u)
                                         port1.0.24(u) port1.0.25(u)
                                         port1.0.26(u) port1.0.27(u)
                                         port1.0.28(u) port1.0.29(u)
                                         port1.0.30(u) port1.0.31(u)
                                         port1.0.32(u) port1.0.33(u)
                                         port1.0.34(u) port1.0.35(u)
                                         port1.0.36(u) port1.0.37(u)
                                         port1.0.38(u) port1.0.39(u)
                                         port1.0.40(u) port1.0.41(u)
                                         port1.0.44(u) port1.0.45(u)
                                         port1.0.46(u) port1.0.47(u)
                                         port1.0.48(u) port1.0.49(u)
                                         port1.0.50(u)
7       VLAN0007         STATIC  ACTIVE  port1.0.28(t) port1.0.29(u)
20      "this is a long vlan name"
                         STATIC  ACTIVE  port1.0.42(t) port1.0.43(t)
10      VLAN0010         STATIC  ACTIVE  port1.0.28(t) port1.0.19(t)
                                         port1.0.15(t)
    """]})

    d=Device(host=dut.host,port=dut.port,protocol=dut.protocol, log_level=log_level)
    d.open()
    assert '1.0.16' not in d.vlan[1]['untagged']
    assert '1.0.16' in d.vlan[10]['untagged']
    d.vlan.delete_interface(10,'1.0.16')
    # assert '1.0.16' in d.vlan[1]['untagged']
    # assert '1.0.16' not in d.vlan[10]['untagged']
    d.close()


def test_add_interface_4(dut, log_level):
    setup_dut(dut)
    dut.add_cmd({'cmd':'show running-config', 'state':0, 'action': 'PRINT','args':["""
!
interface port1.0.1-1.0.50
switchport
switchport mode access
!
vlan database
vlan 10 name "marketing vlan"
vlan 10 state enable
vlan 7 name admin state enable
vlan 8-100 mtu 1200
vlan 6,7 mtu 1000
!
end
    """]})
    dut.add_cmd({'cmd': 'show vlan all',                        'state':0, 'action':'PRINT','args':["""
VLAN ID  Name            Type    State   Member ports
                                         (u)-Untagged, (t)-Tagged
======= ================ ======= ======= ====================================
1       default          STATIC  ACTIVE  port1.0.1(u) port1.0.2(u) port1.0.3(u)
                                         port1.0.4(u) port1.0.5(u) port1.0.6(u)
                                         port1.0.7(u) port1.0.8(u) port1.0.9(u)
                                         port1.0.10(u) port1.0.11(u)
                                         port1.0.12(t) port1.0.13(u)
                                         port1.0.14(u) port1.0.15(u)
                                         port1.0.16(u) port1.0.17(u)
                                         port1.0.18(u) port1.0.19(u)
                                         port1.0.20(t) port1.0.21(u)
                                         port1.0.22(u) port1.0.23(u)
                                         port1.0.24(u) port1.0.25(u)
                                         port1.0.26(u) port1.0.27(u)
                                         port1.0.28(u) port1.0.29(u)
                                         port1.0.31(u)
                                         port1.0.32(u) port1.0.33(u)
                                         port1.0.34(u) port1.0.35(u)
                                         port1.0.36(u) port1.0.37(u)
                                         port1.0.38(u) port1.0.39(u)
                                         port1.0.40(u) port1.0.41(u)
                                         port1.0.44(u) port1.0.45(u)
                                         port1.0.46(u) port1.0.47(u)
                                         port1.0.48(u) port1.0.49(u)
                                         port1.0.50(u)
7       VLAN0007         STATIC  ACTIVE  port1.0.28(t) port1.0.29(u)
20      "this is a long vlan name"
                         STATIC  ACTIVE  port1.0.42(u) port1.0.43(t)
10      VLAN0010         STATIC  ACTIVE  port1.0.28(t)
    """]})
    dut.add_cmd({'cmd': 'interface port1.0.17'                , 'state':0, 'action':'SET_PROMPT','args':['(config-if)#']})
    dut.add_cmd({'cmd': 'interface port1.0.17'                , 'state':0, 'action':'SET_STATE','args':[1]})
    dut.add_cmd({'cmd': 'switchport mode trunk'               , 'state':1, 'action':'SET_STATE','args':[2]})
    dut.add_cmd({'cmd': 'switchport trunk allowed vlan add 10', 'state':2, 'action':'SET_STATE','args':[3]})
    dut.add_cmd({'cmd': 'show running-config'                 , 'state':3, 'action':'PRINT','args':["""
!
interface port1.0.1-1.0.16
switchport
switchport mode access
!
interface port1.0.17
switchport
switchport mode trunk
switchport trunk allowed vlan add 10
!
interface port1.0.18-1.0.50
switchport
switchport mode access
!
vlan database
vlan 10 name "marketing vlan"
vlan 10 state enable
vlan 7 name admin state enable
!
end
    """]})
    dut.add_cmd({'cmd': 'show vlan all'                       , 'state':3, 'action':'PRINT','args':["""
VLAN ID  Name            Type    State   Member ports
                                         (u)-Untagged, (t)-Tagged
======= ================ ======= ======= ====================================
1       default          STATIC  ACTIVE  port1.0.1(u) port1.0.2(u) port1.0.3(u)
                                         port1.0.4(u) port1.0.5(u) port1.0.6(u)
                                         port1.0.7(u) port1.0.8(u) port1.0.9(u)
                                         port1.0.10(u) port1.0.11(u)
                                         port1.0.12(t) port1.0.13(u)
                                         port1.0.14(u) port1.0.15(u)
                                         port1.0.16(u) port1.0.17(u)
                                         port1.0.18(u) port1.0.19(u)
                                         port1.0.20(t) port1.0.21(u)
                                         port1.0.22(u) port1.0.23(u)
                                         port1.0.24(u) port1.0.25(u)
                                         port1.0.26(u) port1.0.27(u)
                                         port1.0.28(u) port1.0.29(u)
                                         port1.0.30(u) port1.0.31(u)
                                         port1.0.32(u) port1.0.33(u)
                                         port1.0.34(u) port1.0.35(u)
                                         port1.0.36(u) port1.0.37(u)
                                         port1.0.38(u) port1.0.39(u)
                                         port1.0.40(u) port1.0.41(u)
                                         port1.0.44(u) port1.0.45(u)
                                         port1.0.46(u) port1.0.47(u)
                                         port1.0.48(u) port1.0.49(u)
                                         port1.0.50(u)
7       VLAN0007         STATIC  ACTIVE  port1.0.28(t) port1.0.29(u)
20      "this is a long vlan name"
                         STATIC  ACTIVE  port1.0.42(t) port1.0.43(t)
10      VLAN0010         STATIC  ACTIVE  port1.0.28(t) port1.0.17(t)
"""]})
    d=Device(host=dut.host,port=dut.port,protocol=dut.protocol, log_level=log_level)
    d.open()
    assert '1.0.17' in d.vlan[1]['untagged']
    assert '1.0.17' not in d.vlan[10]['tagged']
    d.vlan.add_interface(10,'1.0.17',tagged=True)
    assert '1.0.17' in d.vlan[1]['untagged']
    assert '1.0.17' in d.vlan[10]['tagged']
    d.close()


def test_delete_interface_4(dut, log_level):
    setup_dut(dut)
    dut.add_cmd({'cmd': 'show running-config'                 , 'state':0, 'action':'PRINT','args':["""
!
interface port1.0.1-1.0.16
switchport
switchport mode access
!
interface port1.0.17
switchport
switchport mode trunk
switchport trunk allowed vlan add 10
!
interface port1.0.18-1.0.50
switchport
switchport mode access
!
vlan database
vlan 10 name "marketing vlan"
vlan 10 state enable
vlan 7 name admin state enable
!
end
    """]})
    dut.add_cmd({'cmd': 'show vlan all'               , 'state':0, 'action':'PRINT','args':["""
VLAN ID  Name            Type    State   Member ports
                                         (u)-Untagged, (t)-Tagged
======= ================ ======= ======= ====================================
1       default          STATIC  ACTIVE  port1.0.1(u) port1.0.2(u) port1.0.3(u)
                                         port1.0.4(u) port1.0.5(u) port1.0.6(u)
                                         port1.0.7(u) port1.0.8(u) port1.0.9(u)
                                         port1.0.10(u) port1.0.11(u)
                                         port1.0.12(t) port1.0.13(u)
                                         port1.0.14(u) port1.0.15(u)
                                         port1.0.16(u) port1.0.17(u)
                                         port1.0.18(u) port1.0.19(u)
                                         port1.0.20(t) port1.0.21(u)
                                         port1.0.22(u) port1.0.23(u)
                                         port1.0.24(u) port1.0.25(u)
                                         port1.0.26(u) port1.0.27(u)
                                         port1.0.28(u) port1.0.29(u)
                                         port1.0.30(u) port1.0.31(u)
                                         port1.0.32(u) port1.0.33(u)
                                         port1.0.34(u) port1.0.35(u)
                                         port1.0.36(u) port1.0.37(u)
                                         port1.0.38(u) port1.0.39(u)
                                         port1.0.40(u) port1.0.41(u)
                                         port1.0.44(u) port1.0.45(u)
                                         port1.0.46(u) port1.0.47(u)
                                         port1.0.48(u) port1.0.49(u)
                                         port1.0.50(u)
7       VLAN0007         STATIC  ACTIVE  port1.0.28(t) port1.0.29(u)
20      "this is a long vlan name"
                         STATIC  ACTIVE  port1.0.42(t) port1.0.43(t)
10      VLAN0010         STATIC  ACTIVE  port1.0.28(t) port1.0.19(t)
                                         port1.0.15(t) port1.0.17(t)
"""]})
    dut.add_cmd({'cmd': 'interface port1.0.17'                   , 'state':0, 'action':'SET_PROMPT','args':['(config-if)#']})
    dut.add_cmd({'cmd': 'interface port1.0.17'                   , 'state':0, 'action':'SET_STATE','args':[1]})
    dut.add_cmd({'cmd': 'no switchport trunk allowed vlan 10'    , 'state':1, 'action':'SET_STATE','args':[2]})
    dut.add_cmd({'cmd': 'show running-config'                    , 'state':2, 'action':'PRINT','args':["""
!
interface port1.0.1-1.0.16
switchport
switchport mode access
!
interface port1.0.17
switchport
switchport mode trunk
!
interface port1.0.18-1.0.50
switchport
switchport mode access
!
vlan database
vlan 10 name "marketing vlan"
vlan 10 state enable
vlan 7 name admin state enable
!
end
    """]})
    dut.add_cmd({'cmd': 'show vlan all'                          , 'state':2, 'action':'PRINT','args':["""
VLAN ID  Name            Type    State   Member ports
                                         (u)-Untagged, (t)-Tagged
======= ================ ======= ======= ====================================
1       default          STATIC  ACTIVE  port1.0.1(u) port1.0.2(u) port1.0.3(u)
                                         port1.0.4(u) port1.0.5(u) port1.0.6(u)
                                         port1.0.7(u) port1.0.8(u) port1.0.9(u)
                                         port1.0.10(u) port1.0.11(u)
                                         port1.0.12(t) port1.0.13(u)
                                         port1.0.14(u) port1.0.15(u)
                                         port1.0.16(u) port1.0.17(u)
                                         port1.0.18(u) port1.0.19(u)
                                         port1.0.20(t) port1.0.21(u)
                                         port1.0.22(u) port1.0.23(u)
                                         port1.0.24(u) port1.0.25(u)
                                         port1.0.26(u) port1.0.27(u)
                                         port1.0.28(u) port1.0.29(u)
                                         port1.0.30(u) port1.0.31(u)
                                         port1.0.32(u) port1.0.33(u)
                                         port1.0.34(u) port1.0.35(u)
                                         port1.0.36(u) port1.0.37(u)
                                         port1.0.38(u) port1.0.39(u)
                                         port1.0.40(u) port1.0.41(u)
                                         port1.0.44(u) port1.0.45(u)
                                         port1.0.46(u) port1.0.47(u)
                                         port1.0.48(u) port1.0.49(u)
                                         port1.0.50(u)
7       VLAN0007         STATIC  ACTIVE  port1.0.28(t) port1.0.29(u)
20      "this is a long vlan name"
                         STATIC  ACTIVE  port1.0.42(t) port1.0.43(t)
10      VLAN0010         STATIC  ACTIVE  port1.0.28(t) port1.0.19(t)
                                         port1.0.15(t)
    """]})

    d=Device(host=dut.host,port=dut.port,protocol=dut.protocol, log_level=log_level)
    d.open()
    assert '1.0.17' in d.vlan[1]['untagged']
    assert '1.0.17' in d.vlan[10]['tagged']
    d.vlan.delete_interface(10,'1.0.17')
    # assert '1.0.17' in d.vlan[1]['untagged']
    # assert '1.0.17' not in d.vlan[10]['tagged']
    d.close()


def test_add_interface_5(dut, log_level):
    setup_dut(dut)
    dut.add_cmd({'cmd':'show running-config', 'state':0, 'action': 'PRINT','args':["""
!
interface port1.0.1-1.0.17
switchport
switchport mode access
!
interface port1.0.18
switchport
switchport mode trunk
!
interface port1.0.19-1.0.50
switchport
switchport mode access
!
vlan database
vlan 10 name "marketing vlan"
vlan 10 state enable
vlan 7 name admin state enable
!
end
    """]})
    dut.add_cmd({'cmd': 'show vlan all',                        'state':0, 'action':'PRINT','args':["""
VLAN ID  Name            Type    State   Member ports
                                         (u)-Untagged, (t)-Tagged
======= ================ ======= ======= ====================================
1       default          STATIC  ACTIVE  port1.0.1(u) port1.0.2(u) port1.0.3(u)
                                         port1.0.4(u) port1.0.5(u) port1.0.6(u)
                                         port1.0.7(u) port1.0.8(u) port1.0.9(u)
                                         port1.0.10(u) port1.0.11(u)
                                         port1.0.12(t) port1.0.13(u)
                                         port1.0.14(u) port1.0.15(u)
                                         port1.0.16(u) port1.0.17(u)
                                         port1.0.18(u) port1.0.19(u)
                                         port1.0.20(t) port1.0.21(u)
                                         port1.0.22(u) port1.0.23(u)
                                         port1.0.24(u) port1.0.25(u)
                                         port1.0.26(u) port1.0.27(u)
                                         port1.0.28(u) port1.0.29(u)
                                         port1.0.31(u)
                                         port1.0.32(u) port1.0.33(u)
                                         port1.0.34(u) port1.0.35(u)
                                         port1.0.36(u) port1.0.37(u)
                                         port1.0.38(u) port1.0.39(u)
                                         port1.0.40(u) port1.0.41(u)
                                         port1.0.44(u) port1.0.45(u)
                                         port1.0.46(u) port1.0.47(u)
                                         port1.0.48(u) port1.0.49(u)
                                         port1.0.50(u)
7       VLAN0007         STATIC  ACTIVE  port1.0.28(t) port1.0.29(u)
20      "this is a long vlan name"
                         STATIC  ACTIVE  port1.0.42(u) port1.0.43(t)
10      VLAN0010         STATIC  ACTIVE  port1.0.28(t)
    """]})
    dut.add_cmd({'cmd': 'interface port1.0.18'                , 'state':0, 'action':'SET_PROMPT','args':['(config-if)#']})
    dut.add_cmd({'cmd': 'interface port1.0.18'                , 'state':0, 'action':'SET_STATE','args':[1]})
    dut.add_cmd({'cmd': 'switchport trunk allowed vlan add 10', 'state':1, 'action':'SET_STATE','args':[2]})
    dut.add_cmd({'cmd': 'show running-config'                 , 'state':2, 'action':'PRINT','args':["""
!
interface port1.0.1-1.0.17
switchport
switchport mode access
!
interface port1.0.18
switchport
switchport mode trunk
switchport trunk allowed vlan add 10
!
interface port1.0.19-1.0.50
switchport
switchport mode access
!
vlan database
vlan 10 name "marketing vlan"
vlan 10 state enable
vlan 7 name admin state enable
!
end
    """]})
    dut.add_cmd({'cmd': 'show vlan all'                       , 'state':2, 'action':'PRINT','args':["""
VLAN ID  Name            Type    State   Member ports
                                         (u)-Untagged, (t)-Tagged
======= ================ ======= ======= ====================================
1       default          STATIC  ACTIVE  port1.0.1(u) port1.0.2(u) port1.0.3(u)
                                         port1.0.4(u) port1.0.5(u) port1.0.6(u)
                                         port1.0.7(u) port1.0.8(u) port1.0.9(u)
                                         port1.0.10(u) port1.0.11(u)
                                         port1.0.12(t) port1.0.13(u)
                                         port1.0.14(u) port1.0.15(u)
                                         port1.0.16(u) port1.0.17(u)
                                         port1.0.18(u) port1.0.19(u)
                                         port1.0.20(t) port1.0.21(u)
                                         port1.0.22(u) port1.0.23(u)
                                         port1.0.24(u) port1.0.25(u)
                                         port1.0.26(u) port1.0.27(u)
                                         port1.0.28(u) port1.0.29(u)
                                         port1.0.30(u) port1.0.31(u)
                                         port1.0.32(u) port1.0.33(u)
                                         port1.0.34(u) port1.0.35(u)
                                         port1.0.36(u) port1.0.37(u)
                                         port1.0.38(u) port1.0.39(u)
                                         port1.0.40(u) port1.0.41(u)
                                         port1.0.44(u) port1.0.45(u)
                                         port1.0.46(u) port1.0.47(u)
                                         port1.0.48(u) port1.0.49(u)
                                         port1.0.50(u)
7       VLAN0007         STATIC  ACTIVE  port1.0.28(t) port1.0.29(u)
20      "this is a long vlan name"
                         STATIC  ACTIVE  port1.0.42(t) port1.0.43(t)
10      VLAN0010         STATIC  ACTIVE  port1.0.28(t) port1.0.18(t)
"""]})
    d=Device(host=dut.host,port=dut.port,protocol=dut.protocol, log_level=log_level)
    d.open()
    assert '1.0.18' in d.vlan[1]['untagged']
    assert '1.0.18' not in d.vlan[10]['tagged']
    d.vlan.add_interface(10,'1.0.18',tagged=True)
    assert '1.0.18' in d.vlan[1]['untagged']
    assert '1.0.18' in d.vlan[10]['tagged']
    d.close()


def test_delete_interface_5(dut, log_level):
    setup_dut(dut)
    dut.add_cmd({'cmd': 'show running-config'                 , 'state':0, 'action':'PRINT','args':["""
!
interface port1.0.1-1.0.17
switchport
switchport mode access
!
interface port1.0.18
switchport
switchport mode trunk
switchport trunk allowed vlan add 10
!
interface port1.0.19-1.0.50
switchport
switchport mode access
!
vlan database
vlan 10 name "marketing vlan"
vlan 10 state enable
vlan 7 name admin state enable
!
end
    """]})
    dut.add_cmd({'cmd': 'show vlan all'                       , 'state':0, 'action':'PRINT','args':["""
VLAN ID  Name            Type    State   Member ports
                                         (u)-Untagged, (t)-Tagged
======= ================ ======= ======= ====================================
1       default          STATIC  ACTIVE  port1.0.1(u) port1.0.2(u) port1.0.3(u)
                                         port1.0.4(u) port1.0.5(u) port1.0.6(u)
                                         port1.0.7(u) port1.0.8(u) port1.0.9(u)
                                         port1.0.10(u) port1.0.11(u)
                                         port1.0.12(t) port1.0.13(u)
                                         port1.0.14(u) port1.0.15(u)
                                         port1.0.16(u) port1.0.17(u)
                                         port1.0.18(u) port1.0.19(u)
                                         port1.0.20(t) port1.0.21(u)
                                         port1.0.22(u) port1.0.23(u)
                                         port1.0.24(u) port1.0.25(u)
                                         port1.0.26(u) port1.0.27(u)
                                         port1.0.28(u) port1.0.29(u)
                                         port1.0.30(u) port1.0.31(u)
                                         port1.0.32(u) port1.0.33(u)
                                         port1.0.34(u) port1.0.35(u)
                                         port1.0.36(u) port1.0.37(u)
                                         port1.0.38(u) port1.0.39(u)
                                         port1.0.40(u) port1.0.41(u)
                                         port1.0.44(u) port1.0.45(u)
                                         port1.0.46(u) port1.0.47(u)
                                         port1.0.48(u) port1.0.49(u)
                                         port1.0.50(u)
7       VLAN0007         STATIC  ACTIVE  port1.0.28(t) port1.0.29(u)
20      "this is a long vlan name"
                         STATIC  ACTIVE  port1.0.42(t) port1.0.43(t)
10      VLAN0010         STATIC  ACTIVE  port1.0.28(t) port1.0.18(t)
"""]})
    dut.add_cmd({'cmd': 'interface port1.0.18'                   , 'state':0, 'action':'SET_PROMPT','args':['(config-if)#']})
    dut.add_cmd({'cmd': 'interface port1.0.18'                   , 'state':0, 'action':'SET_STATE','args':[1]})
    dut.add_cmd({'cmd': 'switchport trunk allowed vlan remove 10', 'state':1, 'action':'SET_STATE','args':[2]})
    dut.add_cmd({'cmd': 'show running-config'                    , 'state':2, 'action': 'PRINT','args':["""
!
interface port1.0.1-1.0.17
switchport
switchport mode access
!
interface port1.0.18
switchport
switchport mode trunk
!
interface port1.0.19-1.0.50
switchport
switchport mode access
!
vlan database
vlan 10 name "marketing vlan"
vlan 10 state enable
vlan 7 name admin state enable
!
end
    """]})
    dut.add_cmd({'cmd': 'show vlan all',                        'state':2, 'action':'PRINT','args':["""
VLAN ID  Name            Type    State   Member ports
                                         (u)-Untagged, (t)-Tagged
======= ================ ======= ======= ====================================
1       default          STATIC  ACTIVE  port1.0.1(u) port1.0.2(u) port1.0.3(u)
                                         port1.0.4(u) port1.0.5(u) port1.0.6(u)
                                         port1.0.7(u) port1.0.8(u) port1.0.9(u)
                                         port1.0.10(u) port1.0.11(u)
                                         port1.0.12(t) port1.0.13(u)
                                         port1.0.14(u) port1.0.15(u)
                                         port1.0.16(u) port1.0.17(u)
                                         port1.0.18(u) port1.0.19(u)
                                         port1.0.20(t) port1.0.21(u)
                                         port1.0.22(u) port1.0.23(u)
                                         port1.0.24(u) port1.0.25(u)
                                         port1.0.26(u) port1.0.27(u)
                                         port1.0.28(u) port1.0.29(u)
                                         port1.0.30(u) port1.0.31(u)
                                         port1.0.32(u) port1.0.33(u)
                                         port1.0.34(u) port1.0.35(u)
                                         port1.0.36(u) port1.0.37(u)
                                         port1.0.38(u) port1.0.39(u)
                                         port1.0.40(u) port1.0.41(u)
                                         port1.0.44(u) port1.0.45(u)
                                         port1.0.46(u) port1.0.47(u)
                                         port1.0.48(u) port1.0.49(u)
                                         port1.0.50(u)
7       VLAN0007         STATIC  ACTIVE  port1.0.28(t) port1.0.29(u)
20      "this is a long vlan name"
                         STATIC  ACTIVE  port1.0.42(u) port1.0.43(t)
10      VLAN0010         STATIC  ACTIVE  port1.0.28(t)
    """]})
    d=Device(host=dut.host,port=dut.port,protocol=dut.protocol, log_level=log_level)
    d.open()
    assert '1.0.18' in d.vlan[1]['untagged']
    assert '1.0.18' in d.vlan[10]['tagged']
    d.vlan.delete_interface(10,'1.0.18')
    assert '1.0.18' in d.vlan[1]['untagged']
    assert '1.0.18' not in d.vlan[10]['tagged']
    d.close()


def test_delete_vlan(dut, log_level):
    setup_dut(dut)
    dut.add_cmd({'cmd': 'show vlan all'               , 'state':0, 'action':'PRINT','args':["""
VLAN ID  Name            Type    State   Member ports
                                         (u)-Untagged, (t)-Tagged
======= ================ ======= ======= ====================================
1       default          STATIC  ACTIVE  port1.0.1(u) port1.0.2(u) port1.0.3(u)
                                         port1.0.4(u) port1.0.5(u) port1.0.6(u)
                                         port1.0.7(u) port1.0.8(u) port1.0.9(u)
                                         port1.0.10(u) port1.0.11(u)
                                         port1.0.12(t) port1.0.13(u)
                                         port1.0.14(u) port1.0.15(u)
                                         port1.0.16(u) port1.0.17(u)
                                         port1.0.18(u) port1.0.19(u)
                                         port1.0.20(t) port1.0.21(u)
                                         port1.0.22(u) port1.0.23(u)
                                         port1.0.24(u) port1.0.25(u)
                                         port1.0.26(u) port1.0.27(u)
                                         port1.0.28(u) port1.0.29(u)
                                         port1.0.30(u) port1.0.31(u)
                                         port1.0.32(u) port1.0.33(u)
                                         port1.0.34(u) port1.0.35(u)
                                         port1.0.36(u) port1.0.37(u)
                                         port1.0.38(u) port1.0.39(u)
                                         port1.0.40(u) port1.0.41(u)
                                         port1.0.44(u) port1.0.45(u)
                                         port1.0.46(u) port1.0.47(u)
                                         port1.0.48(u) port1.0.49(u)
                                         port1.0.50(u)
20      "this is a long vlan name"
                         STATIC  ACTIVE  port1.0.42(t) port1.0.43(t)
10      VLAN0010         STATIC  ACTIVE  port1.0.28(t) port1.0.29(u)
                                         port1.0.19(t) port1.0.15(t)
"""]})
    dut.add_cmd({'cmd': 'vlan database'                  , 'state':0, 'action':'SET_PROMPT','args':['(config-vlan)#']})
    dut.add_cmd({'cmd': 'vlan database'                  , 'state':0, 'action':'SET_STATE','args':[1]})
    dut.add_cmd({'cmd': 'no vlan 10',                      'state':1, 'action':'SET_STATE','args':[2]})
    dut.add_cmd({'cmd': 'show running-config',             'state':2, 'action':'PRINT','args':["""
!
vlan database
 vlan 20 name admin state enable mtu 1300
!
    """]})
    dut.add_cmd({'cmd':'show vlan all',         'state':2, 'action':'PRINT','args':["""
VLAN ID  Name            Type    State   Member ports
                                         (u)-Untagged, (t)-Tagged
======= ================ ======= ======= ====================================
1       default          STATIC  ACTIVE  port1.0.1(u) port1.0.2(u) port1.0.3(u)
                                         port1.0.4(u) port1.0.5(u) port1.0.6(u)
                                         port1.0.7(u) port1.0.8(u) port1.0.9(u)
                                         port1.0.10(u) port1.0.11(u)
                                         port1.0.12(t) port1.0.13(u)
                                         port1.0.14(u) port1.0.15(u)
                                         port1.0.16(u) port1.0.17(u)
                                         port1.0.18(u) port1.0.19(u)
                                         port1.0.20(t) port1.0.21(u)
                                         port1.0.22(u) port1.0.23(u)
                                         port1.0.24(u) port1.0.25(u)
                                         port1.0.26(u) port1.0.27(u)
                                         port1.0.28(u) port1.0.29(u)
                                         port1.0.30(u) port1.0.31(u)
                                         port1.0.32(u) port1.0.33(u)
                                         port1.0.34(u) port1.0.35(u)
                                         port1.0.36(u) port1.0.37(u)
                                         port1.0.38(u) port1.0.39(u)
                                         port1.0.40(u) port1.0.41(u)
                                         port1.0.44(u) port1.0.45(u)
                                         port1.0.46(u) port1.0.47(u)
                                         port1.0.48(u) port1.0.49(u)
                                         port1.0.50(u)
20      "this is a long vlan name"
                         STATIC  ACTIVE  port1.0.42(t) port1.0.43(t)
"""]})
    d=Device(host=dut.host,port=dut.port,protocol=dut.protocol, log_level=log_level)
    d.open()
    d.vlan.delete(10)
    with pytest.raises(KeyError):
        d.vlan[10]
    d.close()
