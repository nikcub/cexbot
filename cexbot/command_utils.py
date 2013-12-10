#!/usr/bin/env python

""" cexbot - command_utils.py

Default command line utitlities to run cexbot
"""

import os, sys, logging
import cexbot, config, parser, db, cexapi, updater, timer, cex

def main(argv=[]):
  args = parser.get_parser()

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
  # print config
  config.first_run()

  if verbose == 3:
    print args

  if args.command == 'config':
    if args.list:
      return config.list()
    elif args.edit:
      return config.edit_config()
    elif args.testauth:
      return config.test_auth()
    elif args.name and args.value:
      v = config.set(args.name, args.value)
      return config.cprint(args.name)
    elif args.name:
      return config.cprint(args.name)
    logging.error('Invalid config option')
    return 1

  elif args.command == 'update':
    return updater.check_update()

  # not implemented
  elif args.command == 'cleardata':
    return config.clear_userdata()


  ac = cexapi.CexAPI(config.get('cex.username'), config.get('cex.apikey'), config.get('cex.secret'))
  dbi = db.DbManager()
  cx = CexMethods(ac, dbi)

  if args.command == 'balance':
    print "Balance: %s BTC" % ac.get_balance()
    return True

  elif args.command == 'initdb':
    return dbi.initdb()

  elif args.command == 'getmarket':
    return ac.get_market()

  elif args.command == 'getprice':
    return ac.get_market_quote()

  elif args.command == 'order':
    amount = args.amount
    price = args.price
    r = ac.place_order(amount, price)
    logging.info("Ordered: %s" % r)

  elif args.command == 'updatequotes':
    logging.info('Running updatequotes')
    ticker_timer = timer.ReqTimer(2, cx.update_ticker)
    ticker_timer.start()

  elif args.command == 'buybalance':
    logging.info('Running buybalance')
    balance_timer = timer.ReqTimer(5, ac.buy_balance)
    balance_timer.start()

  # @TODO __import__
  # if args.task in cexbot.tasks:
    # cexbot.tasks[args.task]()


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
  # return None
  try:
    import cexbot.gui
    cexbot.gui.main()
  except Exception, e:
    print "Error: %s" % str(e)

