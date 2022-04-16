from serial import Serial
from pathlib import Path
from Logging.GPSLogger import GPSLogger
import pynmea2
import sys
import os


class GPSReader:
    DEF_PORTS = {'win32': 'COM5', 'linux': '/dev/ttyACM0'}
    DEF_ENDER = 'GLL'


    def __init__(self, port=None, log=True):
        self._port = port or self.DEF_PORTS[sys.platform]
        self._ser = Serial(port, 9600, timeout=1.2)

        match log:
            case True:
                log_file = Path(__file__).parent.parent / 'datalogs' / 'gps_def.csv'
            case rel if rel.startswith('.'):
                log_file = Path(__file__).parent.parent / rel
            case abs:
                log_file = Path(abs)

        self._logger = GPSLogger(log_file) if log else None


    def __del__(self):
        self._ser.close()


    @property
    def port(self):
        return self._port

    @property
    def has_logger(self):
        return self._logger != None

    @property
    def log_file(self):
        return self._logger.file_name


    def read(self, noLog=False):
        line = self._ser.readline().decode().rstrip('\r\n')
        data = pynmea2.parse(line, check=True)

        if not noLog and self.has_logger:
            self._logger.log_sentence(data)

        return data