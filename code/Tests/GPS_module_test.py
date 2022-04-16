# Code working
from serial import Serial
import pynmea2
import sys
import pytest


PORTS = {'win32': 'COM5', 'linux': '/dev/ttyACM0'}
BAUD = 9600
TIMEOUT = 1.2
GPS_TYPES = ['TXT', 'GGA', 'GLL', 'GSA', 'GSV', 'RMC', 'VTG']


@pytest.fixture
def port():
    return PORTS[sys.platform]

@pytest.fixture
def serial(port):
    with Serial(port, BAUD, timeout=TIMEOUT) as serial:
        yield serial
    if serial.is_open: serial.close()

@pytest.fixture
def lines(serial):
    return [nextline(serial) for _ in range(15)]

@pytest.fixture
def msgs(lines):
    return [pynmea2.parse(line, check=True) for line in lines]

def nextline(ser):
    return ser.readline().decode().rstrip('\r\n')


def test_serial_port(port):
    """ Test that the serial port can be opened """
    with Serial(port, BAUD) as serial:
        assert serial.is_open


def test_receiving_data(serial):
    """ Test that the serial port is receiving data """
    #with Serial(PORT, BAUD, timeout=TIMEOUT) as ser:
    assert serial.read(1)


def test_receiving_nmea_sentences(lines):
    """ Test that the serial port is receiving NMEA sentences """
    for line in lines:
        assert line.startswith('$')
        assert pynmea2.parse(line, check=True)


def test_receiving_gps_sentences(msgs):
    """ Test that the serial port is receiving GPS sentences """
    for msg in msgs:
        assert msg.sentence_type in GPS_TYPES


def test_receiving_gps_pos(msgs):
    """ Test that the serial port is receiving GPS position data """
    for msg in msgs:
        if msg.sentence_type == 'GGA':
            assert msg.timestamp and msg.lat and msg.lon and msg.altitude
            return
    assert 0, 'No GGA message received'


if __name__ == '__main__':
    pass