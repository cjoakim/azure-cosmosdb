#!/bin/bash

# Bash script to repair a stopped mongod installation after it crashes.
# Chris Joakim, Microsoft, May 2021

echo 'repairing ...'
mongod --config /usr/local/etc/mongod.conf --repair

echo 'displaying log ...'
cat /usr/local/var/log/mongodb/mongo.log

# Reinstall:
# $ alias | grep mongod
# $ alias mongod_start='mongod --config /usr/local/etc/mongod.conf &'
#   path:   /usr/local/var/log/mongodb/mongo.log
#   dbPath: /usr/local/var/mongodb
# $ brew uninstall mongodb-community@4.0
# $ brew cleanup
# $ rm -rf /usr/local/var/log/mongodb/ 
# $ rm -rf /usr/local/var/mongodb 
#
# $ brew tap mongodb/brew
# $ brew install mongodb-community@4.4
# To have launchd start mongodb/brew/mongodb-community now and restart at login:
#   brew services start mongodb/brew/mongodb-community
# Or, if you don't want/need a background service you can just run:
#   mongod --config /usr/local/etc/mongod.conf
# ==> Summary
# 🍺  /usr/local/Cellar/mongodb-community/4.4.5: 11 files, 157.3MB, built in 6 seconds
#
# ... exit shell, start a new one
#
# $ $ mongo --version
# MongoDB shell version v4.4.5
