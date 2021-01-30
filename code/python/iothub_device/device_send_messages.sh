#!/bin/bash

# Usage:
#   $ ./device_send_messages.sh <count> <sleep_milliseconds>
#   $ ./device_send_messages.sh 10 1000
#
# Chris Joakim, Microsoft, 2020/11/03

msg_count=$1
sleep_milliseconds=$2

python device.py $msg_count $sleep_milliseconds

echo 'done'
