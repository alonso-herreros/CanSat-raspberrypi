from Interfacing.ArduinoReader import ArduinoReader


if __name__ == '__main__':
    with ArduinoReader(baud=19200) as arduino:
        while True:
            print(arduino.readline(True))
