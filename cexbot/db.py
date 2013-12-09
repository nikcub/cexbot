#!/usr/bin/env python
"""
  cexbot.db - database abstraction
"""

import logging
import sqlite3 as lite

import config

class DbManager(object):

  def __init__(self, path_db=None):
    if not path_db:
      path_db = config.get_db_path()
    self.conn = lite.connect(path_db)
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


  def getdb(self):
    con = lite.connect(DB_NAME)
    return con

  def init(self):
    self.cur.execute("CREATE TABLE IF NOT EXISTS quotes (time INTEGER primary key, last integer, volume integer, high integer, low integer, bid integer, ask integer)")
    logging.info('Database Initialized')
    return True