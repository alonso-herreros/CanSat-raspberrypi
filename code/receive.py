from Interfacing.ArduinoReader import ArduinoReader
from pathlib import Path


if __name__ == '__main__':
    with ArduinoReader(Path('dev/ttyACM0')) as arduino:
        while True:
            print(arduino.readline(True))
