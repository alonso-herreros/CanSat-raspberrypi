from Interfacing.ArduinoReader import ArduinoReader
import pytest

#TODO: Create a mock serial object for testing without an actual arduino
@pytest.fixture
def device():
    return None


@pytest.fixture
def reader(tmp_path, device):
    return ArduinoReader(tmp_path, port=device.port)



def test_init(tmp_path):
    """ Test that the logger is initialized with the right properties"""
    reader = ArduinoReader(tmp_path)
    assert reader, 'Reader not initialized'
    #TODO: Uncomment when Loggers are implemented in ArduinoReader
    #assert reader.log_dir == tmp_path, 'Dir not set correctly'
    #assert ArduinoReader().log_dir, 'No default dir is set'


def test_readline(tmp_path):
    pass
