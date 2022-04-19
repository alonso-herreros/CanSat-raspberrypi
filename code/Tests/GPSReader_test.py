from Interfacing.GPSReader import GPSReader
from Logging.GPSLogger import GPSLogger
import csv
import sys
import pytest


PORTS = {'win32': 'COM5', 'linux': '/dev/ttyACM0'}


@pytest.fixture(params=['def'])
def tmp_file(tmp_path, request):
    if request.param == None:
        return None
    else:
        return tmp_path / ('gps_test.csv' if request.param == 'def' else request.param)

@pytest.fixture
def port():
    return PORTS[sys.platform]

@pytest.fixture
def gps(tmp_file):
    with GPSReader(tmp_file) as gps:
        yield gps
        
        
def test_init_ser(gps, port):
    assert gps.port == port, 'Port not set correctly. Maybe Serial failed to open.'


@pytest.mark.parametrize('tmp_file', [None, 'def'], indirect=True)
def test_init_log(gps, tmp_file):
    assert gps.log_file == tmp_file
    assert gps.headers == (GPSLogger.HEADERS if tmp_file else None)
    assert gps.has_logger == (tmp_file != None)


@pytest.mark.parametrize('tmp_file', [None, 'def'], indirect=True)
def test_readline(gps):
    assert gps.readline().sentence_type
    assert gps.readline(True).sentence_type


def test_readline_logging(gps):
    data = [gps.readline(True) for _ in range(15)]
    gps_data = [sen for sen in data if sen.sentence_type == 'GGA' or sen.sentence_type == 'GLL']

    assert len(data) == 15, f'Expected 15 lines of data, got {len(data)}'
    assert len(gps_data) > 0, 'No GGA or GLL sentences found'

    with gps.log_file.open('r') as file:
        reader = csv.reader(file, delimiter=',')
        headers, *rows = [i for i in reader]

        assert headers == gps.headers, 'Headers were not written to file: file writing is broken'
        assert len(rows) == len(gps_data), 'Not all gps data lines were logged'

        for sen, row in zip(gps_data, rows):
            assert len(row) == 4, 'Logged line does not contain required columns'
            assert str(sen.timestamp) == row[0], 'Timestamp not logged'
            assert str(sen.lat) == row[1], 'Latitude not logged'
            assert str(sen.lon) == row[2], 'Longitude not logged'
            assert str(getattr(sen, 'altitude', '')) == row[3], 'Altitude not logged'
