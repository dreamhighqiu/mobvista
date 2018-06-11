# -*- coding: utf-8 -*-
'''
@author: redstar
'''
import paramiko


class SSHClient():

    _client = None
    _stdin = None
    _stdout = None
    _stderr = None

    def __init__(self, host, port=22, user="root", passwd=""):
        self._client = paramiko.SSHClient()
        self._client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self._client.connect(host, port, user, passwd)

    def exe_cmd(self, cmd):
        print "[exe_cmd]%s" % cmd
        max_try = 3
        while(max_try > 0):
            try:
                self._stdin, self._stdout, self._stderr = self._client.exec_command(
                    cmd)
                err = self._stderr.readlines()
                if err:
                    raise Exception(err)
                return self._stdout.readlines()
            except Exception, e:
                print "[exe_cmd]Got Exception %s\nTry Again..." % str(e)
                max_try -= 1

    def __del__(self):
        self._client.close()
