from cell_names import *
from datetime import datetime


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
        if column == DATE:
            value = self.to_date(value)
        if column == TIME:
            value = int(value)
        return value

    @staticmethod
    def to_date(s):
        return datetime.strptime(s, '%Y-%m-%d %H:%M:%S.%f')

    def get_filtered_rows(self, column, value):
        to_return = []
        for row in self.rows:
            if row[column] == value:
                to_return.append(row)
        return to_return

