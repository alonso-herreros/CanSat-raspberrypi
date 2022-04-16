from Interfacing.GPSReader import GPSReader
from pathlib import Path
import sys
import pytest


PORTS = {'win32': 'COM5', 'linux': '/dev/ttyACM0'}
BAUD = 9600
TIMEOUT = 1.2


def test_init():
    gps = GPSReader()
    assert gps.port == PORTS[sys.platform]
    assert gps.has_logger
    assert gps.log_file == Path(__file__).parent.parent / 'datalogs' / 'gps_def.csv'