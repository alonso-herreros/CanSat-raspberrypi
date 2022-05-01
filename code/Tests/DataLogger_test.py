from Interfacing.DataLogger import DataLogger
from pathlib import Path
import csv
import pytest


class SampleLog:
    def __init__(self, *args):
        self._fields = args[0]
        self._data = args[1] if len(args) == 2 else args[1:]
        
        
    @property
    def fields(self): return self._fields

    @property
    def data(self): return self._data
    
    @property
    def headers(self): return [*getattr(self.fields, 'values', lambda: self.fields)()]

    @property
    def rows(self): return [self.headers, *self._data]


SAMPLES = {
    'default': SampleLog(
        DataLogger.DEF_FIELDS, 
        [1.234],
        [5.678],
    ),
    'gps': SampleLog(
        ['Time', 'Latitude', 'Longitude', 'Altitude'],
        ['2019-01-01 00:00:00', 1.234, 5.678, 912],
        ['2019-01-01 00:00:30', 2.345, 6.789, 123],
    ),
    'gps_nmea': SampleLog(
        {'timestamp':'Time', 'lat':'Latitude', 'lon':'Longitude', 'altitude':'Altitude'},
        ['2019-01-01 00:00:00', 1.234, 5.678, 912],
        ['2019-01-01 00:00:30', 2.345, 6.789, 123],
    ),
    'time_data': SampleLog(
        ['Time', 'Data'],
        ['2019-01-01 00:00:00', 1.234],
        ['2019-01-01 00:00:30', 5.678],
    ),
    'subjects': SampleLog(
        ['English', 'Spanish', 'Math', 'Physics', 'Chemistry'],
        ['0:00', '0:30', '1:30', '1:00', '1:00'],
        ['0:05', '0:00', '0:00', '3:00', '1:00'],
        ['0:00', '0:30', '0:30', '0:00', '0:30'],
    ),
}

FILE_CASES = {
    'simple': ['tmp.csv', 0],
    'single': ['a', 1],
    'inner':  ['inner/tmp.csv', 0],
    'inner2': ['in1/in2/tmp.csv', 0],
    'in_ner': ['in ner/tmp.csv', 1],
}


@pytest.fixture(params=['default'])
def sample(request):
    return SAMPLES[request.param]
@pytest.fixture
def fields(sample):
    return sample.fields
@pytest.fixture
def data(sample):
    return sample.data
@pytest.fixture
def headers(sample):
    return sample.headers

@pytest.fixture(params=['simple'])
def tmp_file(tmp_path, request):
    file, exist = FILE_CASES[request.param]
    tmp_file = tmp_path / file

    match exist: # Will the file exist?
        case (True | 1): # File will exist
            tmp_file.parent.mkdir(parents=True, exist_ok=True)
            tmp_file.touch()
        case (False | 0): # File will not exist
            if tmp_file.exists(): tmp_file.unlink()
        case -1: # File's parent directory will not exist
            if tmp_file.exists(): tmp_file.unlink()
            if tmp_file.parent.is_dir(): tmp_file.parent.remove()

    yield tmp_file
    tmp_file.unlink() # Delete the file after use

@pytest.fixture
def logger(tmp_file, fields):
    return DataLogger(tmp_file, fields)


@pytest.mark.parametrize('sample', SAMPLES.keys(), indirect=True)
def test_init(tmp_file, fields, headers):
    """ Test that the logger is initialized with the right properties"""
    logger = DataLogger(tmp_file, fields)
    assert logger, 'Logger not initialized'
    assert logger.headers == [*getattr(fields, 'values', lambda: fields)()]
    assert logger.fields == [*getattr(fields, 'keys', lambda: [i.lower() for i in fields])()]


@pytest.mark.parametrize('tmp_file', FILE_CASES.keys(), indirect=True)
def test_file_creation(tmp_file):
    """ Test that the file is set up correctly """
    logger = DataLogger(tmp_file)
    assert logger.file == Path(tmp_file).resolve(), 'Path property not set correctly'
    assert logger.file.is_file(), 'File not created'


@pytest.mark.parametrize('sample', SAMPLES.keys(), indirect=True)
def test_write_headers(logger, headers):
    """ Test that the headers are written correctly """
    with logger.file.open('r') as file:
        reader = csv.reader(file, delimiter=',')
        assert next(reader) == headers, 'Headers not written correctly'


@pytest.mark.parametrize('sample', SAMPLES.keys(), indirect=True)
def test_log_data(logger, sample):
    """" Test that data can be logged """
    for entry in sample.data: logger.log(entry)

    with logger.file.open('r') as file:
        reader = csv.reader(file, delimiter=',')
        for i, row in enumerate(reader):
            assert row == [str(j) for j in sample.rows[i]]
