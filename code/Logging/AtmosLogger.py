from .DataLogger import DataLogger


class AtmosLogger(DataLogger):
    HEADERS = ['Time', 'Pressure', 'Temperature', 'Humidity', 'Altitude']


    def __init__(self, file_name, headers=None):
        super().__init__(file_name, headers or AtmosLogger.HEADERS)

    
    def log_bmp(self, data):
        time = data.get('t', 0) or data.get('time', 0) or data.get('timestamp', None)
        pres = data.get('p', 0) or data.get('press', 0) or data.get('pressure', None)
        temp = data.get('T', 0) or data.get('temp', 0) or data.get('temperature', None)
        hum  = data.get('h', 0) or data.get('hum', 0) or data.get('humidity', None)
        alt  = data.get('a', 0) or data.get('alt', 0) or data.get('altitude', None)
        
        self.log([time, pres, temp, hum, alt])
        