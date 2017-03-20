#
# Mounts SD card to `/sd` directory on boot up
#  Call in `boot.py` using:
#    execfile('sd-card.py')
#
from machine import SD
import os

# Create one-off log file
f = open('sd-card.log', 'w')

try:
    sd = SD()
    os.mount(sd, '/sd')
    f.write('Successfully mounted SD card to "/sd"')
except:
    f.write('Error mounting SD card!')

f.close()
