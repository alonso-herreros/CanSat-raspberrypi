from serial import Serial
from time import sleep


class ArduinoReader:
    pass


if __name__ == '__main__':
    with Serial('/dev/ttyACM1') as arduino, open('test.txt', 'w') as fp:
    
        lines = []
        for _ in range(10):
            if arduino.in_waiting:
                lines.append(arduino.readline().decode().rstrip('\n\r') + '\n')
                print(len(lines))
            sleep(0.2)
        
        fp.writelines(lines)
