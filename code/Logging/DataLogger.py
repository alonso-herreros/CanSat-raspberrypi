import csv


class DataLogger:
    def __init__(self, file_name, headers=[]):
        self._file_name = file_name
        self._columns = len(headers)
        
        try:
            with open(self._file_name, 'w', newline='') as file:
                writer = csv.writer(file, delimiter=',')
                writer.writerow(headers)
        except IOError as e:
            print(f"IOError: {e}")


    @property
    def columns(self):
        return self._columns

    @property
    def file_name(self):
        return self._file_name

    @property
    def headers(self):
        try:
            with open(self._file_name, 'r') as file:
                reader = csv.reader(file, delimiter=',')
                headers = next(reader)
            return headers
        except IOError as e:
            print(f"IOError: {e}")
            return None


    def log_data(self, data):
        try:
            with open(self._file_name, 'a', newline='') as file:
                writer = csv.writer(file, delimiter=',')
                writer.writerow(data)
            return data
        except IOError as e:
            print(f"IOError: {e}")
            return None