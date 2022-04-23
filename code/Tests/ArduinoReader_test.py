from Interfacing.ArduinoReader import ArduinoReader
import csv
import sys
import pytest


PORTS = {'win32': 'COM4', 'linux': '/dev/ttyACM1'}
BAUD = 115200
TIMEOUT = 1.2
EXPECTED_SENTENCES = ['TXT', 'GGA', 'GLL', 'MDA']


#TODO: Create a mock serial object for testing without an actual arduino
@pytest.fixture
def device():
    return None

@pytest.fixture
def port():
    return PORTS[sys.platform]


@pytest.fixture
def arduino(tmp_path, port):
    with ArduinoReader(port=port, baud=BAUD, timeout=TIMEOUT) as arduino:
        yield arduino



def test_init(tmp_path):
    """ Test that the logger is initialized with the right properties"""
    arduino = ArduinoReader(tmp_path)
    assert arduino, 'Reader not initialized'
    assert arduino.log_dir == tmp_path, 'Dir not set correctly'
    assert ArduinoReader().log_dir, 'No default dir is set'


def test_readline(arduino):
    lines = [arduino.readline(False) for _ in range(3)]
    assert len([line for line in lines if line]), 'No line read' #Count non-empty lines


def test_readline_mda(arduino):
    lines = [arduino.readline(False) for _ in range(3)]
    mda_lines = [sen for sen in lines if sen and sen.sentence_type == 'MDA']
    assert len(lines) == 3, f'Expected 5 lines of data, got {len(lines)}'
    assert len(mda_lines) > 0, 'No MDA sentences found'


def test_readline_logging(arduino):
    lines = [arduino.readline(True) for _ in range(5)]
    mda_lines = [sen for sen in lines if (sen and sen.sentence_type == 'MDA')]
    gps_lines = [sen for sen in lines if (sen and (sen.sentence_type == 'GGA' or sen.sentence_type == 'GLL'))]

    assert len(lines) == 5, f'Expected 5 lines of data, got {len(lines)}'
    assert len(mda_lines) + len(gps_lines) > 0, 'No MDA, GGA or GLL sentences found at all'
    
    with arduino.log_file_atmos.open('r') as file:
        reader = csv.reader(file, delimiter=',')
        _, *rows = [i for i in reader]
        assert len(rows) == len(mda_lines), 'Not all data lines were logged'

        for sen, row in zip(mda_lines, rows):
            assert len(row) == 4, 'Logged line does not contain required columns'
            assert str(sen.b_pressure_bar or '') == row[1], 'Pressure not logged'
            assert str(sen.air_temp or '') == row[2], 'Temperature not logged'
            assert str(sen.rel_humidity or '') == row[3], 'Humidity not logged'

    with arduino.log_file_gps.open('r') as file:
        reader = csv.reader(file, delimiter=',')
        _, *rows = [i for i in reader]
        assert len(rows) == len(gps_lines), 'Not all data lines were logged'

        for sen, row in zip(gps_lines, rows):
            assert len(row) == 4, 'Logged line does not contain required columns'
            assert str(sen.timestamp or '') == row[0], 'Timestamp not logged'
            assert str(sen.lat or '') == row[1], 'Latitude not logged'
            assert str(sen.lon or '') == row[2], 'Longitude not logged'
            assert str(getattr(sen, 'altitude', '')) == row[3], 'Altitude not logged'
