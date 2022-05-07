from Interfacing.CTReader import CTReader
from pathlib import Path


dir = Path() / 'logs' / 'sat_file'


if __name__ == '__main__':
    with CTReader(open('D:/tmp/main_.txt'), dir, append=False) as reader:
        while True:
            line = reader.readline(True)

            if line: print(line)
