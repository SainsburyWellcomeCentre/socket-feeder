#!/usr/bin/env python3

"""Socket feeder example client application."""

import socket

HOST = '192.168.137.122'
PORT = 65535

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # Connect to the feeder.
    s.connect((HOST, PORT))
    # Display the feeder's welcome message.
    print(s.recv(1024).decode())
    # Read and send commands.
    while True:
        command = input('Command? ') + '\n'
        s.sendall(command.encode())
