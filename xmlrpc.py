#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xmlrpclib
import socket

a = xmlrpclib.ServerProxy('http://chcekcer:3607885@127.0.0.1:9001')
a.system.listMethods()
a.supervisor.getSupervisorVersion()
a.supervisor.getAllProcessInfo()
# a.supervisor.stopProcessGroup('proxy_check')
# a.supervisor.startProcessGroup('proxy_check')
a.supervisor.reloadConfig()
