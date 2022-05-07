from Interfacing.CustomReader import CustomReader
from pathlib import Path
from serial import Serial


dir = Path() / 'logs' / 'sat'


if __name__ == '__main__':
    with CustomReader(Serial('COM6', 9600, timeout=1), dir, append=False) as receiver:
        while True:
            line = receiver.readline(True)

            if line: print(line)
