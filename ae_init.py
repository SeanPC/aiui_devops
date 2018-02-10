#!/usr/bin/env python
# -*- coding:utf-8 -*-

import ConfigParser

#initialize config loading
CONFIG_PATH = '/root/code/python/ae.conf'
CONFIG = ConfigParser.ConfigParser(allow_no_value=True)
CONFIG.read(CONFIG_PATH)

