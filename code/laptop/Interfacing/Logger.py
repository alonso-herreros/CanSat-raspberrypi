from pathlib import Path
from datetime import datetime
import csv


class Logger:
    DEF_FIELDS = ['Data']

    def __init__(self, file, fields=[], filter=None):
        self._file = Path(file).resolve()
        self.filter = filter or (lambda x: x)

        fields = fields or Logger.DEF_FIELDS
        self._fields = fields if hasattr(fields, 'values') else {i.lower().replace(' ', '_'): i for i in fields}

        self._file.parent.mkdir(parents=True, exist_ok=True)
        self._file.touch()
        with self._file.open('w', newline='') as file:
            writer = csv.writer(file, delimiter=',')
            writer.writerow(self.headers)


    @property
    def headers(self):
        return [*self._fields.values()]
    @property
    def fields(self):
        return [*self._fields]

    @property
    def file(self):
        return self._file


    #TODO: Implement alternative by getting data as kwargs with column aliases
    def log(self, *entries):
        logged = []

        with open(self._file, 'a', newline='') as file:
            writer = csv.writer(file, delimiter=',') #Initialize a csv writer

            #There may be more than one entry to log at once, passed as a multiple args
            for entry in entries:
                entry = self.filter(entry)
                if not entry: # Don't log if the entry doesn't pass the filter
                    continue 

                # Most common case, entry is just a list
                if isinstance(entry, (list, tuple)):
                    row = entry
                # If it's a dict, use the field names if possible or use the given order
                elif hasattr(entry, 'keys'):
                    row = [entry.get(k) for k in self.fields] or entry.values()
                # If it's an nmea sentence, use the field names if possible or log nothing
                elif hasattr(entry, 'sentence_type'):
                    row = [getattr(entry, k, None) for k in self.fields]
                # If it's a string, just log that
                elif hasattr(entry, 'lower'):
                    row = [entry]
                # If it's not recognized we're going to try to log it anyway
                else:
                    row = entry

                if (i for i in row if i): # Check if there is valid data in the list
                    # If there is $time in fields and there is no data in row for it, add the current time
                    if "$time" in self.fields and not row[self.fields.index("$time")]:
                        row[self.fields.index("$time")] = str(datetime.now())

                    if len(row) != len(self.fields):
                        raise ValueError('Data length does not match column count')

                    writer.writerow(row)
                    logged.append(row)

        return logged[0] if len(logged) == 1 else logged