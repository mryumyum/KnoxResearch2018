#!C:\Users\tmoses\AppData\Local\Continuum\Anaconda3\python.exe
"""
T. Moses - 6-11-18
filename: tmPySerialTest1.py
Run from same directory as program, e.g. c:\tomcode.
"""

import serial
import time

ser = serial.Serial(port='COM7', baudrate=19200, timeout=5)
time.sleep(2)  # Must wait for arduino to open port; 1 sec insufficient
cmdToSend = '<SV,2000>'
print('Writing: ', cmdToSend)   # no end-of-line character needed in cmdToSend
ser.write(str(cmdToSend).encode())
time.sleep(1)
ser.flush() # it is buffering. required to get the data out *now*
#readOut = ser.readline().decode('ascii')  #works, but reads only one line
bytesToRead = ser.inWaiting()
readOut = ser.read(bytesToRead).decode('utf-8')
time.sleep(1)
print('readOut = ', readOut)