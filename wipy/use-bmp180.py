import pycom
import time
pycom.heartbeat(False)

from bmp180 import BMP180
from  machine import I2C,  Pin

INTERVAL = 4      #interval between readings in seconds

try:
    i2c =  I2C(0)
    i2c.init(I2C.MASTER, baudrate=100000, pins=(Pin('P9'),Pin('P10')))
    print("I2C setup scan",  i2c.scan())

    bmp180 = BMP180(i2c)
    bmp180.oversample_sett = 2
    bmp180.baseline = 101325

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
    pycom.rgbled(0x7f0000) # red
    time.sleep(1)
    print("Error: ", str(e))
   
pycom.heartbeat(False) 
pycom.heartbeat(True)
