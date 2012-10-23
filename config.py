#!/usr/bin/env python
# -*- coding: utf-8 -*-
import ConfigParser
import os

def config():
	cfg = ConfigParser.ConfigParser()
	cfg.read('config.ini')
	return cfg
