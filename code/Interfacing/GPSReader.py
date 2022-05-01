# Currently broken

from serial import Serial, serialutil
from Logging.GPSLogger import GPSLogger
import pynmea2
import sys


class GPSReader:
    DEF_PORTS = {'win32': 'COM5', 'linux': '/dev/ttyACM0'}
    DEF_BAUD = 9600
    DEF_TIMEOUT = 1.2


    def __init__(self, file=None, headers=None, port=None, baud=None, timeout=None):
        try:
            self._ser = Serial(
                port=port or GPSReader.DEF_PORTS[sys.platform],
                baudrate=baud or GPSReader.DEF_BAUD,
                timeout=timeout or GPSReader.DEF_TIMEOUT
            )
        except serialutil.SerialException:
            self._ser = None

        self._logger = GPSLogger(file, headers) if file else None


    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


    @property
    def port(self):
        return self._ser.port if self._ser else None

    @property
    def ser_satus(self):
        return (True if self._ser.is_open else False) if self._ser else None

    @property
    def log_file(self):
        return self._logger.file if self._logger else None

    @property
    def headers(self):
        return self._logger.headers if self._logger else None

    @property
    def has_logger(self):
        return True if self._logger else False


    def close(self):
        if self._ser: self._ser.close()


    def readline(self, log=False):
        if not self._ser:
            raise AttributeError('Serial is not set. Maybe it failed to open.')

        line = self._ser.readline().decode().rstrip('\r\n')
        data = pynmea2.parse(line, check=True)

        if log and self.has_logger:
            return self._logger.log_sentence(data)
        else:
            return data