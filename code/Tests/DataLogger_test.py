from Logging.DataLogger import DataLogger
import csv
import pytest


test_headers = ['timestamp', 'value']

@pytest.fixture
def tmp_file(tmp_path):
    return tmp_path / 'tmp_log.csv'

@pytest.fixture
def logger(tmp_file):
    return DataLogger(tmp_file, test_headers)


def test_init_properties(tmp_file):
    """ Test that the logger is initialized """
    logger = DataLogger(tmp_file)

    assert logger.file_name == tmp_file


def test_init_headers(tmp_file):
    """ Test that the logger is initialized and headers logged """
    logger = DataLogger(tmp_file, test_headers)
    assert logger.headers == test_headers


def test_init_new_dir(tmp_path):
    """ Test that a new directory is created if it doesn't exist """
    tmp_file = tmp_path / 'tmp_dir' / 'tmp_log.csv'

    logger = DataLogger(tmp_file, test_headers)

    assert logger.file_name == tmp_file
    assert logger.headers == test_headers


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
    test_init_properties()