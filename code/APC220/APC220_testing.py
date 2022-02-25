from serial import Serial
from time import sleep


with Serial('/dev/ttyS0', baudrate=19200, timeout=2) as radio:
    radio.write("Testing serial comms. Reading input for 5 seconds...".encode())
    sleep(5)
    rcv = radio.read(16)
    radio.write(f"\nReceived {rcv}.\n".encode())
    print(f"Received {rcv} over serial.")