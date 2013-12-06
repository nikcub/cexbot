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

  if args.task == 'genconfig':
    return config.write_blank()

  if args.task == 'update':
    return check_update()

  config = cexbot.config.get_config()
  ac = CexAPI(config.get('auth', 'username'), config.get('auth', 'apikey'), config.get('auth', 'secret'))
  dbi = DbManager()
  cx = CexMethods(ac, dbi)

  if args.task == 'getbalance':
    logging.info("Balance: %s" % ac.get_balance())
    return True

  if args.task == 'initdb':
    return dbi.initdb()

  if args.task == 'updatequotes':
    ticker_timer = ReqTimer(2, cx.update_ticker)
    ticker_timer.start()

  if args.task == 'buybalance':
    balance_timer = ReqTimer(60 * 5, ac.buy_balance)
    balance_timer.start()

  # @TODO __import__
  # if args.task in cexbot.tasks:
    # cexbot.tasks[args.task]()

def get_parser():
  parser = argparse.ArgumentParser(prog='cexbot-cli', description='cexbot')
  parser.add_argument('task')
  # parser.add_argument('-o', dest='logfile', type=str, help='output log file')
  parser.add_argument('-v', dest='verbose', action='store_true', help='verbose output')
  parser.add_argument('-d', dest='debug', action='store_true', help='debug output')
  # parser.add_argument('-p', dest='proxy', type=str, default='tor', help='proxy to use')
  # parser.add_argument('-t', dest='threads', type=int, default=25, help='number of threads')
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
  raise Exception('Not Implemented.')

