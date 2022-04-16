from serial import Serial
from pathlib import Path
from Logging.GPSLogger import GPSLogger
import pynmea2


class GPSReader:
    DEF_PORT = '/dev/ttyACM0'
    DEF_END = 'GLL'


    def __init__(self, port=DEF_PORT, logger=True):
        self._port = port

        self.logger = logger

        try:
            self._ser = Serial(self.port, 9600, timeout=0)
        except OSError as e:
            print(f"OSError: {e}")


    def __del__(self):
        self._ser.close()


    @property
    def logger(self):
        return self._logger

    @logger.setter
    def logger(self, val):
        if val == True:
            self._logger = GPSLogger(Path('.') / 'datalogs' / 'gps_def.csv')
        else:
            self._logger = val or None

    @property
    def port(self):
        return self._port


    def read(self, noLog=False):
        line = self._ser.readline().decode().rstrip('\r\n')
        data = pynmea2.parse(line, check=True)

        if not noLog and self._logger:
            self._logger.log_sentence(data)

        return data