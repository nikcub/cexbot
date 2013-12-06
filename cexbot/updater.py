#!/usr/bin/env python
"""
	cexbot.updater - config abstraction
"""

import requests
import cexbot
import logging
# @TODO find a non-brainded semver implementation
# import semantic_version

UPDATE_URL = "https://raw.github.com/nikcub/cexbot/master/VERSION"

def get_latest():
	v =requests.get(UPDATE_URL)
	if v.status_code == 200:
		return v.text
	else:
		return False

def check_update():
	cur_version = cexbot.get_version()
	latest_version = get_latest()
	logging.info("Current version: %s Latest version: %s" % (cur_version, latest_version))
	# if latest_version:
		# lv = semantic_version.Version(latest_version)
		# cv = semantic_version.Version(cur_version)
		# if lv > cv:
			# logging.error("New version available, run git pull or pip -U cexbot")
	return None