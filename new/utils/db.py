#!/usr/bin/env python
# -*- coding: utf-8 -*-

import MySQLdb

def __get_con():
	return MySQLdb.connect('localhost', 'root', 'root', 'checker')

def get_keyword_domain_by(id):
	db = __get_con()
	with db:
		c = db.cursor(MySQLdb.cursors.DictCursor)
        c.execute("SELECT keyword, domain FROM keywords_domains LEFT JOIN keywords ON keywords_domains.keyword_id = keywords.id LEFT JOIN domains ON keywords_domains.domain_id = domains.id WHERE keywords_domains.id = %s", str(id))
        rows = c.fetchall()
        if rows:
        	return rows[0]
        else:
        	return None

def save_search_result(id, pos):
	db = __get_con()
	with db:
		c = db.cursor()
		c.execute("INSERT INTO search_results VALUES(DATE(NOW()), %s, %s) ON DUPLICATE KEY UPDATE position=%s", (id, pos or 0, pos or 0))

def get_all_keyword_domain_ids():
	db = __get_con()
	with db:
		c = db.cursor(MySQLdb.cursors.DictCursor)
		c.execute("SELECT id FROM keywords_domains")
		rows = c.fetchall()
		rows = [int(row.get('id')) for row in rows]
		return rows