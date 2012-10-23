#!/usr/bin/env python
# -*- coding: utf-8 -*-

import _mysql
import sys

con = None

try:
    con = _mysql.connect(host='localhost', user='checker', password='3607885', db='checker', init_command='SET NAMES UTF8')
    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM proxy")
        rows = cur.fetchall()
        for row in rows:
            print row
except _mysql.Error, e:
    print "Error %d: %s" % (e.args[0], e.args[1])
    sys.exit(1)
finally:
    if con:
        con.close()
