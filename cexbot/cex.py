#!/usr/bin/env python
"""
	cexbot.cexapi
"""


class CexMethods(object):

	def __init__(self):
		pass

	def update_ticker():
		r = req('ticker')
		con = getdb()
		cur = con.cursor()
		sql = "INSERT INTO quotes VALUES(%s, %s, %s, %s, %s, %s, %s)" % (r['timestamp'], r['last'], r['volume'], r['high'], r['low'], r['bid'], r['ask'])
		try:
			cur.execute(sql)
		except Exception, e:
			pass
		con.commit()

	def get_balance():
		try:
			return req('balance')['BTC']['available']
		except KeyError:
			return False

	def buy_market(amount):
		pass

	def place_order(amount, price, typ='buy'):
		extras = {
			'type': typ,
			'amount': amount,
			'price': price
		}
		r = req('place_order', extras)
		if 'id' in r:
			return r['id']
		print "Order error"
		return False

	def buy_balance(balance_threshold=0.0001):
		balance = get_balance()
		if not balance:
			return False
		if balance < balance_threshold:
			return False
		price = get_market_quote()
		if not price:
			return False
		price = float(price)
		balance = float(balance)
		amount = balance / price
		order_total = amount * price
		if amount > 0.0001:
			print "Buy %s at %s for total balance %s (of %s)" % (amount, price, order_total, balance)
			e = place_order(amount, price)
			print "Order Id: %s" % e

	def get_market_quote():
		# @todo check the quantity here
		try:
			ask = req('book')['asks'][0][0]
			return ask
		except Exception:
			return False

