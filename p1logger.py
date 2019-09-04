# -*- coding: utf-8 -*-
"""
Python script to log p1 data in a .csv file

v0.1
Daan Wielens
2019-09-04

Based on: http://domoticx.com/p1-poort-slimme-meter-telegram-uitlezen-met-python/
"""

import re
import serial
import datetime
import os

if not os.path.isdir('p1data'):
    os.mkdir('p1data')

#%% Configure serial port
ser = serial.Serial()

# DSMR 2.2 > 9600 7E1:
#ser.baudrate = 9600
#ser.bytesize = serial.SEVENBITS
#ser.parity = serial.PARITY_EVEN
#ser.stopbits = serial.STOPBITS_ONE

# DSMR 4.0/4.2 > 115200 8N1:
ser.baudrate = 115200
ser.bytesize = serial.EIGHTBITS
ser.parity = serial.PARITY_NONE
ser.stopbits = serial.STOPBITS_ONE

ser.xonxoff = 0
ser.rtscts = 0
ser.timeout = 12
ser.port = "/dev/ttyUSB0"
ser.close()

#%% Main code

while True:
  ser.open()
  checksum_found = False

  while not checksum_found:
    telegram_line = ser.readline()
    telegram_line = telegram_line.decode('ascii').strip()

    # Check if data matches preset variables (https://github.com/DaanWielens/p1data-parser/blob/master/parser.json)
    if '1-0:1.7.0' in telegram_line: #1-0:1.7.0 = Actual use in kW
      # 1-0:1.7.0(0000.54*kW)
      kw = telegram_line.split('(')[1].split('*')[0]
      watt = float(kw) * 1000

    if '0-1:24.2.1' in telegram_line: #0-1:24.2.1 = Gas in m3
      gmcubed = telegram_line.split('(')[2].split('*')[0]

    # Check whether end of telegram was received
    if '!' in telegram_line:
      checksum_found = True

  ser.close()

  # Write data to file
  ts = int(datetime.datetime.now().timestamp())
  data_str = ', '.join([str(ts), str(watt), str(gmcubed)]) + '\n'

  cur_day = datetime.datetime.now().strftime('%Y-%m-%d')
  filename = 'p1data/' + cur_day + '_p1data.csv'

  if os.path.isfile(filename):
      # Write data
      with open(filename, 'a') as file:
          file.write(data_str)

  else:
      # Write header
      with open(filename, 'w') as file:
          file.write('Time (epoch), Power (W), Gas (m3)\n')
          file.write(data_str)
