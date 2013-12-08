#!/usr/bin/env python
"""
	cexbot.config - config abstraction
"""

import os
import logging
import ConfigParser
import subprocess

CNF_NAME = 'cex.cnf'
CNF_SEARCHPATHS = ['.', '~', '/etc']
CONFIG_DEFAULTS = {
	'auth': {
		'username': '',
		'apikey': '',
		'secret': '',
		}
	}

CONFIG_REQUIRED = {
	'auth': ('username', 'apikey', 'secret'),
}

class BadConfig(Exception):
	pass

def cnf_object():
	return ConfigParser.SafeConfigParser(allow_no_value=True)

def defaults_write(parser):
	for default_section in CONFIG_DEFAULTS.keys():
		if not parser.has_section(default_section):
			parser.add_section(default_section)
		for key in CONFIG_DEFAULTS[default_section]:
			if not parser.has_option(default_section, key):
				parser.set(default_section, key, CONFIG_DEFAULTS[default_section][key])
	return parser

def defaults_check(parser):
	for section in CONFIG_REQUIRED.keys():
		if not parser.has_section(section):
			raise BadConfig("Require %s section in config" % section)
			parser.add_section(section)
		for i in CONFIG_REQUIRED[section]:
			if not parser.has_option(section, i):
				raise BadConfig("Require %s option in %s section of config" % (i, section))
			if len(parser.get(section, i)) < 1:
				raise BadConfig("Require non-empty %s option in %s section of config" % (i, section))
	return parser

def write_blank(file_path=None):
	parser = cnf_object()
	parser = defaults_check(parser)
	if not file_path:
		file_path = CNF_NAME
	with open(file_path, 'wb') as config_file:
		parser.write(config_file)
	logging.info("Blank config file written to %s" % config_file)

def get_cwd():
  if not '__file__' in globals():
    cwd = os.path.abspath(os.getcwd())
  else:
    cwd = os.path.dirname(os.path.abspath(__file__))
  return os.path.realpath(cwd)

def get_config_file():
	cwd = get_cwd()
	for p in CNF_SEARCHPATHS:
		tp = os.path.join('.')

def edit_config():
	config_file = CNF_NAME
	editor = os.environ.get('EDITOR','vim')
	subprocess.call([editor, config_file])
	return True

def get_config():
	parser = cnf_object()
	parser.read([CNF_NAME, os.path.expanduser('~/.' + CNF_NAME), os.path.realpath('/etc/' + CNF_NAME)])
	try:
		defaults_check(parser)
	except BadConfig, e:
		logging.error(str(e))

	return parser
