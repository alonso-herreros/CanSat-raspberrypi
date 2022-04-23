from .DataLogger import DataLogger


class GPSLogger(DataLogger):
    HEADERS = ['Time', 'Latitude', 'Longitude', 'Altitude']


    def __init__(self, file_name, headers=None):
        super().__init__(file_name, headers or GPSLogger.HEADERS)

    
    def log_sentence(self, sen):
        try:
            data = [sen.timestamp, sen.lat, sen.lon, getattr(sen, 'altitude', None)]
            self.log(data)
            return data
        except AttributeError:
            return None