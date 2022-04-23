from .DataLogger import DataLogger


class AtmosLogger(DataLogger):
    HEADERS = ['Time', 'Temperature', 'Pressure', 'Humidity', 'Altitude']


    def __init__(self, file_name, headers=None):
        super().__init__(file_name, headers or AtmosLogger.HEADERS)

    
    def log_bmp(self, data):
        time = data.get('time', None)
        pres = data.get('p', 0) or data.get('press', 0) or data.get('pressure', None)
        temp = data.get('T', 0) or data.get('temp', 0) or data.get('temperature', None)
        hum = data.get('humidity', None)
        alt = data.get('altitude', None)
        
        self.log([time, pres, temp, hum, alt])
        