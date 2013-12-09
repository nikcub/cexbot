#!/usr/bin/env python

""" cexbot - command_utils.py

Default command line utitlities to run cexbot

@TODO improve the long helps
"""

import os
import sys
import logging
import argparse

import cexbot.config
import cexbot.tasks

from cexbot.db import DbManager
from cexbot.cexapi import CexAPI
from cexbot.updater import check_update
from cexbot.timer import ReqTimer
from cexbot.cex import CexMethods


def main(argv=[]):
  args = get_parser()

  if args.task == 'genconfig':
    return cexbot.config.write_blank()

  if args.task == 'editconfig':
    return cexbot.config.edit_config()

  if args.task == 'update':
    return check_update()

  if args.task == 'cleardata':
    return cexbot.config.clear_userdata()

  verbose = 1
  if args.verbose:
    verbose = 2
  if args.debug:
    verbose = 3

  if verbose>2:
    log_level=logging.DEBUG
  elif verbose==2:
    log_level=logging.INFO
  elif verbose==1:
    log_level=logging.WARNING
  elif verbose<1:
    log_level=logging.ERROR

  logging.basicConfig(level=log_level, format="%(asctime)s %(levelname)s: %(message)s")

  cexbot.config.first_run()
  config = cexbot.config.get_config()
  ac = CexAPI(config.get('auth', 'username'), config.get('auth', 'apikey'), config.get('auth', 'secret'))
  dbi = DbManager()
  cx = CexMethods(ac, dbi)

  if args.task == 'getbalance':
    logging.info("Balance: %s" % ac.get_balance())
    return True

  if args.task == 'initdb':
    return dbi.initdb()

  if args.task == 'getmarket':
    return ac.get_market()

  if args.task == 'getprice':
    return ac.get_market_quote()

  if args.task == 'order':
    amount = args.amount
    price = args.price
    r = ac.place_order(amount, price)
    logging.info("Ordered: %s" % r)

  if args.task == 'updatequotes':
    logging.info('Running updatequotes')
    ticker_timer = ReqTimer(2, cx.update_ticker)
    ticker_timer.start()

  if args.task == 'buybalance':
    logging.info('Running buybalance')
    balance_timer = ReqTimer(5, ac.buy_balance)
    balance_timer.start()

  # @TODO __import__
  # if args.task in cexbot.tasks:
    # cexbot.tasks[args.task]()

def get_parser():
  parser = argparse.ArgumentParser(prog='cexbot-cli', description='cexbot')
  parser.add_argument('task')
  # parser.add_argument('-o', dest='logfile', type=str, help='output log file')
  parser.add_argument('-v', dest='verbose', action='store_true', help='verbose output')
  parser.add_argument('--version', dest='version', action='store_true', help='show version')
  parser.add_argument('-d', dest='debug', action='store_true', help='debug output')
  parser.add_argument('-p', dest='price', action='store_true', help='price')
  parser.add_argument('-a', dest='amount', action='store_true', help='amount')
  # parser.add_argument('-p', dest='proxy', type=str, default='tor', help='proxy to use')
  # parser.add_argument('-t', dest='threads', type=int, default=1, help='number of threads')
  return parser.parse_args()

def cl_error(msg=""):
  print >> sys.stderr, msg

def run_cl(argv=[]):
  try:
    raise SystemExit(main(sys.argv))
  except KeyboardInterrupt:
    cl_error('Interrupted.')
    raise SystemExit(-1)

def run_gui(argv=[]):
  print "GUI coming soon."
  return None
  try:
    import cexbot.gui
    cexbot.gui.main()
  except Exception, e:
    print "Error: %s" % str(e)

