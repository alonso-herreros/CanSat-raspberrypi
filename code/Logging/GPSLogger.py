from .DataLogger import DataLogger


class GPSLogger(DataLogger):
    _HEADERS = ['Time', 'Latitude', 'Longitude', 'Altitude']


    def __init__(self, file_name):
        super().__init__(file_name, self._HEADERS)

    
    def log_sentence(self, sen):
        try:
            data = [sen.timestamp, sen.lat, sen.lon, sen.altitude]
            self.log_data(data)
            return data
        except AttributeError:
            raise AttributeError('Sentence does not have the required attributes')