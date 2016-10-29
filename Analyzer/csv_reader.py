from cell_names import *
from datetime import datetime


class CSVReader:
    def __init__(self, columns):
        self.columns = columns

    @staticmethod
    def to_date(s):
        return datetime.strptime(s, '%Y-%m-%d %H:%M:%S.%f')

    def to_cells(self, line):
        chunks = line.split(";")
        cells = {}
        for column in self.columns:
            cells[column] = self.get_column_value(chunks, column)
        return cells

    def get_column_value(self, chunks, column):
        value = chunks[self.columns.index(column)]
        if column == DATE:
            value = self.to_date(value)
        return value

    def to_log_entries(self, data):
        header = True
        data_entries = []
        for line in data:
            if header:
                header = False
                continue
            data_entries.append(self.to_cells(line))
        return data_entries
