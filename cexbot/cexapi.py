#!/usr/bin/env python
"""
  cexbot.cexapi
"""

import requests
import requests.exceptions
import hmac
import hashlib
import json
import logging
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
    if not username or not apikey or not secret:
      logging.error("Need username, apikey and secret")
    self.access_token['username'] = username
    self.access_token['apikey'] = apikey
    self.access_token['secret'] = secret

  def get_params(self):
    nonce = int(time())
    message = str(nonce) + self.access_token['username'] + self.access_token['apikey']
    sig = hmac.new(self.access_token['secret'], msg=message, digestmod=hashlib.sha256).hexdigest().upper()
    return {'key': self.access_token['apikey'], 'signature': sig, 'nonce': nonce}

  def get_headers(self):
    headers = self.headers
    # @TODO add headers
    return headers

  def req(self, meth, extras={}):
    if not meth in self.api_methods:
      logging.error("Error: No method %s" % (meth))
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
      logging.error("Error: connection")
      return false
    if r.headers['Content-Type'] != 'text/json' or not r.text:
      logging.error("Request error (%s)" % r.text[:200])
      return False
    try:
      c = json.loads(r.text)
      if 'error' in c:
        logging.error("API: %s" % c['error'])
        return False
    except ValueError:
      logging.error("Content loading error")
      return False
    return c

  def get_balance(self):
    try:
      br = self.req('balance')
      if br:
        return br['BTC']['available']
    except KeyError:
      return False

  def buy_market(self, amount):
    pass

  def place_order(self, amount, price, typ='buy'):
    extras = {
      'type': typ,
      'amount': amount,
      'price': price
    }
    r = self.req('place_order', extras)
    if 'id' in r:
      return r['id']
    logging.error("Order error")
    return False

  def buy_balance(self, balance_threshold=0.0001):
    balance = self.get_balance()
    if not balance:
      return False
    if balance < balance_threshold:
      return False
    price = self.get_market_quote()
    if not price:
      logging.error('price error')
      return False
    price = float(price)
    balance = float(balance)
    amount = balance / price
    order_total = amount * price
    if amount > 0.0001:
      logging.info("Buy %s at %s for total balance %s (of %s)" % (amount, price, order_total, balance))
      e = self.place_order(amount, price)
      logging.info("Order Id: %s" % e)

  def get_market(self):
    try:
      quotes = self.req('book')
      if quotes:
        for q in quotes[:5]:
          print q
    except Exception:
      return False

  def get_market_quote(self):
    # @todo check the quantity here
    try:
      ask = self.req('book')
      if ask:
        return ask['asks'][0][0]
    except Exception:
      return False

