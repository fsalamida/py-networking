# -*- coding: utf-8 -*-
from pynetworking import Feature
from pprint import pformat
import re
import json
try:
    from collections import OrderedDict
except ImportError: #pragma: no cover
    from ordereddict import OrderedDict

class ats_user(Feature):
    """
    User account feature implementation for ATS
    """
    def __init__(self, device, **kvargs):
        Feature.__init__(self, device, **kvargs)
        self._user_config={}
        self._user={}
        self._d = device
        self._d.log_debug("loading feature")

    def load_config(self, config):
        self._d.log_info("loading config")
        self._user_config = OrderedDict()

        # username manager password 8 $1$bJoVec4D$JwOJGPr7YqoExA0GVasdE0 privilege 15 encrypted
        ifre = re.compile('username\s+'
                          '(?P<user_name>[^\s]+)\s+'
                          'level\s+'
                          '(?P<privilege_level>\d+)\s+'
                          'password\s+'
                          '(?P<password>[^\s]+)\s+'
                          'encrypted\s+')
        for line in self._device.cmd("show running-config").split('\n'):
            m = ifre.match(line)
            if m:
                self._user_config[m.group('user_name')] = {'privilege_level': m.group('privilege_level'),
                                                           'encryption': True,
                                                           'password': m.group('password')
                                                          }
        self._d.log_info(self._user_config)


    def create(self, user_name, password, privilege_level, enc_pwd=False):
        self._d.log_info("add {0} {1} {2}".format(user_name, password, privilege_level))
        self._update_user()

        cmds = {'cmds':[{'cmd': 'enable', 'prompt':'\#'},
                        {'cmd': 'conf t', 'prompt':'\(config\)\#'}
                       ]}

        if enc_pwd == False:
            create_cmd = 'username {0} password {1} level {2}'.format(user_name, password, privilege_level)
        else:
            create_cmd = 'username {0} password {1} level {2} encrypted'.format(user_name, password, privilege_level)
        cmds['cmds'].append({'cmd': create_cmd, 'prompt':'\(config\)\#'})
        cmds['cmds'].append({'cmd': chr(26)   , 'prompt':'\#'})

        self._device.cmd(cmds, cache=False, flush_cache=True)
        self._device.load_system()


    def delete(self, user_name):
        self._d.log_info("remove {0}".format(user_name))
        self._update_user()

        cmds = {'cmds':[{'cmd': 'enable', 'prompt':'\#'},
                        {'cmd': 'conf t', 'prompt':'\(config\)\#'}
                       ]}
        delete_cmd = 'no username {0}'.format(user_name)
        cmds['cmds'].append({'cmd': delete_cmd, 'prompt':'\(config\)\#'})
        cmds['cmds'].append({'cmd': chr(26)   , 'prompt':'\#'})

        self._device.cmd(cmds, cache=False, flush_cache=True)
        self._device.load_system()


    def update(self, user_name, **kwargs):
        self._d.log_info("update {0} {1}".format(user_name,pformat(kwargs)))
        self._update_user()

        enc_pwd = False
        run_cmd = False
        cmds = {'cmds':[{'cmd': 'enable', 'prompt':'\#'},
                        {'cmd': 'conf t', 'prompt':'\(config\)\#'}
                       ]}

        if 'password' in kwargs:
            pwd = kwargs['password']
            if enc_pwd == False:
                pwd_cmd = 'username {0} password {1}'.format(user_name, pwd)
            else:
                pwd_cmd = 'username {0} password {1} encrypted'.format(user_name, pwd)
            cmds['cmds'].append({'cmd': pwd_cmd, 'prompt':'\(config\)\#'})
            run_cmd=True

        if 'privilege_level' in kwargs:
            level = kwargs['privilege_level']
            priv_cmd = 'username {0} level {1}'.format(user_name, level)
            cmds['cmds'].append({'cmd': priv_cmd, 'prompt':'\(config\)\#'})
            run_cmd=True

        if run_cmd:
            cmds['cmds'].append({'cmd': chr(26)   , 'prompt':'\#'})
            self._device.cmd(cmds, cache=False, flush_cache=True)
            self._device.load_system()


    def items(self):
        self._update_user()
        return self._user.items()


    def keys(self):
        self._update_user()
        return self._user.keys()


    def __getitem__(self, username):
        self._update_user()
        if username in self._user.keys():
            return self._user[username]
        raise KeyError('user {0} does not exist'.format(username))


    def _update_user(self):
        self._d.log_info("_update_user")
        self._user = OrderedDict()

        # username manager password $1$bJoVec4D$JwOJGPr7YqoExA0GVasdE0 privilege 15 encrypted
        ifre = re.compile('username\s+'
                          '(?P<user_name>[^\s]+)\s+'
                          'privilege\s+'
                          '(?P<privilege_level>\d+)\s+'
                          'password\s+'
                          '(?P<password>[^\s]+)\s+'
                          'encrypted\s+')
        for line in self._device.cmd("show running-config").split('\n'):
            m = ifre.match(line)
            if m:
                key = m.group('user_name')
                self._d.log_info("matching key is {0} ".format(key))
                self._user[key] = {'privilege_level': m.group('privilege_level'),
                                   'encryption': True,
                                   'password': m.group('password')
                                  }
                self._user[key] = dict(self._user[key].items() + self._user_config[key].items())

        self._d.log_debug("User {0}".format(pformat(json.dumps(self._user))))
