from Interfacing.GPSReader import GPSReader
from pathlib import Path
from serial import Serial


dir = Path() / 'logs' / 'gps'


if __name__ == '__main__':
    with GPSReader(Serial('COM7', 9600, timeout=1), dir, append=False) as receiver:
        while True:
            line = receiver.readline(True)

            print(line)
