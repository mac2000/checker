#!/usr/bin/env python
# -*- coding: utf-8 -*-
import ConfigParser
import os

cfg = ConfigParser.ConfigParser()
cfg.read('/etc/supervisor/supervisord.conf')

username = cfg.get('inet_http_server', 'username')
password = cfg.get('inet_http_server', 'password')
