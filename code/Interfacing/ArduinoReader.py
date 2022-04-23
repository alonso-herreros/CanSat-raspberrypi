from serial import Serial, serialutil
from pathlib import Path
from time import sleep
import pynmea2
import sys
from Logging.GPSLogger import GPSLogger 
from Logging.AtmosLogger import AtmosLogger


class ArduinoReader:
    DEF_PORTS = {'win32': 'COM4', 'linux': '/dev/ttyACM1'}
    DEF_BAUD = 115200
    DEF_TIMEOUT = 1.2

    
    def __init__(self, dir=True, port=None, baud=None, timeout=None):
        try:
            self._ser = Serial(
                port=port or ArduinoReader.DEF_PORTS[sys.platform],
                baudrate=baud or ArduinoReader.DEF_BAUD,
                timeout=timeout or ArduinoReader.DEF_TIMEOUT
            )
        except serialutil.SerialException:
            self._ser = None

        dir = Path(__file__).parent / 'arduino_log' if dir == True else dir
        self._gps_logger = GPSLogger(dir / 'gps.csv') if dir else None
        self._atmos_logger = AtmosLogger(dir / 'atmos.csv') if dir else None


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
    def log_dir(self):
        return self._gps_logger.file.parent if self._gps_logger else None

    @property
    def log_file_gps(self):
        return self._gps_logger.file if self._gps_logger else None
    @property
    def log_file_atmos(self):
        return self._atmos_logger.file if self._atmos_logger else None

    @property
    def has_logger(self):
        return True if self._gps_logger and self._atmos_logger else False


    def close(self):
        if self._ser: self._ser.close()


    def readline(self, log=True):
        if not self._ser:
            raise AttributeError('Serial is not set. Maybe it failed to open.')

        line = self._ser.readline().decode()
        if not line.startswith('$'): return ''
        sen = pynmea2.parse(line)

        if log and self.has_logger:
            if sen.sentence_type == 'MDA':
                self._atmos_logger.log_sentence(sen)
            elif sen.sentence_type == 'GGA':
                self._gps_logger.log_sentence(sen)
        return sen


