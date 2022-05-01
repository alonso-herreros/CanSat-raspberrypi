from serial import Serial, serialutil
from pathlib import Path
import pynmea2
import sys
from DataLogger import DataLogger


class ArduinoReader:
    DEF_PORTS = {'win32': 'COM4', 'linux': '/dev/ttyACM0'}
    DEF_BAUD = 9600
    DEF_TIMEOUT = 1.2

    LOGS = {
        'dump': {
            'file': 'dump.csv',
            'fields': dict(zip(
                ['$time', 'message'],
                ['Time', 'Message'])),
            'filter': lambda x: [None, str(x)] if x else None,
        },
        'gps': {
            'file': 'gps.csv',
            'fields': dict(zip(
                ['timestamp', 'lat', 'lon', 'altitude'],
                ['Time', 'Latitude', 'Longitude', 'Altitude'])),
            'filter': lambda x: x if x.sentence_type == 'GGA' else None,
        },
        'atmos': {
            'file': 'atmos.csv',
            'fields': dict(zip(
                ['$time', 'b_pressure_bar', 'air_temp', 'rel_humidity'],
                ['Time', 'Pressure (Bar)', 'Temperature (C)', 'Humidity (%)'])),
            'filter': lambda x: x if x.sentence_type == 'MDA' else None,
        },
        'txt': {
            'file': 'txt.csv',
            'fields': dict(zip(
                ['$time', 'text'],
                ['Time', 'Message'])),
            'filter': lambda x: x if x.sentence_type == 'TXT' else None,
        },
    }

    
    def __init__(self, dir=True, port=None, baud=None, timeout=None):
        try:
            self._ser = Serial(
                port=port or ArduinoReader.DEF_PORTS[sys.platform],
                baudrate=baud or ArduinoReader.DEF_BAUD,
                timeout=1.2
            )
        except serialutil.SerialException:
            self._ser = None

        self._dir = Path() / 'arduino_log' if dir == True else dir

        if self._dir:
            self._loggers = {
                k: DataLogger(self._dir / v['file'], v['fields'], v.get('filter'))
                for k, v in ArduinoReader.LOGS.items()
            }


    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


    @property
    def port(self):
        return self._ser.port if self._ser else None
    @property
    def baud(self):
        return self._ser.baudrate if self._ser else None

    @property
    def ser_satus(self):
        return (True if self._ser.is_open else False) if self._ser else None

    @property
    def log_dir(self):
        return self._dir if self._dir else None
    @property
    def log_files(self):
        return {k: self._dir / l.file for k, l in self._loggers.items()}

    @property
    def has_loggers(self):
        return True if [i for i in self._loggers if i] else False


    def close(self):
        if self._ser: self._ser.close()


    def readline(self, log=True):
        if not self._ser:
            raise AttributeError('Serial is not set. Maybe it failed to open.')

        line = self._ser.readline()
        try:
            line = line.decode('ascii')
        except UnicodeDecodeError:
            return 'ERROR: Can\'t decode'

        if not line.startswith('$'):
            return None
        line = line.rstrip('\r\n')
        try:
            sen = pynmea2.parse(line, check=False)
        except pynmea2.nmea.ParseError:
            return 'ERROR: Can\'t parse'

        if log and self.has_loggers:
            for logger in self._loggers.values():
                logger.log(sen)
        return sen


