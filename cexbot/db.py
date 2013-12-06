#!/usr/bin/env python
"""
	cexbot.db - database abstraction
"""

import sqlite3 as lite

class DbManager(object):
	DB_NAME = 'cex.db'

	def __init__(self, db):
	  self.conn = lite.connect(db)
	  self.conn.execute('pragma foreign_keys = on')
	  self.conn.commit()
	  self.cur = self.conn.cursor()

	def __del__(self):
	  self.conn.close()

	def query(self, arg):
	  self.cur.execute(arg)
	  self.conn.commit()
	  return self.cur

	def check_table(self, name):
		self.cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='%s'" % (name))


	def getdb():
		con = lite.connect(DB_NAME)
		return con

	def initdb():
		con = getdb()
		cur = con.cursor()
		con.execute("CREATE TABLE IF NOT EXISTS quotes (time INTEGER primary key, last integer, volume integer, high integer, low integer, bid integer, ask integer)")
		return True