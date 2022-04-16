from time import sleep
import serial


# Open the serial port. ttyS0 is the mini UART serial port on GPIO 14,15 (pins 8,10)
# 19200 is the highest baudrate that the APC220 can reach
with serial.Serial('/dev/ttyS0', baudrate=19200, timeout=2) as radio:

    # Use .write(<bytes>) for transmitting data.
    # A string can be converted to bytes using .encode() or by defining it with b"string"
    radio.write("Testing serial comms. Reading input for 5 seconds...".encode())

    sleep(5)

    # The .read() method will read only 1 byte by default. Specify the max number of
    # bytes or use .readline()
    rcv = radio.read(16)

    radio.write(f"\nReceived {rcv}.\n".encode())
    print(f"Received {rcv} over serial.")
