from serial import Serial
from time import sleep

port = Serial('/dev/ttyS0', baudrate=19200, timeout=2)

port.write("Testing APC220. Reading input for 5 seconds...".encode())

sleep(5)
rcv = port.read(16)
port.write(f"\nReceived {rcv}.\n".encode())
print(f"Received {rcv} over serial.")