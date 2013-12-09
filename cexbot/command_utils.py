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

  if args.command == 'version':
    print cexbot.get_version()
    return True

  # make sure this is always above command parsing
  cexbot.config.first_run()

  if verbose == 3:
    print args

  if args.command == 'config':
    if args.list:
      return cexbot.config.list()
    elif args.edit:
      return cexbot.config.edit_config()
    elif args.testauth:
      return cexbot.config.test_auth()
    elif args.name and args.value:
      v = cexbot.config.set(args.name, args.value)
      return cexbot.config.cprint(args.name)
    elif args.name:
      return cexbot.config.cprint(args.name)
    logging.error('Invalid config option')
    return 1

  elif args.command == 'update':
    return check_update()

  if args.task == 'cleardata':
    return cexbot.config.clear_userdata()


  config = cexbot.config.get_config()
  ac = CexAPI(config.get('cex', 'username'), config.get('cex', 'apikey'), config.get('cex', 'secret'))
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

  parser.add_argument('-v', dest='verbose', action='store_true', help='verbose output')
  parser.add_argument('-d', dest='debug', action='store_true', help='debug output (Warning: lots of output, for developers)')

  subparsers = parser.add_subparsers(description='available subcommands', dest="command")

  parser_config = subparsers.add_parser('config', help='config options')
  parser_config.add_argument('--list', dest='list', action='store_true', help='list configuration variables')
  parser_config.add_argument('--edit', dest='edit', action='store_true', help='edit configuration directly')
  parser_config.add_argument('--testauth', dest='testauth', action='store_true', help='test authentication credentials')
  parser_config.add_argument('name', type=str, help='option name', nargs='?')
  parser_config.add_argument('value', type=str, help='option value', nargs='?')

  parser_task = subparsers.add_parser('task', help='modify tasks')
  # parser_config.add_argument('--list', dest='task_list', action='store_true', help='list current tasks')
  parser_task.add_argument('name', type=str, help='task name', nargs='?')

  parser_order = subparsers.add_parser('order', help='order')
  parser_order.add_argument('-p', dest='price', action='store_true', help='price')
  parser_order.add_argument('-a', dest='amount', action='store_true', help='amount')

  parser_update = subparsers.add_parser('update', help='check for updates')

  parser_version = subparsers.add_parser('version', help='show version')

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

