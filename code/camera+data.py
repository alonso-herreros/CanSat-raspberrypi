#!/usr/bin/env python
import time
from bmp280 import BMP280
from csv import writer
import csv
from picamera import PiCamera
camera = PiCamera()

try:
       from smbus2 import SMBus
except ImportError:
       from smbus import SMBus

# Initialise the BMP280
bus = SMBus(1)
bmp280 = BMP280(i2c_dev=bus)


    
while True: 
    for i, filename in enumerate(camera.capture_continuous("/home/cansat/timelapse/image{counter:02d}.jpg")):
        temperature = bmp280.get_temperature()
        pressure = bmp280.get_pressure()
        if pressure is not None and temperature is not None:
            file = open("data.csv","a")
            file.write("{0:0.2f}".format(temperature)+","+"{0:0.2f}".format(pressure)+"\n")
            time.sleep(10)        
        else:
            file = open("data.csv","a")
            file.write("NAN     "+",")
        file.close()
    
    
    
