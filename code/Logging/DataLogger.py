import csv
from pathlib import Path


class DataLogger:
    DEF_HEADERS = ['Data']

    def __init__(self, file, headers=None):
        self._file = Path(file).resolve()
        self._headers = headers or DataLogger.DEF_HEADERS

        self._file.parent.mkdir(parents=True, exist_ok=True)
        self._file.touch()

        with self._file.open('w', newline='') as file:
            writer = csv.writer(file, delimiter=',')
            writer.writerow(self._headers)


    @property
    def columns(self):
        return len(self._headers)

    @property
    def file(self):
        return self._file

    @property
    def headers(self):
        return self._headers


    def log(self, *args):
        data = [args] if len(args) == 1 else args

        with open(self._file, 'a', newline='') as file:
            writer = csv.writer(file, delimiter=',')
            for entry in data:
                if len(entry) == len(self._headers): 
                    writer.writerow(entry)
                else:
                    raise ValueError('Data length does not match headers length')
        return data