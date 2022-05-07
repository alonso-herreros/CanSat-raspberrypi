from pathlib import Path
<<<<<<< Updated upstream
import pynmea2
import sys
from .Logger import Logger
=======
from .Logger import Logger
from serial import serialutil
>>>>>>> Stashed changes


class Reader:
    DEF_LOGS = {
        'dump': {
            'file': Path() / 'logs' / 'dump.csv',
            'fields': dict(zip(
                ['$time', 'message'],
                ['Time', 'Message'])),
            'filter': lambda x: [None, str(x)] if x else None
        }
    }

    
    def __init__(self, source, loggers=None, filter=None):
        self._source = source
        self._filter = filter or (lambda x: x if x else None)

        loggers = loggers or Reader.DEF_LOGS if loggers is not False else {}
        if loggers and not hasattr([*loggers.values()][0], 'log'):
            self.loggers = {name: Logger(**params) for name, params in loggers.items()}
        else:
            self.loggers = loggers

    @property
    def source(self):
        return self._source

    @property
    def has_loggers(self):
        return True if [i for i in self.loggers if i] else False
    @property
    def log_files(self):
        return {k: log.file for k, log in self.loggers.items() if log}


    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        getattr(self._source, 'close', lambda: None)()


    def filter(self, line):
        return getattr(self, '_filter', lambda x: x)(line)


    def readline(self, log=True):
        try:
            line = self._source.readline()
            line = getattr(line, 'decode', lambda: line)()
            line = line.rstrip(' \r\n') # Remove these - they may confuse the parser
            line = self.filter(line)
            assert line
        except serialutil.SerialException:
            try:
                self._source.close()
                self._source.open()
            finally:
                return None
        except (AttributeError, AssertionError):
            return None

        if log and self.loggers:
            for logger in self.loggers.values():
                logger.log(line)

        return line
