#!/usr/bin/env python

"""cexbot
"""
# Contributions from Django

# Copyright (c) Django Software Foundation and individual contributors.
# All rights reserved.

import sys
import os

VERSION = (0, 0, 13, 'alpha', 1)

__clsname__ = 'cexbot'
__author__ = 'Nik Cubrilovic <nikcub@gmail.com>'
__email__ = 'nikcub@gmail.com'
__url__ = 'http://nikcub.github.com/cexbot'
__license__ = 'BSD'
__copyright__ = 'Copyright (c) 2013, Nik Cubrilovic. All rights reserved.'


def get_version(version=None, semantic=False):
  if version is None:
    version = VERSION
  assert version[3] in ('alpha', 'beta', 'rc', 'final')
  parts = 2 if version[2] == 0 else 3
  main = '.'.join(str(x) for x in version[:parts])
  sub = ''
  if version[3] == 'alpha' and version[4] == 0:
    git_changeset = get_git_changeset()
    if git_changeset:
      sub = '.dev%s' % git_changeset
  elif version[3] != 'final':
    mapping = {'alpha': 'a', 'beta': 'b', 'rc': 'c'}
    sub = mapping[version[3]] + str(version[4])
  if not semantic:
    return main + sub
  else:
    return main + '-' + sub

def get_status(version=None):
  if version is None:
    version = VERSION
  assert version[3] in ('alpha', 'beta', 'rc', 'final')
  return version[3]

def write_version(file_path=None, semantic=False):
  if not file_path:
    if not '__file__' in globals():
      cwd = os.path.abspath(os.getcwd())
    else:
      cwd = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.realpath(os.path.join(cwd, '..'))
  version_file = os.path.join(file_path, 'VERSION')
  print file_path
  with open(version_file, 'w') as f:
    f.write(get_version(semantic=semantic))

def get_git_changeset():  # pragma: nocover
  """Returns a numeric identifier of the latest git changeset.

  The result is the UTC timestamp of the changeset in YYYYMMDDHHMMSS format.
  This value isn't guaranteed to be unique, but collisions are very
  unlikely, so it's sufficient for generating the development version
  numbers.
  """
  repo_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
  git_log = subprocess.Popen('git log --pretty=format:%ct --quiet -1 HEAD',
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                           shell=True, cwd=repo_dir,
                           universal_newlines=True)
  timestamp = git_log.communicate()[0]
  try:
    timestamp = datetime.datetime.utcfromtimestamp(int(timestamp))
  except ValueError:  # pragma: nocover
    return None   # pragma: nocover
  return timestamp.strftime('%Y%m%d%H%M%S')


if __name__ == '__main__':
  from cexbot.command_utils import run_cl
  sys.exit(run_cl())

