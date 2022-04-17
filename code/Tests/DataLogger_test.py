from Logging.DataLogger import DataLogger
from pathlib import Path as P
import csv
import pytest


@pytest.fixture(params=['tmp_log.csv', 'tmp log.csv', 'a.csv', 'a', 'a/'])
def tmp_files(tmp_path, request):
    return tmp_path / request.param

@pytest.fixture
def tmp_file(tmp_path):
    return tmp_path / 'tmp_log.csv'

@pytest.fixture(params=[P('inner') / 'tmp.csv', P('in1') / 'in2' / 'tmp_log.csv'])
def tmp_files_inner(tmp_path, request):
    return tmp_path / request.param

@pytest.fixture
def headers_def():
    return DataLogger.DEF_HEADERS

@pytest.fixture(params=[
    ['Time', 'Data'],
    ['Time', 'Latitude', 'Longitude', 'Altitude'],
    ['Account', 'Balance'],
    ['English', 'Spanish', 'Math', 'Physics', 'Chemistry', 'History'],
])
def headers(request):
    return request.param

@pytest.fixture
def logger_def(tmp_file):
    return DataLogger(tmp_file)

@pytest.fixture
def logger(tmp_file, headers):
    return DataLogger(tmp_file, headers)


def test_init(tmp_file):
    """ Test that the logger is initialized """
    assert DataLogger(tmp_file), 'Logger not initialized'


def test_file_property(tmp_files):
    """ Test that the file property is set correctly """
    logger = DataLogger(tmp_files)
    assert logger.file == tmp_files


def test_def_properties(logger_def, headers_def):
    """ Test that the default properties are set correctly """
    assert logger_def.headers == headers_def
    assert logger_def.columns == len(headers_def)


def test_set_properties(logger, headers):
    """ Test that the properties can be set at initialization """
    assert logger.headers == headers
    assert logger.columns == len(headers)


def test_new_file(tmp_files):
    """ Test that the logger can create a new file """
    if tmp_files.exists(): tmp_files.unlink()
    logger_def = DataLogger(tmp_files)
    assert logger_def.file.is_file()


def test_existing_file(tmp_files):
    """ Test that the logger can read an existing file """
    tmp_files.touch()
    logger = DataLogger(tmp_files)
    assert logger.file.is_file()


def test_new_dir(tmp_files_inner, headers):
    """ Test that a new directory is created if it doesn't exist """
    logger = DataLogger(tmp_files_inner, headers)
    assert logger.file.is_file()


def test_log_data(logger):
    """" Test that data can be logged """
    test_data = ['2019-01-01 00:00:00', 1.234]

    logger.log_data(test_data)

    with open(logger.file_name, 'r') as file:
        reader = csv.reader(file, delimiter=',')
        _ = next(reader) # skip headers
        data = next(reader)

    assert data == [str(i) for i in test_data] # Convert data to strings before comparing


if __name__ == '__main__':
    pass