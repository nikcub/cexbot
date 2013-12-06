#!/usr/bin/env python
"""
	cexbot.cexapi
"""

import requests
import requests.exceptions
import hmac
import hashlib
import json
from time import time

class CexAPI(object):

	CEX_API_BASE = 'https://cex.io/api'

	# format is (URI, private, required params)
	api_methods = {
		'ticker': ('/ticker/GHS/BTC', False, None),
		'book': ('/order_book/GHS/BTC', False, None),
		'history': ('/trade_history/GHS/BTC', False, None),
		'balance': ('/balance/', True),
		'orders': ('/open_orders/GHS/BTC', True),
		'cancel_order': ('/cancel_order/', True, ('id')),
		'place_order': ('/place_order/GHS/BTC', True, ('type', 'amount', 'price')),
	}

	access_token = {'username': None, 'apikey': None, 'secret': None}

	headers = {
		'User-Agent' : 'bot-cex.io-',
		}

	def __init__(self, username, apikey, secret):
		self.access_token['username'] = username
		self.access_token['apikey'] = apikey
		self.access_token['secret'] = secret

	def get_params():
		nonce = int(time())
		message = str(nonce) + self.access_token['username'] + self.access_token['apikey']
		sig = hmac.new(self.access_token['secret'], msg=message, digestmod=hashlib.sha256).hexdigest().upper()
		return {'key': self.access_token['apikey'], 'signature': sig, 'nonce': nonce}

	def get_headers():
		headers = self.headers
		# @TODO add headers
		return headers

	def req(self, meth, extras={}):
		if not meth in self.api_methods:
			print "Error: No method %s" % (meth)
			return False
		req_method = self.api_methods[meth]
		req_uri = self.CEX_API_BASE + req_method[0]
		try:
			if req_method[1]:
				params = self.get_params()
				params.update(extras)
				r = requests.post(req_uri, headers=self.headers, data=params)
			else:
				r = requests.post(req_uri, headers=self.headers)
		except requests.exceptions.ConnectionError, e:
			print "Error: connection"
			return false
		if r.headers['Content-Type'] != 'text/json' or not r.text:
			print "Request error (%s)" % r.text[:200]
			return False
		try:
			c = json.loads(r.text)
		except ValueError:
			return False
		return c