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


def test_add_user(dut, log_level):
    config_0 = ["""
!
service password-encryption
!
no banner motd
!
username manager privilege 15 password 8 $1$bJoVec4D$JwOJGPr7YqoExA0GVasdE0
!
ssh server allow-users manager
service ssh
!
interface port1.0.1-1.0.50
 switchport
 switchport mode access
!
interface vlan1
 ip address 10.17.39.253/24
!
end
"""]
    config_1 = ["""
!
service password-encryption
!
no banner motd
!
username manager privilege 15 password 8 $1$bJoVec4D$JwOJGPr7YqoExA0GVasdE0
username testuser privilege 5 password 8 $1$uWpWUKfS$l0FbezBRUBllEpc8.9kIF/
!
ssh server allow-users manager
service ssh
!
interface port1.0.1-1.0.50
 switchport
 switchport mode access
!
interface vlan1
 ip address 10.17.39.253/24
!
end
"""]
    setup_dut(dut)
    dut.add_cmd({'cmd': 'show running-config'                         , 'state':0, 'action':'PRINT','args': config_0})
    dut.add_cmd({'cmd': 'username testuser password enemy privilege 5', 'state':0, 'action':'SET_STATE','args':[1]})
    dut.add_cmd({'cmd': 'show running-config'                         , 'state':1, 'action':'PRINT','args': config_1})
    d=Device(host=dut.host,port=dut.port,protocol=dut.protocol, log_level=log_level)
    d.open()
    assert d.user['manager']['privilege_level'] == '15'
    d.user.create("testuser", password="enemy", privilege_level=5)
    assert d.user['manager']['privilege_level'] == '15'
    # assert d.user['testuser']['privilege_level'] == '5'
    d.close()


def test_change_user_password(dut, log_level):
    config_0 = ["""
!
service password-encryption
!
no banner motd
!
username manager privilege 15 password 8 $1$bJoVec4D$JwOJGPr7YqoExA0GVasdE0
username testuser privilege 5 password 8 $1$uWpWUKfS$l0FbezBRUBllEpc8.9kIF/
!
ssh server allow-users manager
service ssh
!
interface port1.0.1-1.0.50
 switchport
 switchport mode access
!
interface vlan1
 ip address 10.17.39.253/24
!
end
"""]
    config_1 = ["""
!
service password-encryption
!
no banner motd
!
username manager privilege 15 password 8 $1$bJoVec4D$JwOJGPr7YqoExA0GVasdE0
username testuser privilege 5 password 8 $1$CEgGZi0q$3JfHL/fM2F5YS47c/54ZQ.
!
ssh server allow-users manager
service ssh
!
interface port1.0.1-1.0.50
 switchport
 switchport mode access
!
interface vlan1
 ip address 10.17.39.253/24
!
end
"""]
    config_2 = ["""
!
service password-encryption
!
no banner motd
!
username manager privilege 15 password 8 $1$bJoVec4D$JwOJGPr7YqoExA0GVasdE0
username testuser privilege 5 password 8 $1$uWpWUKfS$l0FbezBRUBllEpc8.9kIF/
!
ssh server allow-users manager
service ssh
!
interface port1.0.1-1.0.50
 switchport
 switchport mode access
!
interface vlan1
 ip address 10.17.39.253/24
!
end
"""]
    setup_dut(dut)
    dut.add_cmd({'cmd': 'show running-config'              , 'state':0, 'action':'PRINT','args': config_0})
    dut.add_cmd({'cmd': 'username testuser password newpwd', 'state':0, 'action':'SET_STATE','args':[1]})
    dut.add_cmd({'cmd': 'show running-config'              , 'state':1, 'action':'PRINT','args': config_1})
    dut.add_cmd({'cmd': 'username testuser password enemy' , 'state':1, 'action':'SET_STATE','args':[2]})
    dut.add_cmd({'cmd': 'show running-config'              , 'state':2, 'action':'PRINT','args': config_2})
    d=Device(host=dut.host,port=dut.port,protocol=dut.protocol, log_level=log_level)
    d.open()
    print("change user password")
# add here library function invokations and asserts
    d.user.update("testuser", password="newpwd")
    d.user.update("testuser", password="enemy")
    d.close()


def test_change_user_privilege(dut, log_level):
    config_0 = ["""
!
service password-encryption
!
no banner motd
!
username manager privilege 15 password 8 $1$bJoVec4D$JwOJGPr7YqoExA0GVasdE0
username testuser privilege 5 password 8 $1$uWpWUKfS$l0FbezBRUBllEpc8.9kIF/
!
ssh server allow-users manager
service ssh
!
interface port1.0.1-1.0.50
 switchport
 switchport mode access
!
interface vlan1
 ip address 10.17.39.253/24
!
end
"""]
    config_1 = ["""
!
service password-encryption
!
no banner motd
!
username manager privilege 15 password 8 $1$bJoVec4D$JwOJGPr7YqoExA0GVasdE0
username testuser privilege 4 password 8 $1$uWpWUKfS$l0FbezBRUBllEpc8.9kIF/
!
ssh server allow-users manager
service ssh
!
interface port1.0.1-1.0.50
 switchport
 switchport mode access
!
interface vlan1
 ip address 10.17.39.253/24
!
end
"""]
    config_2 = ["""
!
service password-encryption
!
no banner motd
!
username manager privilege 15 password 8 $1$bJoVec4D$JwOJGPr7YqoExA0GVasdE0
username testuser privilege 5 password 8 $1$uWpWUKfS$l0FbezBRUBllEpc8.9kIF/
!
ssh server allow-users manager
service ssh
!
interface port1.0.1-1.0.50
 switchport
 switchport mode access
!
interface vlan1
 ip address 10.17.39.253/24
!
end
"""]
    setup_dut(dut)
    dut.add_cmd({'cmd': 'show running-config'          , 'state':0, 'action':'PRINT','args': config_0})
    dut.add_cmd({'cmd': 'username testuser privilege 4', 'state':0, 'action':'SET_STATE','args':[1]})
    dut.add_cmd({'cmd': 'show running-config'          , 'state':1, 'action':'PRINT','args': config_1})
    dut.add_cmd({'cmd': 'username testuser privilege 5', 'state':1, 'action':'SET_STATE','args':[2]})
    dut.add_cmd({'cmd': 'show running-config'          , 'state':2, 'action':'PRINT','args': config_2})
    d=Device(host=dut.host,port=dut.port,protocol=dut.protocol, log_level=log_level)
    d.open()
    assert d.user['testuser']['privilege_level'] == '5'
    d.user.update("testuser", privilege_level=4)
    assert d.user['testuser']['privilege_level'] == '4'
    d.user.update("testuser", privilege_level=5)
    assert d.user['testuser']['privilege_level'] == '5'
    d.close()


def test_remove_user(dut, log_level):
    config_0 = ["""
!
service password-encryption
!
no banner motd
!
username manager privilege 15 password 8 $1$bJoVec4D$JwOJGPr7YqoExA0GVasdE0
username testuser privilege 5 password 8 $1$uWpWUKfS$l0FbezBRUBllEpc8.9kIF/
!
ssh server allow-users manager
service ssh
!
interface port1.0.1-1.0.50
 switchport
 switchport mode access
!
interface vlan1
 ip address 10.17.39.253/24
!
end
"""]
    config_1 = ["""
!
service password-encryption
!
no banner motd
!
username manager privilege 15 password 8 $1$bJoVec4D$JwOJGPr7YqoExA0GVasdE0
!
ssh server allow-users manager
service ssh
!
interface port1.0.1-1.0.50
 switchport
 switchport mode access
!
interface vlan1
 ip address 10.17.39.253/24
!
end
"""]
    setup_dut(dut)
    dut.add_cmd({'cmd': 'show running-config' , 'state':0, 'action':'PRINT','args': config_0})
    dut.add_cmd({'cmd': 'no username testuser', 'state':0, 'action':'SET_STATE','args':[1]})
    dut.add_cmd({'cmd': 'show running-config' , 'state':1, 'action':'PRINT','args': config_1})
    d=Device(host=dut.host,port=dut.port,protocol=dut.protocol, log_level=log_level)
    d.open()
    d.user.delete("testuser")
    with pytest.raises(KeyError):
        d.user['testuser']
    d.close()

###
### the above reported sequence has to be repeated with an encrypted password user
###
