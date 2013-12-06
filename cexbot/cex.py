#!/usr/bin/env python
"""
	cexbot.cexapi
"""


class CexMethods(object):

	def __init__(self, ap, db):
		self.ap = ap
		self.db = db
		pass

	def update_ticker():
		r = self.ap.req('ticker')
		con = self.db.getdb()
		cur = con.cursor()
		sql = "INSERT INTO quotes VALUES(%s, %s, %s, %s, %s, %s, %s)" % (r['timestamp'], r['last'], r['volume'], r['high'], r['low'], r['bid'], r['ask'])
		try:
			cur.execute(sql)
		except Exception, e:
			pass
		con.commit()



