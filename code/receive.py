from Interfacing.ArduinoReader import ArduinoReader
from Interfacing.DataLogger import DataLogger
from pathlib import Path


dir = Path() / 'logs'

logs = {
    'dump': {
        'file': dir / 'dump.csv',
        'fields': dict(zip(
            ['$time', 'message'],
            ['Time', 'Message'])),
        'filter': lambda x: [None, str(x)] if x else None,
    },
    'gps': {
        'file': dir / 'gps.csv',
        'fields': dict(zip(
            ['timestamp', 'lat', 'lon', 'altitude'],
            ['Time', 'Latitude', 'Longitude', 'Altitude'])),
        'filter': lambda x: x if getattr(x, 'sentence_type', None) == 'GGA' else None,
    },
    'atmos': {
        'file': dir / 'atmos.csv',
        'fields': dict(zip(
            ['$time', 'b_pressure_bar', 'air_temp', 'rel_humidity'],
            ['Time', 'Pressure (Bar)', 'Temperature (C)', 'Humidity (%)'])),
        'filter': lambda x: x if getattr(x, 'sentence_type', None) == 'MDA' else None,
    },
    'txt': {
        'file': dir / 'txt.csv',
        'fields': dict(zip(
            ['$time', 'text'],
            ['Time', 'Message'])),
        'filter': lambda x: x if getattr(x, 'sentence_type', None) == 'TXT' else None,
    },
}


if __name__ == '__main__':
    with ArduinoReader(baud=19200, loggers=logs) as arduino:
        while True:
            line = arduino.readline(True)
            print(line)
