#
# Get BMP180 sensor reading for WiPy 2 micropython board.
#   Requires `bmp180.py` library from https://github.com/micropython-IMU/micropython-bmp180
#     copy above file in /lib directory of Wipy
'''
The MIT License (MIT)
Copyright 2017 Marlon Santos, learn@marlsantos.com

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), 
to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, 
and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS 
IN THE SOFTWARE.
'''
import pycom
import time
from bmp180 import BMP180
from  machine import I2C,  Pin

INTERVAL = 4      #interval between readings in seconds

try:
    # Setup I2C bus
    i2c =  I2C(0)
    i2c.init(I2C.MASTER, baudrate=100000, pins=(Pin('P9'),Pin('P10')))  # Change pins accordingly
    print("I2C setup scan",  i2c.scan())

    # Initialize BMP180 object
    bmp180 = BMP180(i2c)
    bmp180.oversample_sett = 2
    bmp180.baseline = 101325

    # Loop indefinitely (Ctrl+C to quit)
    while True:
       print("Reading sensor data...") 
       pycom.heartbeat(False)
       temp = bmp180.temperature
       p = bmp180.pressure
       altitude = bmp180.altitude
       print("Temp: {}C\nPressure: {}\nAltitude: {}m\n".format(temp, p, altitude))
       pycom.rgbled(0x007f00) # green
       time.sleep(1)
       pycom.heartbeat(False)
       time.sleep(INTERVAL)
       
except Exception as e: 
    pycom.rgbled(0x7f0000) # Red
    time.sleep(1)
    print("Error: ", str(e))
   
# Restore heartbeat LED   
pycom.heartbeat(False) 
pycom.heartbeat(True)
