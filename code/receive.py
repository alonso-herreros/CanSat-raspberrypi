from Interfacing.ArduinoReader import ArduinoReader


if __name__ == '__main__':
    with ArduinoReader() as arduino:
        while True:
            print(arduino.readline(True))
