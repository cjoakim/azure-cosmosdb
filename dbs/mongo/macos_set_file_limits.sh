#!/bin/bash

# Bash script to increase the number of max number of open files from 256
# to 65536 before starting the mongod program.
#
# Symptoms; you'll see something like the following in the mongo.log
#   "errmsg" : "Index build failed: 6ae8f393-ad75-4a42-8329-a20bfc56c720: Collection olympics.g1998_winter ( b8ba5549-4173-4cfa-9068-2a0143c130da ) :: caused by :: index build on empty collection failed: 6ae8f393-ad75-4a42-8329-a20bfc56c720 :: caused by :: 24: Too many open files",
#   "code" : 264,
#   "codeName" : "TooManyFilesOpen"
#
# Chris Joakim, Microsoft, May 2021

echo '---'

echo 'current ulimit -n'
ulimit -n

echo 'current launchctl limit maxfiles'
launchctl limit maxfiles

echo '---'

echo 'ulimit increasing limits ...'
ulimit -n 65536 200000

echo 'launchctl increasing limits ...'
sudo launchctl limit maxfiles 65536 200000

echo '---'

echo 'updated ulimit -n'
ulimit -n

echo 'updated launchctl limit maxfiles'
launchctl limit maxfiles

echo ''
echo 'now start thd mongod program with:'
echo 'mongod --config /usr/local/etc/mongod.conf &'
echo ''
