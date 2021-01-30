"""
Usage:
  python main.py simulate_device_http_telemetry 5 3.0
Options:
  -h --help     Show this screen.
  --version     Show version.
"""

import asyncio
import datetime
import json
import os
import random
import sys
import time
import uuid

from azure.iot.device.aio import IoTHubDeviceClient
from azure.iot.device import Message

# IoT Hub Client program.
# Generates and sends simulated telemetry JSON messages to the IotHub.
#
# Usage:
#   dotnet run <message-count> <sleep-milliseconds>
#
# Chris Joakim, Microsoft, 2020/10/26

async def main(count, sleep_milliseconds):
  conn_str = os.getenv("AZURE_IOTHUB_DEVICE1_CONN_STR")
  device_client = IoTHubDeviceClient.create_from_connection_string(conn_str)

  await device_client.connect()

  for i in range(count):
    await send_message(device_client, i)
    time.sleep(float(sleep_milliseconds) / 1000.0)

  await device_client.disconnect()

def simulated_telemetry_data(i):
  msg_data = dict()
  msg_data['seq'] = i + 1
  msg_data['epoch'] = time.time()
  msg_data['device_type'] = 'python'
  msg_data['device_os'] = os.uname()[0].lower()
  msg_data['device_version'] = str(sys.version_info)
  msg_data['device_pid']  = os.getpid()
  msg_data['line_speed']  = random.randint(0, 20000)
  msg_data['temperature'] = random.randint(40, 200)
  msg_data['humidity']    = random.randint(50, 100)
  return msg_data

async def send_message(device_client, i):
  msg_body = json.dumps(simulated_telemetry_data(i))
  print('sending message: {}'.format(msg_body))
  msg_id = uuid.uuid4()
  msg = Message(msg_body)
  msg.message_id = msg_id
  msg.correlation_id = msg_id
  await device_client.send_message(msg)


if __name__ == "__main__":
  msg_count, sleep_milliseconds = int(sys.argv[1]), float(sys.argv[2])
  print('device.py main start - msg_count: {}, sleep_milliseconds: {}'.format(msg_count, sleep_milliseconds))
  asyncio.run(main(msg_count, sleep_milliseconds))
  print('device.py main finish')
 