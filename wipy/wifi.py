# 
# Setup WiFi connection on the WiPy micropython board 
#  Can be called in `boot.py` as: 
#    execfile('wifi.py')
#
import os
import machine

uart = machine.UART(0, 115200)
os.dupterm(uart)

# Create one-off log file
f = open('wifi.log', 'w')

known_nets = {
    'WIFI_AP1': {'pwd': 'xxxxxyyyyyZZZZZ'}, # (ip, subnet_mask, gateway, DNS_server)
    'WIFI_AP2': {'pwd': 'aaaaabbbbbCCCCC'}
}
f.write("Connecting to known WiFi networks...\n")
if machine.reset_cause() != machine.SOFT_RESET:
    from network import WLAN
    wl = WLAN()
    while not wl.isconnected():
        wl.mode(WLAN.STA)
        original_ssid = wl.ssid()
        original_auth = wl.auth()

        print("Scanning for known wifi nets")
        available_nets = wl.scan()
        nets = frozenset([e.ssid for e in available_nets])

        known_nets_names = frozenset([key for key in known_nets])
        net_to_use = list(nets & known_nets_names)
        try:
            net_to_use = net_to_use[0]
            net_properties = known_nets[net_to_use]
            pwd = net_properties['pwd']
            sec = [e.sec for e in available_nets if e.ssid == net_to_use][0]
            if 'wlan_config' in net_properties:
                wl.ifconfig(config=net_properties['wlan_config'])
            wl.connect(net_to_use, (sec, pwd), timeout=10000)
            while not wl.isconnected():
                machine.idle() # save power while waiting
            f.write("Connected to "+net_to_use+" with IP address: " + wl.ifconfig()[0]+"\n")

        except Exception as e:
            f.write("Failed to connect to any known network, going into AP mode\n")
            wl.init(mode=WLAN.AP, ssid=original_ssid, auth=original_auth, channel=6, antenna=WLAN.INT_ANT)
        pass
f.close()

