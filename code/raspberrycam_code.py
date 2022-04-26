from Interfacing.ArduinoReader import ArduinoReader
from picamera import PiCamera
from time import sleep

camera = PiCamera()

i = 0

arduino = ArduinoReader()

while True:
    camera.capture(f'captures/{i}.jpg')
    for _ in range(5):
        arduino.readline(True)
        sleep(1)
    i += 1

