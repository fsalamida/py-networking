import pytest
from pynetworking.Device import Device


def setup_dut(dut):
    dut.reset()
    dut.add_cmd({'cmd': 'show version', 'state': -1, 'action': 'PRINT', 'args': ["""
AlliedWare Plus (TM) 5.4.2 09/25/13 12:57:26

Build name : x600-5.4.2-3.14.rel
Build date : Wed Sep 25 12:57:26 NZST 2013
Build type : RELEASE
    """]})


def test_get_vlan(dut, log_level, use_mock):
    setup_dut(dut)
    dut.add_cmd({'cmd': 'show running-config', 'state': 0, 'action': 'PRINT', 'args': ["""
!
interface port1.0.1-1.0.50
switchport
switchport mode access
!
vlan database
vlan 7,10,20
exit
interface vlan 20
name "this is a long vlan name"
exit
interface vlan 1
ip address 10.17.39.253 255.255.255.0
name default
exit
!
end
    """]})
    dut.add_cmd({'cmd': 'show vlan all', 'state': 0, 'action': 'PRINT', 'args': ["""
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
    d = Device(host=dut.host, port=dut.port, protocol=dut.protocol, log_level=log_level, mock=use_mock)
    d.open()
    if dut.mode == 'emulated':
        assert d.vlan[1] == {"tagged": ("1.0.12", "1.0.20"),
                             "current state": "ACTIVE", "type": "STATIC", "name": "default",
                             "untagged": ("1.0.1", "1.0.2", "1.0.3", "1.0.4", "1.0.5", "1.0.6", "1.0.7", "1.0.8", "1.0.9", "1.0.10",
                                          "1.0.11", "1.0.13", "1.0.14", "1.0.15", "1.0.16", "1.0.17", "1.0.18", "1.0.19",
                                          "1.0.21", "1.0.22", "1.0.23", "1.0.24", "1.0.25", "1.0.26", "1.0.27", "1.0.28", "1.0.29",
                                          "1.0.31", "1.0.32", "1.0.33", "1.0.34", "1.0.35", "1.0.36", "1.0.37", "1.0.38", "1.0.39",
                                          "1.0.40", "1.0.41", "1.0.44", "1.0.45", "1.0.46", "1.0.47", "1.0.48", "1.0.49", "1.0.50")
                             }
        assert d.vlan[7] == {"current state": "ACTIVE", "untagged": ("1.0.29",), "type": "STATIC", "name": "VLAN0007", "tagged": ("1.0.28",)}
        assert d.vlan[20] == {"current state": "ACTIVE", "untagged": ("1.0.42",), "type": "STATIC", "name": "this is a long vlan name", "tagged": ("1.0.43",)}
        assert d.vlan[10] == {"current state": "ACTIVE", "untagged": ("1.0.29",), "type": "STATIC", "name": "VLAN0010",
                              "tagged": ("1.0.28", "1.0.19", "1.0.30")}
    else:
        assert d.vlan[1]['tagged'] == ()
        assert d.vlan[1]['untagged'] != ()
        assert d.vlan[1]['name'] == 'default'
        str(d.vlan)
    with pytest.raises(KeyError) as excinfo:
        d.vlan[1111]
    assert 'vlan id 1111 does not exist' in excinfo.value
    d.close()


def test_vlan_dashed_list(dut, log_level, use_mock):
    if dut.mode != 'emulated':
        pytest.skip("only on emulated")
    output_show_rcfg = ["""
!
interface port1.0.1-1.0.50
 switchport
 switchport mode access
!
vlan database
vlan 21-23,25,30-33
exit
interface vlan 21
name "twentyone"
exit
interface vlan 22
name "zweiundzwanzig"
exit
interface vlan 23
name "vingttrois"
exit
interface vlan 25
name "venticinque"
exit
interface vlan 32
name "telnet vlan"
exit
interface vlan 1
ip address 10.17.39.253 255.255.255.0
name default
exit
!
end
    """]
    output_show_vlan = ["""
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
21      twentyone        STATIC  ACTIVE  port1.0.42(t) port1.0.43(t)
22      zweiundzwanzig   STATIC  ACTIVE  port1.0.42(t) port1.0.43(t)
23      vingttrois       STATIC  ACTIVE  port1.0.42(t) port1.0.43(t)
25      venticinque      STATIC  ACTIVE  port1.0.42(t) port1.0.43(t)
30      VLAN0030         STATIC  SUSPEND
31      VLAN0031         STATIC  SUSPEND
32      "telnet vlan"    STATIC  SUSPEND
33      VLAN0033         STATIC  SUSPEND
    """]

    setup_dut(dut)
    dut.add_cmd({'cmd': 'show running-config', 'state': 0, 'action': 'PRINT', 'args': output_show_rcfg})
    dut.add_cmd({'cmd': 'show vlan all', 'state': 0, 'action': 'PRINT', 'args': output_show_vlan})
    d = Device(host=dut.host, port=dut.port, protocol=dut.protocol, log_level=log_level, mock=use_mock)
    d.open()
    assert '21' in d.vlan
    assert d.vlan[21]['name'] == 'twentyone'
    assert ('22', {'current state': 'ACTIVE', 'name': 'zweiundzwanzig', 'untagged': (), 'tagged': ('1.0.42', '1.0.43'), 'type': 'STATIC'}) in d.vlan.items()
    with pytest.raises(TypeError) as excinfo:
        d.vlan[d.vlan]
    assert 'invalid argument type' in excinfo.value
    str(d.vlan)
    assert '23' in d.vlan
    assert d.vlan[23]['name'] == 'vingttrois'
    assert '24' not in d.vlan
    assert '25' in d.vlan
    assert d.vlan[25]['name'] == 'venticinque'
    assert '26' not in d.vlan
    assert '27' not in d.vlan
    assert '28' not in d.vlan
    assert '29' not in d.vlan
    assert '30' in d.vlan
    assert d.vlan[30]['name'] == 'VLAN0030'
    assert '31' in d.vlan
    assert '32' in d.vlan
    assert d.vlan[32]['name'] == 'telnet vlan'
    assert '33' in d.vlan
    d.close()


def test_create_vlan(dut, log_level, use_mock):
    output_rc_0 = ["""
!
interface port1.0.1-1.0.50
switchport
switchport mode access
!
interface vlan 1
ip address 10.17.39.253 255.255.255.0
exit
!
end
    """]
    output_va_0 = ["""
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
    """]
    output_rc_1 = ["""
!
interface port1.0.1-1.0.50
switchport
switchport mode access
!
interface vlan 1
ip address 10.17.39.253 255.255.255.0
exit
!
vlan database
vlan 10 name "this is a long vlan name" state enable mtu 1200
!
end
"""]
    output_va_1 = ["""
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
10      "this is a long vlan name"
                         STATIC  ACTIVE
"""]
    output_rc_2 = ["""
!
interface port1.0.1-1.0.50
switchport
switchport mode access
!
interface vlan 1
ip address 10.17.39.253 255.255.255.0
exit
!
vlan database
vlan 10 name "this is a long vlan name" state enable mtu 1200
vlan 20 name admin state enable mtu 1300
!
end
"""]
    output_va_2 = ["""
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
10      "this is a long vlan name"
                         STATIC  ACTIVE
20      admin            STATIC  ACTIVE
"""]
    output_rc_3 = ["""
!
interface port1.0.1-1.0.50
switchport
switchport mode access
!
interface vlan 1
ip address 10.17.39.253 255.255.255.0
exit
!
vlan database
vlan 10 name "this is a long vlan name" state enable mtu 1200
vlan 20 name admin state enable mtu 1300
vlan 99 state disable
!
end
"""]
    output_va_3 = ["""
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
10      "this is a long vlan name"
                         STATIC  ACTIVE
20      admin            STATIC  ACTIVE
99      VLAN0099         STATIC  SUSPEND
"""]

    setup_dut(dut)

    dut.add_cmd({'cmd': 'show running-config', 'state': 0, 'action': 'PRINT', 'args': output_rc_0})
    dut.add_cmd({'cmd': 'show vlan all', 'state': 0, 'action': 'PRINT', 'args': output_va_0})
    dut.add_cmd({'cmd': 'vlan database', 'state': 0, 'action': 'SET_PROMPT', 'args': ['(config-vlan)#']})
    dut.add_cmd({'cmd': 'vlan database', 'state': 0, 'action': 'SET_STATE', 'args': [1]})
    dut.add_cmd({'cmd': 'vlan 10 name "this is a long vlan name"', 'state': 1, 'action': 'SET_STATE', 'args': [2]})
    dut.add_cmd({'cmd': 'vlan 10 mtu 1200', 'state': 2, 'action': 'SET_STATE', 'args': [3]})
    dut.add_cmd({'cmd': 'show running-config', 'state': 3, 'action': 'PRINT', 'args': output_rc_1})
    dut.add_cmd({'cmd': 'show vlan all', 'state': 3, 'action': 'PRINT', 'args': output_va_1})
    dut.add_cmd({'cmd': 'vlan database', 'state': 3, 'action': 'SET_PROMPT', 'args': ['(config-vlan)#']})
    dut.add_cmd({'cmd': 'vlan database', 'state': 3, 'action': 'SET_STATE', 'args': [4]})
    dut.add_cmd({'cmd': 'vlan 20 name admin', 'state': 4, 'action': 'SET_STATE', 'args': [5]})
    dut.add_cmd({'cmd': 'vlan 20 mtu 1300', 'state': 5, 'action': 'SET_STATE', 'args': [6]})
    dut.add_cmd({'cmd': 'show running-config', 'state': 6, 'action': 'PRINT', 'args': output_rc_2})
    dut.add_cmd({'cmd': 'show vlan all', 'state': 6, 'action': 'PRINT', 'args': output_va_2})
    dut.add_cmd({'cmd': 'vlan database', 'state': 6, 'action': 'SET_PROMPT', 'args': ['(config-vlan)#']})
    dut.add_cmd({'cmd': 'vlan database', 'state': 6, 'action': 'SET_STATE', 'args': [7]})
    dut.add_cmd({'cmd': 'vlan 99 state disable', 'state': 7, 'action': 'SET_STATE', 'args': [8]})
    dut.add_cmd({'cmd': 'show running-config', 'state': 8, 'action': 'PRINT', 'args': output_rc_3})
    dut.add_cmd({'cmd': 'show vlan all', 'state': 8, 'action': 'PRINT', 'args': output_va_3})

    d = Device(host=dut.host, port=dut.port, protocol=dut.protocol, log_level=log_level, mock=use_mock)
    d.open()
    d.vlan.create(10, name='this is a long vlan name', mtu=1200)
    assert d.vlan[10] == {'current state': 'ACTIVE', 'tagged': (), 'type': 'STATIC', 'untagged': (), 'state': 'enable',
                          'name': 'this is a long vlan name', 'mtu': 1200}
    with pytest.raises(KeyError) as excinfo:
        d.vlan.update(30, name='does not exist')
    assert '[30] vlans do not exist' in excinfo.value
    with pytest.raises(ValueError):
        d.vlan.update(10, state='idle')
    assert 'idle state makes no sense for vlans'
    d.vlan.create(20, name='admin', mtu=1300)
    assert d.vlan[20] == {'current state': 'ACTIVE', 'tagged': (), 'type': 'STATIC', 'untagged': (), 'state': 'enable', 'name': 'admin', 'mtu': 1300}
    d.vlan.create(99, state='disable')
    assert d.vlan[99]['state'] == 'disable'
    d.close()


def test_crud_vlan(dut, log_level, use_mock):
    output_rc_0 = ["""
!
interface port1.0.1-1.0.50
 switchport
 switchport mode access
!
interface vlan 1
 ip address 10.17.39.253 255.255.255.0
!
vlan database
 vlan 7 state enable
!
end
    """]
    output_va_0 = ["""
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
                                         port1.0.30(t) port1.0.31(u)
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
"""]
    output_rc_1 = ["""
!
interface port1.0.1-1.0.50
 switchport
 switchport mode access
!
interface vlan 1
 ip address 10.17.39.253 255.255.255.0
!
vlan database
 vlan 7 state enable
 vlan 30 name vlan_name state enable mtu 1300
!
end
"""]
    output_va_1 = ["""
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
30      vlan_name        STATIC  ACTIVE
"""]
    output_rc_2 = ["""
!
interface port1.0.1-1.0.50
 switchport
 switchport mode access
!
interface vlan 1
 ip address 10.17.39.253 255.255.255.0
!
vlan database
 vlan 7 state enable
 vlan 30 name "vlan name" state enable mtu 1400
!
end
    """]
    output_va_2 = ["""
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
30      "vlan name"      STATIC  ACTIVE  port1.0.42(u) port1.0.43(t)
"""]

    setup_dut(dut)

    dut.add_cmd({'cmd': 'show running-config', 'state': 0, 'action': 'PRINT', 'args': output_rc_0})
    dut.add_cmd({'cmd': 'show vlan all', 'state': 0, 'action': 'PRINT', 'args': output_va_0})
    dut.add_cmd({'cmd': 'vlan database', 'state': 0, 'action': 'SET_PROMPT', 'args': ['(config-vlan)#']})
    dut.add_cmd({'cmd': 'vlan database', 'state': 0, 'action': 'SET_STATE', 'args': [1]})
    dut.add_cmd({'cmd': 'vlan 30 name vlan_name', 'state': 1, 'action': 'SET_STATE', 'args': [2]})
    dut.add_cmd({'cmd': 'vlan 30 mtu 1300', 'state': 2, 'action': 'SET_STATE', 'args': [3]})
    dut.add_cmd({'cmd': 'show running-config', 'state': 3, 'action': 'PRINT', 'args': output_rc_1})
    dut.add_cmd({'cmd': 'show vlan all', 'state': 3, 'action': 'PRINT', 'args': output_va_1})
    dut.add_cmd({'cmd': 'vlan database', 'state': 3, 'action': 'SET_PROMPT', 'args': ['(config-vlan)#']})
    dut.add_cmd({'cmd': 'vlan database', 'state': 3, 'action': 'SET_STATE', 'args': [4]})
    dut.add_cmd({'cmd': 'vlan 30 name "vlan name"', 'state': 4, 'action': 'SET_STATE', 'args': [5]})
    dut.add_cmd({'cmd': 'vlan 30 mtu 1400', 'state': 5, 'action': 'SET_STATE', 'args': [6]})
    dut.add_cmd({'cmd': 'show running-config', 'state': 6, 'action': 'PRINT', 'args': output_rc_2})
    dut.add_cmd({'cmd': 'show vlan all', 'state': 6, 'action': 'PRINT', 'args': output_va_2})
    dut.add_cmd({'cmd': 'vlan database', 'state': 6, 'action': 'SET_PROMPT', 'args': ['(config-vlan)#']})
    dut.add_cmd({'cmd': 'vlan database', 'state': 6, 'action': 'SET_STATE', 'args': [7]})
    dut.add_cmd({'cmd': 'no vlan 30', 'state': 7, 'action': 'SET_STATE', 'args': [8]})
    dut.add_cmd({'cmd': 'show running-config', 'state': 8, 'action': 'PRINT', 'args': output_rc_0})
    dut.add_cmd({'cmd': 'show vlan all', 'state': 8, 'action': 'PRINT', 'args': output_va_0})

    d = Device(host=dut.host, port=dut.port, protocol=dut.protocol, log_level=log_level, mock=use_mock)
    d.open()
    assert '30' not in d.vlan
    d.vlan.create(30, mtu=1300, name='vlan_name')
    assert d.vlan[30]['mtu'] == 1300
    assert d.vlan[30]['name'] == 'vlan_name'
    d.vlan.update(30, mtu=1400, name='vlan name')
    assert d.vlan[30]['mtu'] == 1400
    assert d.vlan[30]['name'] == 'vlan name'
    d.vlan.delete(30)
    assert '30' not in d.vlan
    with pytest.raises(KeyError):
        d.vlan[30]
    d.close()


def test_add_and_delete_interface_1(dut, log_level, use_mock):
    output_rc_0 = ["""
!
interface port1.0.1-1.0.50
 switchport
 switchport mode access
!
interface vlan 1
 ip address 10.17.39.253 255.255.255.0
!
vlan database
 vlan 10 state enable
!
end
    """]
    output_va_0 = ["""
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
    """]
    output_rc_1 = ["""
!
interface port1.0.1-1.0.13
 switchport
 switchport mode access
!
interface port1.0.14
 switchport
 switchport mode access
 switchport access vlan 10
!
interface port1.0.15-1.0.50
 switchport
 switchport mode access
!
interface vlan 1
 ip address 10.17.39.253 255.255.255.0
!
vlan database
 vlan 10 state enable
!
end
"""]
    output_va_1 = ["""
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
"""]

    setup_dut(dut)

    dut.add_cmd({'cmd': 'show running-config', 'state': 0, 'action': 'PRINT', 'args': output_rc_0})
    dut.add_cmd({'cmd': 'show vlan all', 'state': 0, 'action': 'PRINT', 'args': output_va_0})
    dut.add_cmd({'cmd': 'interface port1.0.14', 'state': 0, 'action': 'SET_PROMPT', 'args': ['(config-if)#']})
    dut.add_cmd({'cmd': 'interface port1.0.14', 'state': 0, 'action': 'SET_STATE', 'args': [1]})
    dut.add_cmd({'cmd': 'switchport access vlan 10', 'state': 1, 'action': 'SET_STATE', 'args': [2]})
    dut.add_cmd({'cmd': 'show running-config', 'state': 2, 'action': 'PRINT', 'args': output_rc_1})
    dut.add_cmd({'cmd': 'show vlan all', 'state': 2, 'action': 'PRINT', 'args': output_va_1})
    dut.add_cmd({'cmd': 'interface port1.0.14', 'state': 2, 'action': 'SET_PROMPT', 'args': ['(config-if)#']})
    dut.add_cmd({'cmd': 'interface port1.0.14', 'state': 2, 'action': 'SET_STATE', 'args': [3]})
    dut.add_cmd({'cmd': 'no switchport access vlan', 'state': 3, 'action': 'SET_STATE', 'args': [4]})
    dut.add_cmd({'cmd': 'show running-config', 'state': 4, 'action': 'PRINT', 'args': output_rc_0})
    dut.add_cmd({'cmd': 'show vlan all', 'state': 4, 'action': 'PRINT', 'args': output_va_0})

    d = Device(host=dut.host, port=dut.port, protocol=dut.protocol, log_level=log_level, mock=use_mock)
    d.open()
    d.vlan.add_interface(10, '1.0.14')
    assert '1.0.14' in d.vlan[10]['untagged']
    assert '1.0.14' not in d.vlan[1]['untagged']
    assert d.vlan._interface_config['1.0.14']['switchport mode'] == 'access'
    with pytest.raises(ValueError) as excinfo:
        d.vlan.add_interface(11, '1.0.20')
    assert '11 is not a valid vlan id' in excinfo.value
    with pytest.raises(ValueError) as excinfo:
        d.vlan.add_interface(10, '1.0.51')
    assert '1.0.51 is not a valid interface' in excinfo.value
    d.vlan.delete_interface(10, '1.0.14')
    assert '1.0.14' not in d.vlan[10]['untagged']
    assert '1.0.14' in d.vlan[1]['untagged']
    with pytest.raises(ValueError) as excinfo:
        d.vlan.delete_interface(11, '1.0.20')
    assert '11 is not a valid vlan id' in excinfo.value
    with pytest.raises(ValueError) as excinfo:
        d.vlan.delete_interface(10, '1.0.51')
    assert '1.0.51 is not a valid interface' in excinfo.value
    d.close()


def test_add_and_delete_interface_2(dut, log_level, use_mock):
    output_rc_0 = ["""
!
interface port1.0.1-1.0.50
 switchport
 switchport mode access
!
interface vlan 1
 ip address 10.17.39.253 255.255.255.0
!
vlan database
 vlan 7 name admin state enable
 vlan 10 state enable
 vlan 20 "this is a long vlan name" state enable
!
end
"""]
    output_va_0 = ["""
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
7       VLAN0007         STATIC  ACTIVE  port1.0.28(t) port1.0.43(u)
20      "this is a long vlan name"
                         STATIC  ACTIVE  port1.0.42(u) port1.0.29(t)
10      VLAN0010         STATIC  ACTIVE  port1.0.28(t) port1.0.29(t)
                                         port1.0.19(t)
"""]
    output_rc_1 = ["""
!
interface port1.0.1-1.0.14
 switchport
 switchport mode access
!
interface port1.0.15
 switchport mode trunk
 switchport trunk allowed vlan add 10
!
interface port1.0.16-1.0.50
 switchport
 switchport mode access
!
interface vlan 1
 ip address 10.17.39.253 255.255.255.0
!
vlan database
 vlan 7 name admin state enable
 vlan 10 state enable
 vlan 20 "this is a long vlan name" state enable
!
end
"""]
    output_va_1 = ["""
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
7       VLAN0007         STATIC  ACTIVE  port1.0.28(t) port1.0.43(u)
20      "this is a long vlan name"
                         STATIC  ACTIVE  port1.0.42(u) port1.0.29(t)
10      VLAN0010         STATIC  ACTIVE  port1.0.28(t) port1.0.29(t)
                                         port1.0.19(t) port1.0.15(t)
"""]

    setup_dut(dut)

    dut.add_cmd({'cmd': 'show running-config', 'state': 0, 'action': 'PRINT', 'args': output_rc_0})
    dut.add_cmd({'cmd': 'show vlan all', 'state': 0, 'action': 'PRINT', 'args': output_va_0})
    dut.add_cmd({'cmd': 'interface port1.0.15', 'state': 0, 'action': 'SET_PROMPT', 'args': ['(config-if)#']})
    dut.add_cmd({'cmd': 'interface port1.0.15', 'state': 0, 'action': 'SET_STATE', 'args': [1]})
    dut.add_cmd({'cmd': 'switchport mode trunk', 'state': 1, 'action': 'SET_STATE', 'args': [2]})
    dut.add_cmd({'cmd': 'switchport trunk allowed vlan add 10', 'state': 2, 'action': 'SET_STATE', 'args': [3]})
    dut.add_cmd({'cmd': 'show running-config', 'state': 3, 'action': 'PRINT', 'args': output_rc_1})
    dut.add_cmd({'cmd': 'show vlan all', 'state': 3, 'action': 'PRINT', 'args': output_va_1})
    dut.add_cmd({'cmd': 'interface port1.0.15', 'state': 3, 'action': 'SET_PROMPT', 'args': ['(config-if)#']})
    dut.add_cmd({'cmd': 'interface port1.0.15', 'state': 3, 'action': 'SET_STATE', 'args': [4]})
    dut.add_cmd({'cmd': 'switchport trunk allowed vlan remove 10', 'state': 4, 'action': 'SET_STATE', 'args': [5]})
    dut.add_cmd({'cmd': 'show running-config', 'state': 5, 'action': 'PRINT', 'args': output_rc_0})
    dut.add_cmd({'cmd': 'show vlan all', 'state': 5, 'action': 'PRINT', 'args': output_va_0})

    d = Device(host=dut.host, port=dut.port, protocol=dut.protocol, log_level=log_level, mock=use_mock)
    d.open()
    assert '1.0.15' in d.vlan[1]['untagged']
    assert '1.0.15' not in d.vlan[10]['tagged']
    d.vlan.add_interface(10, '1.0.15', tagged=True)
    assert '1.0.15' in d.vlan[1]['untagged']
    assert '1.0.15' in d.vlan[10]['tagged']
    assert d.vlan._interface_config['1.0.15']['switchport mode'] == 'trunk'
    d.vlan.delete_interface(10, '1.0.15')
    assert '1.0.15' in d.vlan[1]['untagged']
    assert '1.0.15' not in d.vlan[10]['tagged']
    d.close()


def test_add_and_delete_interface_3(dut, log_level, use_mock):
    output_rc_0 = ["""
!
interface port1.0.1-1.0.15
 switchport
 switchport mode access
!
interface port1.0.16
 switchport
 switchport mode trunk
!
interface port1.0.17-1.0.50
 switchport
 switchport mode access
!
interface vlan 1
 ip address 10.17.39.253 255.255.255.0
!
vlan database
 vlan 10 name "marketing vlan"
 vlan 10 state enable
 vlan 7 name admin state enable
!
end
"""]
    output_va_0 = ["""
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
7       VLAN0007         STATIC  ACTIVE  port1.0.28(t)
20      "this is a long vlan name"
                         STATIC  ACTIVE  port1.0.42(t) port1.0.43(t)
10      VLAN0010         STATIC  ACTIVE  port1.0.28(t) port1.0.19(t)
                                         port1.0.15(t)
"""]
    output_rc_1 = ["""
!
interface port1.0.1-1.0.15
 switchport
 switchport mode access
!
interface port1.0.16
 switchport
 switchport mode trunk
 switchport trunk native vlan 10
!
interface port1.0.17-1.0.50
 switchport
 switchport mode access
!
interface vlan 1
 ip address 10.17.39.253 255.255.255.0
!
vlan database
 vlan 10 name "marketing vlan"
 vlan 10 state enable
 vlan 7 name admin state enable
!
end
"""]
    output_va_1 = ["""
VLAN ID  Name            Type    State   Member ports
                                         (u)-Untagged, (t)-Tagged
======= ================ ======= ======= ====================================
1       default          STATIC  ACTIVE  port1.0.1(u) port1.0.2(u) port1.0.3(u)
                                         port1.0.4(u) port1.0.5(u) port1.0.6(u)
                                         port1.0.7(u) port1.0.8(u) port1.0.9(u)
                                         port1.0.10(u) port1.0.11(u)
                                         port1.0.12(t) port1.0.13(u)
                                         port1.0.14(u) port1.0.15(u)
                                         port1.0.17(u) port1.0.18(u)
                                         port1.0.19(u) port1.0.20(t)
                                         port1.0.21(u) port1.0.22(u)
                                         port1.0.23(u) port1.0.24(u)
                                         port1.0.25(u) port1.0.26(u)
                                         port1.0.27(u) port1.0.28(u)
                                         port1.0.29(u) port1.0.30(u)
                                         port1.0.31(u) port1.0.32(u)
                                         port1.0.33(u) port1.0.34(u)
                                         port1.0.35(u) port1.0.36(u)
                                         port1.0.37(u) port1.0.38(u)
                                         port1.0.39(u) port1.0.40(u)
                                         port1.0.41(u) port1.0.42(u)
                                         port1.0.43(u) port1.0.44(u)
                                         port1.0.45(u) port1.0.46(u)
                                         port1.0.47(u) port1.0.48(u)
                                         port1.0.49(u) port1.0.50(u)
7       VLAN0007         STATIC  ACTIVE  port1.0.28(t)
20      "this is a long vlan name"
                         STATIC  ACTIVE  port1.0.42(t) port1.0.43(t)
10      VLAN0010         STATIC  ACTIVE  port1.0.28(t) port1.0.19(t)
                                         port1.0.15(t) port1.0.16(u)
"""]

    setup_dut(dut)

    dut.add_cmd({'cmd': 'show running-config', 'state': 0, 'action': 'PRINT', 'args': output_rc_0})
    dut.add_cmd({'cmd': 'show vlan all', 'state': 0, 'action': 'PRINT', 'args': output_va_0})
    dut.add_cmd({'cmd': 'interface port1.0.16', 'state': 0, 'action': 'SET_PROMPT', 'args': ['(config-if)#']})
    dut.add_cmd({'cmd': 'interface port1.0.16', 'state': 0, 'action': 'SET_STATE', 'args': [1]})
    dut.add_cmd({'cmd': 'switchport trunk native vlan 10', 'state': 1, 'action': 'SET_STATE', 'args': [2]})
    dut.add_cmd({'cmd': 'show running-config', 'state': 2, 'action': 'PRINT', 'args': output_rc_1})
    dut.add_cmd({'cmd': 'show vlan all', 'state': 2, 'action': 'PRINT', 'args': output_va_1})
    dut.add_cmd({'cmd': 'interface port1.0.16', 'state': 2, 'action': 'SET_PROMPT', 'args': ['(config-if)#']})
    dut.add_cmd({'cmd': 'interface port1.0.16', 'state': 2, 'action': 'SET_STATE', 'args': [3]})
    dut.add_cmd({'cmd': 'switchport trunk native vlan none', 'state': 3, 'action': 'SET_STATE', 'args': [4]})
    dut.add_cmd({'cmd': 'show running-config', 'state': 4, 'action': 'PRINT', 'args': output_rc_0})
    dut.add_cmd({'cmd': 'show vlan all', 'state': 4, 'action': 'PRINT', 'args': output_va_0})

    d = Device(host=dut.host, port=dut.port, protocol=dut.protocol, log_level=log_level, mock=use_mock)
    d.open()
    assert '1.0.16' in d.vlan[1]['untagged']
    assert '1.0.16' not in d.vlan[10]['untagged']
    d.vlan.add_interface(10, '1.0.16')
    assert '1.0.16' not in d.vlan[1]['untagged']
    assert '1.0.16' in d.vlan[10]['untagged']
    d.vlan.delete_interface(10, '1.0.16')
    assert '1.0.16' in d.vlan[1]['untagged']
    assert '1.0.16' not in d.vlan[10]['untagged']
    d.close()


def test_add_and_delete_interface_4(dut, log_level, use_mock):
    output_rc_0 = ["""
!
interface port1.0.1-1.0.16
 switchport
 switchport mode access
!
interface port1.0.17
 switchport
 switchport mode trunk
 switchport trunk allowed vlan add 7
!
interface port1.0.18-1.0.50
 switchport
 switchport mode access
!
interface vlan 1
 ip address 10.17.39.253 255.255.255.0
!
vlan database
 vlan 7 name vlan_vid
 vlan 10 name vlan_data
!
end
"""]
    output_va_0 = ["""
VLAN ID  Name            Type    State   Member ports
                                         (u)-Untagged, (t)-Tagged
======= ================ ======= ======= ====================================
1       default          STATIC  ACTIVE  port1.0.1(u) port1.0.2(u) port1.0.3(u)
                                         port1.0.4(u) port1.0.5(u) port1.0.6(u)
                                         port1.0.7(u) port1.0.8(u) port1.0.9(u)
                                         port1.0.10(u) port1.0.11(u)
                                         port1.0.12(t) port1.0.13(u)
                                         port1.0.14(u) port1.0.15(u)
                                         port1.0.16(u)
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
7       vlan_vid         STATIC  ACTIVE  port1.0.17(t) port1.0.28(t)
10      vlan_data        STATIC  ACTIVE  port1.0.28(t)
"""]

    output_rc_1 = ["""
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
interface vlan 1
 ip address 10.17.39.253 255.255.255.0
!
vlan database
 vlan 7 name vlan_vid
 vlan 10 name vlan_data
!
end
"""]
    output_va_1 = ["""
VLAN ID  Name            Type    State   Member ports
                                         (u)-Untagged, (t)-Tagged
======= ================ ======= ======= ====================================
1       default          STATIC  ACTIVE  port1.0.1(u) port1.0.2(u) port1.0.3(u)
                                         port1.0.4(u) port1.0.5(u) port1.0.6(u)
                                         port1.0.7(u) port1.0.8(u) port1.0.9(u)
                                         port1.0.10(u) port1.0.11(u)
                                         port1.0.12(t) port1.0.13(u)
                                         port1.0.14(u) port1.0.15(u)
                                         port1.0.16(u)
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
7       vlan_vid         STATIC  ACTIVE  port1.0.28(t)
10      vlan_data        STATIC  ACTIVE  port1.0.17(t) port1.0.28(t)
"""]

    setup_dut(dut)

    dut.add_cmd({'cmd': 'show running-config', 'state': 0, 'action': 'PRINT', 'args': output_rc_0})
    dut.add_cmd({'cmd': 'show vlan all', 'state': 0, 'action': 'PRINT', 'args': output_va_0})
    dut.add_cmd({'cmd': 'interface port1.0.17', 'state': 0, 'action': 'SET_PROMPT', 'args': ['(config-if)#']})
    dut.add_cmd({'cmd': 'interface port1.0.17', 'state': 0, 'action': 'SET_STATE', 'args': [1]})
    dut.add_cmd({'cmd': 'switchport trunk allowed vlan add 10', 'state': 1, 'action': 'SET_STATE', 'args': [2]})
    dut.add_cmd({'cmd': 'show running-config', 'state': 2, 'action': 'PRINT', 'args': output_rc_1})
    dut.add_cmd({'cmd': 'show vlan all', 'state': 2, 'action': 'PRINT', 'args': output_va_1})
    dut.add_cmd({'cmd': 'interface port1.0.17', 'state': 2, 'action': 'SET_PROMPT', 'args': ['(config-if)#']})
    dut.add_cmd({'cmd': 'interface port1.0.17', 'state': 2, 'action': 'SET_STATE', 'args': [3]})
    dut.add_cmd({'cmd': 'switchport trunk allowed vlan remove 10', 'state': 3, 'action': 'SET_STATE', 'args': [4]})
    dut.add_cmd({'cmd': 'show running-config', 'state': 4, 'action': 'PRINT', 'args': output_rc_0})
    dut.add_cmd({'cmd': 'show vlan all', 'state': 4, 'action': 'PRINT', 'args': output_va_0})

    d = Device(host=dut.host, port=dut.port, protocol=dut.protocol, log_level=log_level, mock=use_mock)
    d.open()
    assert '1.0.17' in d.vlan[7]['tagged']
    assert '1.0.17' not in d.vlan[10]['tagged']
    d.vlan.add_interface(10, '1.0.17', tagged=True)
    assert '1.0.17' not in d.vlan[7]['tagged']
    assert '1.0.17' in d.vlan[10]['tagged']
    d.vlan.delete_interface(10, '1.0.17')
    assert '1.0.17' in d.vlan[7]['tagged']
    assert '1.0.17' not in d.vlan[10]['tagged']
    d.close()


def test_add_and_delete_interface_5(dut, log_level, use_mock):
    output_rc_0 = ["""
!
interface port1.0.1-1.0.50
 switchport
 switchport mode access
!
vlan database
 vlan 10 name "marketing vlan"
 vlan 10 state enable
 vlan 7 name admin state enable
!
end
"""]
    output_va_0 = ["""
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
20      "this is a long vlan name"
                         STATIC  ACTIVE  port1.0.42(u) port1.0.43(t)
10      VLAN0010         STATIC  ACTIVE  port1.0.28(t)
"""]

    output_rc_1 = ["""
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
 vlan 10 state enable
 vlan 7 name admin state enable
!
end
"""]
    output_va_1 = ["""
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
7       admin            STATIC  ACTIVE  port1.0.28(t) port1.0.29(u)
20      "this is a long vlan name"
                         STATIC  ACTIVE  port1.0.42(t) port1.0.43(t)
10      VLAN0010         STATIC  ACTIVE  port1.0.28(t) port1.0.18(t)
"""]

    setup_dut(dut)

    dut.add_cmd({'cmd': 'show running-config', 'state': 0, 'action': 'PRINT', 'args': output_rc_0})
    dut.add_cmd({'cmd': 'show vlan all', 'state': 0, 'action': 'PRINT', 'args': output_va_0})
    dut.add_cmd({'cmd': 'interface port1.0.18', 'state': 0, 'action': 'SET_PROMPT', 'args': ['(config-if)#']})
    dut.add_cmd({'cmd': 'interface port1.0.18', 'state': 0, 'action': 'SET_STATE', 'args': [1]})
    dut.add_cmd({'cmd': 'switchport trunk allowed vlan add 10', 'state': 1, 'action': 'SET_STATE', 'args': [2]})
    dut.add_cmd({'cmd': 'show running-config', 'state': 2, 'action': 'PRINT', 'args': output_rc_1})
    dut.add_cmd({'cmd': 'show vlan all', 'state': 2, 'action': 'PRINT', 'args': output_va_1})
    dut.add_cmd({'cmd': 'interface port1.0.18', 'state': 2, 'action': 'SET_PROMPT', 'args': ['(config-if)#']})
    dut.add_cmd({'cmd': 'interface port1.0.18', 'state': 2, 'action': 'SET_STATE', 'args': [3]})
    dut.add_cmd({'cmd': 'switchport trunk allowed vlan remove 10', 'state': 3, 'action': 'SET_STATE', 'args': [4]})
    dut.add_cmd({'cmd': 'show running-config', 'state': 4, 'action': 'PRINT', 'args': output_rc_0})
    dut.add_cmd({'cmd': 'show vlan all', 'state': 4, 'action': 'PRINT', 'args': output_va_0})

    d = Device(host=dut.host, port=dut.port, protocol=dut.protocol, log_level=log_level, mock=use_mock)
    d.open()
    assert '1.0.18' in d.vlan[1]['untagged']
    assert '1.0.18' not in d.vlan[10]['tagged']
    d.vlan.add_interface(10, '1.0.18', tagged=True)
    assert '1.0.18' in d.vlan[1]['untagged']
    assert '1.0.18' in d.vlan[10]['tagged']
    d.vlan.delete_interface(10, '1.0.18')
    assert '1.0.18' in d.vlan[1]['untagged']
    assert '1.0.18' not in d.vlan[10]['tagged']
    d.close()
