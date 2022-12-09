"""Socket feeder device - application entry point.

Receives messages over a wireless network connection and passes them to the feeder module.
"""
from machine import Pin
import network
import socket
import time
import feeder

led = Pin('LED', Pin.OUT)
led.value(False)

# Network configuration, define ipconfig for static IP address allocation.
PORT = 65535
ipconfig = None
#ipconfig = ('192.168.1.166', '255.255.255.0', '192.168.1.254', '192.168.1.254')
ssid = 'DESKTOP-IMC5RTM 4824'
password = '+50Q469d'

# Instance network interface and connect.
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)
print('Waiting for network connection... ', end='')
timer = 10
while wlan.status() != 3 and timer > 0:
    time.sleep(1)
    timer -= 1

# Configure IP.
if wlan.status() == 3:
    print('OK')
    if ipconfig is None:
        ipconfig = wlan.ifconfig()
    else:
        wlan.ifconfig(ipconfig)
    print('Address =', ipconfig[0])
else:
    raise RuntimeError('Network connection failed')

# Open network socket.
s = socket.socket()
s.bind(('', PORT))

# Listen for connections.
led.value(True)
s.listen()
while True:
    try:
        # Connect and send help text.
        conn, addr = s.accept()
        print('A client connected from', addr)
        conn.write(feeder.clienthelp.encode())
        # Process commands.
        while True:
            line = conn.readline()
            if not line or line == b'\r\n':
                break
            feeder.process(line)
    except OSError as e:
        conn.close()
        print('Connection closed')
