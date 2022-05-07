from .Reader import Reader
import pynmea2


class GPSReader(Reader):
    APPEND = False

    def __init__(self, source, dir, append=APPEND):
        logs = {
            'dump': {'file': dir / 'dump.csv',
                'append': append,
                'fields': dict(zip(
                    ['$time', 'message'],
                    ['Time', 'Message'])),
                'filter': lambda x: [None, str(x)] if x else None,
            },
            'loc': {'file': dir / 'gps.csv',
                'append': append,
                'file': dir / 'gps.csv',
                'fields': dict(zip(
                    ['$time', 'latitude', 'longitude', 'altitude'],
                    ['Time', 'Latitude', 'Longitude', 'Altitude'])),
                'filter': lambda x: x if getattr(x, 'sentence_type', None) in ['RMC', 'GGA'] else None,
            },
            'txt': {'file': dir / 'txt.csv',
                'append': append,
                'fields': dict(zip(
                    ['$time', 'text'],
                    ['Time', 'Message'])),
                'filter': lambda x: x if getattr(x, 'sentence_type', None) == 'TXT' else None,
            },
        }

        super().__init__(source, loggers=logs)


    @staticmethod
    def filter(line):
        try:
            line = pynmea2.parse(line)
            return line
        except pynmea2.ParseError:
            return None # That was not our message, or it was corrupted
