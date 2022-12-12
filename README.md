# socket-feeder
Wi-Fi enabled feeder controller with IP socket interface, targets the Raspberry Pi Pico W device. Code for the feeder is contained in the [server directory](server), the [client directory](client) contains a minimal application example.

## Dependencies
The target must be running a MicroPython UF2 firmware image built from the latest source code, as described in Chapter 3 of [Connecting to the internet with Pico W](https://datasheets.raspberrypi.com/picow/connecting-to-the-internet-with-pico-w.pdf). The client application example requires Python 3.6 or later.

## Configuration and Installation
The target's network configuration is held in variables in [main.py](server/main.py). These include the SSID and password of the network access point and, optionally, static configuration of IP addresses. For dynamic IP address allocation the `ipconfig` variable should be set to `None`, for static configuration it should be set with the 4 element tuple (IP address, subnet mask, gateway, DNS server).

Once [main.py](server/main.py) is configured, each of the Python files in the [server directory](server) should be copied to the target device using Thonny or similar. If dynamic IP address allocation is used the address can be found by running [main.py](server/main.py) from Thonny. When the server connects to the network its IP address will be reported in the REPL console window. The target may then be used in standalone mode as the code will execute automatically when powered.

To configure the example client application for communication with the feeder, the `HOST` variable in [feeder.py](client/feeder.py) should be set to the IP address of the feeder.

## Operation
The feeder will attempt to connect to the network when power is applied, successful connection is indicated by illumination of the on-board LED. Executing the example client application should then result in the following output:
```
Hello, you are connected to a socket feeder. I support the following commands:

Hn - Home step by n steps.
Mn - Move to position n, where n = [0, 29].

Command?
```
The feeder shutter plate may need to be aligned with a feeder well when first powering the device. This can be achieved using the Home command. There are 160 steps between each feeder well. So, if the shutter plate were half obscuring a well for example, the command `H40` or `H-40` would align the plate with the well. Once aligned, the feeder can be operated by sending move commands. Even numbered positions correspond to feeder wells and odd numbered positions to their adjacent closed locations. For example, to move to the next open from the home position send `M2`, to then close the well send `M3`.

When developing client applications for the feeder, note that commands sent over the socket interface must be terminated with a new line character, for example `M24\n`. 

## Hardware
The feeder uses a geared unipolar stepper motor, RS stock no 351-4631, which is connected to the Raspberry Pi Pico W via 4 channels of a ULN2803 driver IC as follows:

| Pico W | Signal | Motor |
|-|-|-|
| VBUS | A | Red |
| VBUS | B | Green |
| GP18 | Phase 1 | Yellow |
| GP19 | Phase 2 | Orange |
| GP20 | Phase 3 | Brown |
| GP21 | Phase 4 | Black |
