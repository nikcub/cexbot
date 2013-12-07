#!/bin/bash

export ARCHFLAGS="-arch i386 -arch x86_64"

if [[ -z "$1" ]]; then
  echo "Please supply a version number for this release as the first argument."
  exit
fi

echo "Creating OS X packages for Cexbot."

cd src && python2.7 build_osx.py py2app

if [[ $? = "0" ]]; then
  hdiutil create -fs HFS+ -volname "Cexbot" -srcfolder dist/Cexbot.app dist/cexbot-v$1.dmg
else
  echo "Problem creating Cexbot.app, stopping."
  exit
fi
