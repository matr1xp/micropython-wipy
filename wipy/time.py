#
# WiPy board has no RTC so rely on internet's NTP to set 
#  correct time. Call in `boot.py`
#    execfile('time.py')
#
class TimeUtil:
 global format_time
 def format_time(t_tuple):
    return '{0}-{1:02d}-{2:02d} {3:02d}:{4:02d}:{5:02d}'.format(*t_tuple)
    
from machine import RTC
import time

f=open('time.log', 'w')
rtc = RTC()
rtc.ntp_sync('0.au.pool.ntp.org')
time.sleep(2)
f.write("Synching ntp time: "+format_time(rtc.now())+" (UTC)\n")
time.timezone(39600)
rtc.init(time.localtime(time.time() + 39600))
f.write("Time adjusted to: "+format_time(rtc.now())+" (AEDT)\n")
f.close()
