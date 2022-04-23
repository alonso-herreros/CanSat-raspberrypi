import pynmea2
from serial import Serial
from time import sleep


class ArduinoReader:
    pass


if __name__ == '__main__':
    with Serial('COM4', 115200) as arduino:
        while True:
            line = arduino.readline().decode().rstrip('\r\n')
            if line.startswith('$'):
                msg = pynmea2.parse(line, check=False)
                print(msg.data)
