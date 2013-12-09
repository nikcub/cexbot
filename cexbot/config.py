#!/usr/bin/env python
"""
	cexbot.config - config abstraction
"""

import os
import logging
import ConfigParser
import subprocess

from cexbot.appdirs import AppDirs
from cexbot.db import DbManager

ad = AppDirs("cexbot", "cexbot")

DB_NAME = 'tradedata.db'
CNF_NAME = 'cex.cnf'
CNF_SEARCHPATHS = ['.', '~', '/etc']
CONFIG_DEFAULTS = {
	'auth': {
		'username': 'username',
		'apikey': 'api',
		'secret': 'secret',
		}
	}

CONFIG_REQUIRED = {
	'auth': ('username', 'apikey', 'secret'),
}

class BadConfig(Exception):
	pass


def first_run():
	path_config = get_conf_path()
	path_db = get_db_path()
	if not os.path.isdir(ad.user_data_dir):
		os.mkdir(ad.user_data_dir)
	if not os.path.isfile(path_config):
		logging.debug("Writing config at %s" % path_config)
		write_blank(path_config)
	if not os.path.isfile(path_db):
		logging.debug("Writing empty db at: %s" % path_db)
		db = DbManager(path_db)
		db.init()


def clear_userdata():
	path_config = get_conf_path()
	path_db = get_db_path()
	conf_files = [path_config, path_db]
	for conf_file in conf_files:
		if os.path.isfile(conf_file):
			os.unlink(conf_file)


def get_db_path():
	return os.path.join(ad.user_data_dir, DB_NAME)


def get_conf_path():
	return os.path.join(ad.user_data_dir, CNF_NAME)


def get_config_parser():
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


def write_blank(file_path):
	"""Writes a blank config file at path provided by appdir"""
	parser = get_config_parser()
	parser = defaults_write(parser)
	with open(file_path, 'wb') as config_file:
		parser.write(config_file)
	logging.info("Blank config file written to %s" % file_path)


def edit_config():
	"""Edit config file in path from appdir"""
	path_config = get_conf_path()
	editor = os.environ.get('EDITOR','vim')
	subprocess.call([editor, path_config])
	return True

def get_config():
	parser = get_config_parser()
	parser.read(get_conf_path())
	try:
		defaults_check(parser)
	except BadConfig, e:
		logging.error(str(e))

	return parser
