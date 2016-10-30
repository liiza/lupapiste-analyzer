from csv_reader import *
from cell_names import *
import matplotlib.pyplot as plt
from itertools import groupby

COLUMNS = [MUNICIPALITY, TIME, FILLING_TIME]


def get_avg_per_municipality(csvFile):
    avgs = []
    sorted_by_municipality = sorted(map(lambda x: (x[MUNICIPALITY], x[TIME]), csvFile.rows), key=lambda entry: entry[0])
    grouped = groupby(sorted_by_municipality, lambda x: x[0])
    for key, group in grouped:
        times = map(lambda x: x[1], group)
        avgs.append(reduce(lambda x, y: x + y, times) / len(times))
    return avgs


def get_municipalities(csvFile):
    return set(map((lambda x: x[MUNICIPALITY]), csvFile.rows))


csvFile = CSVFile(COLUMNS, open("aws_file.csv", 'r'))
avgs = get_avg_per_municipality(csvFile)
municipalities = get_municipalities(csvFile)

xax = map(lambda x: x * 20, range(0, len(avgs)))
plt.bar(xax, avgs, 10)
plt.ylabel('Avg answering time')
plt.xticks(xax, list(municipalities), rotation='vertical')
plt.show()
