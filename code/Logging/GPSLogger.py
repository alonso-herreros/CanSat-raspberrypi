from .DataLogger import DataLogger


class GPSLogger(DataLogger):
    HEADERS = ['Time', 'Latitude', 'Longitude', 'Altitude']


    def __init__(self, file_name, headers=None):
        super().__init__(file_name, headers or GPSLogger.HEADERS)

    
    def log_sentence(self, sen):
        if sen.sentence_type == 'GGA' or sen.sentence_type == 'GLL':
            data = [sen.timestamp, sen.lat, sen.lon, getattr(sen, 'altitude', None)]
            self.log(data)
            return data
        else:
            return None