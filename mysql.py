#!/usr/bin/env python
# -*- coding: utf-8 -*-

import MySQLdb
import sys

def get_connection(cfg):
    con = mdb.connect(
            cfg.get('mysql', 'host'),
            cfg.get('mysql', 'user'),
            cfg.get('mysql', 'pass'),
            cfg.get('mysql', 'db')
            )
    return con

def all(cfg, sql, params=()):
    con = get_connection(cfg)
    cur = con.cursor(mdb.cursors.DictCursor)
    cur.execute(sql, params)
    con.close()
    rows = cur.fetchall()
    return rows

def one(cfg, sql, params=()):
    con = get_connection(cfg)
    cur = con.cursor(mdb.cursors.DictCursor)
    cur.execute(sql, params)
    con.close()
    row = cur.fetchone()
    return row



'''
con = None

try:
    con = mdb.connect('localhost', 'checker', '3607885', 'checker')
    with con:
        cur = con.cursor(mdb.cursors.DictCursor)
        cur.execute("SELECT * FROM proxy")
        rows = cur.fetchall()
        for row in rows:
            print "%s:%s@%s:%s" % (row['username'], row['password'], row['host'], row['port'])
except mdb.Error, e:
    print "Error %d: %s" % (e.args[0], e.args[1])
    sys.exit(1)
'''
