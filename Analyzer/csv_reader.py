from datetime import datetime

from cell_names import *


class CSVFile:
    def __init__(self, columns, data_file, delimiter=","):
        self.columns = columns
        self.delimiter = delimiter
        self.rows = self.to_rows(data_file)

    def to_rows(self, data_file):
        with open(data_file, 'r') as data:
            header = True
            data_entries = []
            for line in data:
                if header:
                    header = False
                    continue
                data_entries.append(self.to_cells(line))
        return data_entries

    def to_cells(self, line):
        chunks = line.split(self.delimiter)
        cells = {}
        for column in self.columns:
            cells[column] = self.get_column_value(chunks, column)
        return cells

    def get_column_value(self, chunks, column):
        value = chunks[self.columns.index(column)]
        if is_date(column):
            value = self.to_date(value)
        if column == TIME_TO_STATEMENT or column == TIME_TO_VERDICT:
            value = float(value)
        return value

    @staticmethod
    def to_date(s):
        if len(s.strip()) == 0:
            return None
        try:
            date = datetime.strptime(s, '%Y-%m-%d %H:%M:%S.%f')
        except ValueError:
            date = datetime.strptime(s, '%Y-%m-%d %H:%M:%S')

        return date

    def get_filtered_rows(self, column, f):
        to_return = []
        for row in self.rows:
            if f(row[column]):
                to_return.append(row)
        return to_return
