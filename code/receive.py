from Interfacing.ArduinoReader import ArduinoReader


def main():
    print(arduino.readline(True))


if __name__ == '__main__':
    with ArduinoReader() as arduino:
        while True:
            main()