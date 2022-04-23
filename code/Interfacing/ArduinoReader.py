from serial import Serial, serialutil
from pathlib import Path
from time import sleep
import pynmea2
import sys
#TODO: Uncomment when GPSLogger and AtmosLogger are implemented
#from Logging.GPSLogger import GPSLogger 
#from Logging.AtmosLogger import AtmosLogger


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
        #TODO: Switch False for dir when Loggers are implemented
        self._gps_logger = GPSLogger(dir / 'gps.csv') if False else None
        self._atmos_logger = AtmosLogger(dir / 'atmos.csv') if False else None


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
    def has_loggers(self):
        return True if self._gps_logger and self._atmos_logger else False


    def close(self):
        if self._ser: self._ser.close()


    def readline(self, log=True):
        if not self._ser:
            raise AttributeError('Serial is not set. Maybe it failed to open.')

        line = self._ser.readline().decode().rstrip('\r\n')
        if line == "": return line
        data = pynmea2.parse(line)

        if log and self.has_logger:
            if data.sentence_type == 'MDA':
                return self._atmos_logger.log_sentence(data)
            elif data.sentence_type == 'GGA':
                return self._gps_logger.log_sentence(data)
        else:
            return data


