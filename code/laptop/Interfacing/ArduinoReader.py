from serial import Serial, serialutil
from pathlib import Path
import pynmea2
import sys
from .Logger import Logger


class ArduinoReader:
    DEF_PORTS = {'win32': 'COM4', 'linux': '/dev/ttyACM0'}
    DEF_BAUD = 9600
    DEF_TIMEOUT = 1.2
    DEF_LOGS = {
        'dump': {
            'file': Path() / 'logs' / 'dump.csv',
            'fields': dict(zip(
                ['$time', 'message'],
                ['Time', 'Message'])),
            'filter': lambda x: [None, str(x)] if x else None
        }
    }

    
    def __init__(self, port=None, baud=None, timeout=None, loggers=None):
        try:
            self._ser = Serial(
                port=port or ArduinoReader.DEF_PORTS[sys.platform],
                baudrate=baud or ArduinoReader.DEF_BAUD,
                timeout=timeout or ArduinoReader.DEF_TIMEOUT
            )
        except serialutil.SerialException:
            self._ser = None

        loggers = loggers or ArduinoReader.DEF_LOGS if loggers is not False else {}
        if loggers and not hasattr([*loggers.values()][0], 'log'):
            self.loggers = {name: Logger(**params) for name, params in loggers.items()}
        else:
            self.loggers = loggers

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
        return self.loggers.values()[0].file.parent if self.has_loggers else None
    @property
    def log_files(self):
        return {k: log.file for k, log in self.loggers.items() if log}

    @property
    def has_loggers(self):
        return True if [i for i in self.loggers if i] else False


    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        if self._ser: self._ser.close()


    def readline(self, log=True):
        try:
            line = self._ser.readline().decode()
        except (serialutil.SerialException, UnicodeDecodeError):
            # Serial not open or error decoding line. Which one is it? Don't know, don't care
            return None

        line = line.rstrip(' \r\n') # Remove these - they may confuse the parser
        if not line: return '' # Empty line?

        try:
            sen = pynmea2.parse(line, check=False)
        except pynmea2.nmea.ParseError: # Can't parse? Just return the line
            return line

        if log and self.loggers:
            for logger in self.loggers.values():
                logger.log(sen)

        return sen
