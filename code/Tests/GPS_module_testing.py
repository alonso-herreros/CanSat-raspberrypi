from serial import Serial
from time import sleep
from matplotlib import pyplot as plt
import pynmea2


USB_PORT = '/dev/ttyACM0'
BAUD_RATE = 9600


def test_serial_port():
    """ Test that the serial port is open """
    with Serial(USB_PORT, BAUD_RATE) as serial_port:
        assert serial_port.is_open


with Serial(USB_PORT, BAUD_RATE) as ser_gps:
    while True:
        line = ser_gps.readline().decode().rstrip('\r\n')

        msg = pynmea2.parse(line, check=True)

        match msg.sentence_type:
            case 'RMC' | 'GGA':
                print(f"Latitude: {msg.lat:.5f}. Longitude: {msg.lon:.5f}. Altitude: {msg.alt:.5f}")
            case 'GLL':
                print()

        sleep(0.1)


if __name__ == '__main__':
    pass