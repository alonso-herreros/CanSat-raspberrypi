import csv
from pathlib import Path


class DataLogger:
    DEF_HEADERS = ['Data']

    def __init__(self, file, headers=DEF_HEADERS, overwrite=True):
        self._file = Path(file)
        self._headers = headers
        self._columns = len(headers)

        try:
            with open(self._file, 'w', newline='') as file:
                writer = csv.writer(file, delimiter=',')
                writer.writerow(headers)
        except IOError as e:
            print(f"IOError: {e}")


    @property
    def columns(self):
        return self._columns

    @property
    def file(self):
        return self._file

    @property
    def headers(self):
        return self._headers


    def log_data(self, data):
        try:
            with open(self._file, 'a', newline='') as file:
                writer = csv.writer(file, delimiter=',')
                writer.writerow(data)
            return data
        except IOError as e:
            print(f"IOError: {e}")
            return None