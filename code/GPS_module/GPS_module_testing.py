from serial import Serial
from time import sleep

with Serial('/dev/ttyACM0', 9600) as ser_gps:
    while True:
        for i in range(7):
            print(ser_gps.readline().decode().rstrip("\n"))
        print()
        sleep(1)