#!/usr/bin/env python

"""cexbot
"""

import sys
import os

VERSION = (0, 0, 4, 'dev', 1)

__clsname__ = 'cexbot'
__author__ = 'Nik Cubrilovic <nikcub@gmail.com>'
__email__ = 'nikcub@gmail.com'
__url__ = 'http://nikcub.github.com/cexbot'
__license__ = 'BSD'
__copyright__ = 'Copyright (c) 2013, Nik Cubrilovic. All rights reserved.'


def get_version(version=None):
  if version is None:
    version = VERSION
  assert version[3] in ('dev', 'alpha', 'beta', 'rc', 'final')
  parts = 2 if version[2] == 0 else 3
  main = '.'.join(str(x) for x in version[:parts])
  sub = ''
  if version[3] != 'final':
    mapping = {'dev': 'd', 'alpha': 'a', 'beta': 'b', 'rc': 'c'}
    sub = mapping[version[3]] + str(version[4])
  return main + sub

def get_status(version=None):
  if version is None:
    version = VERSION
  assert version[3] in ('alpha', 'beta', 'rc', 'final')
  return version[3]

def write_version(file_path=None):
  if not file_path:
    if not '__file__' in globals():
      cwd = os.path.abspath(os.getcwd())
    else:
      cwd = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.realpath(os.path.join(cwd, '..'))
  version_file = os.path.join(file_path, 'VERSION')
  print file_path
  with open(version_file, 'w') as f:
    f.write(get_version())

if __name__ == '__main__':
  from cexbot.command_utils import run_cl
  sys.exit(run_cl())

