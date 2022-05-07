from .Reader import Reader


class CustomReader(Reader):
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
            'gps': {'file': dir / 'gps.csv',
                'append': append,
                'fields': dict(zip(
                    ['$time', 'LAT', 'LON', 'ALT'],
                    ['Time', 'Latitude', 'Longitude', 'Altitude'])),
                'filter': lambda x: self.parse(x) | {'$time': None},
            },
            'atmos': {'file': dir / 'atmos.csv',
                'append': append,
                'fields': dict(zip(
                    ['$time', 'TEM', 'HUM'],
                    ['Time', 'Temperature (C)', 'Humidity (%)'])),
                'filter': lambda x: self.parse(x) | {'$time': None},
            },
            'txt': {'file': dir / 'txt.csv',
                'append': append,
                'fields': dict(zip(
                    ['$time', 'text'],
                    ['Time', 'Message'])),
                'filter': lambda x: [None, *[self.parse(x)[i] for i in ('TXT', 'WRN', 'TXW') if i in x]],
            },
        }

        super().__init__(source, loggers=logs)


    @staticmethod
    def filter(line):
        try:
            line = line.split('$')[-1] # Start reading from the last $
            line = line.split(';')[0] # Only read until the first ';'
            assert line[0:4] == '[DR]' # It should have the [DR] prefix
            return line
        except (IndexError, AssertionError):
            return None # That was not our message, or it was corrupted


    @staticmethod
    def parse(line):
        return {k: v for k, v in [f.split(':') for f in line[4:].split(',')]}
