from .DataLogger import DataLogger


class AtmosLogger(DataLogger):
    HEADERS = ['Time', 'Pressure (Bar)', 'Temperature (C)', 'Humidity (%)']


    def __init__(self, file_name, headers=None):
        super().__init__(file_name, headers or AtmosLogger.HEADERS)


    def log_mda(self, sen, time=None):
        """ Takes a sentence and an optional timestamp and logs it."""
        try:
            data = [time, sen.b_pressure_bar, sen.air_temp, sen.humidity]
            self.log(data)
            return data
        except AttributeError:
            return None

    #TODO: Implement alternative to log_mda by getting data as arguments somehow
    #def log_mda(self, *args, **kwargs):
    #    time = kwargs.get('t', 0) or data.get('time', 0) or data.get('timestamp', None)
    #    pres = data.get('p', 0) or data.get('press', 0) or data.get('pressure', None)
    #    temp = data.get('T', 0) or data.get('temp', 0) or data.get('temperature', None)
    #    hum  = data.get('h', 0) or data.get('hum', 0) or data.get('humidity', None)
    #    
    #    self.log([time, pres, temp, hum])
        