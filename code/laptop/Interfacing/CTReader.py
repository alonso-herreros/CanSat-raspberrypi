from .Reader import Reader


class CTReader(Reader):
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
                    ['TIM', 'LAT', 'LON', 'ALT'],
                    ['Time', 'Latitude', 'Longitude', 'Altitude'])),
                'filter': lambda x: self.parse(x),
            },
            'atmos': {'file': dir / 'atmos.csv',
                'append': append,
                'fields': dict(zip(
                    ['TIM', 'TEM', 'HUM'],
                    ['Time', 'Temperature (C)', 'Humidity (%)'])),
                'filter': lambda x: self.parse(x),
            }
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
        time, data = line[:19], line[19:]
        main = {'TIM': time} | {k: v for k, v in [f.split(':') for f in data[4:].split(',')]}
        return 
