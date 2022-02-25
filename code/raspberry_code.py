#Photoshoot and recording program for CanSat
#Importing libraries
import time
from bmp280 import BMP280
from picamera import PiCamera
from time import sleep

#Sent countdown for launch
countdown = int()

#Setting up the camera
camera = PiCamera()

#BMP280 set-up
try:
    from smbus2 import SMBus
except ImportError:
    from smbus import SMBus

bus = SMBus(1)
bmp280 = BMP280(i2c_dev=bus)

#Actual program
sleep(countdown) #Insert value in seconds in brackets

#Getting temperature parameters
while True:
    temperature = bmp280.get_temperature()
    print('{:05.2f}*C'.format(temperature))
    time.sleep(2)

#TESTING
#camera.start_preview()

camera.start_recording('/home/pi/Desktop/launch/launch.h264')
sleep(15)
camera.stop_recording()

for i in range (4):
    sleep(3)
    camera.capture('/home/pi/Desktop/captures/image%s.jpg' % i)

sleep(5)

#Record for 30 seconds
camera.start_recording('/home/pi/Desktop/video/video1.h264')
sleep(30)
camera.stop_recording()





