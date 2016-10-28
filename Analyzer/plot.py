import matplotlib.pyplot as plt
from itertools import groupby

MUNICIPALITY = "municipality_id"
TIME = "time"
FILLING_TIME = "filling-time"

COLUMNS = [MUNICIPALITY, TIME, FILLING_TIME]


def to_cells(line):
    chunks = line.split(",")
    return {MUNICIPALITY: chunks[COLUMNS.index(MUNICIPALITY)],
            TIME: int(chunks[COLUMNS.index(TIME)])}


def to_log_entries(data):
    header = True
    data_entries = []
    for line in data:
        if header:
            header = False
            continue
        data_entries.append(to_cells(line))
    return data_entries


def get_avgs_per_municipality(sorted_by_municipality):
    avgs = []
    grouped = groupby(sorted_by_municipality, lambda x: x[0])
    for key, group in grouped:
        times = map(lambda x: x[1], group)
        avgs.append(reduce(lambda x, y: x + y, times) / len(times))
    return avgs


log_entries = to_log_entries(open("aws_file.csv", 'r'))
municipalities = set(map((lambda x: x[MUNICIPALITY]), log_entries))
sorted_by_municipality = sorted(map(lambda x: (x[MUNICIPALITY], x[TIME]), log_entries), key=lambda entry: entry[0])
avgs = get_avgs_per_municipality(sorted_by_municipality)

xax = map(lambda x: x * 20, range(0, len(avgs)))
plt.bar(xax, avgs, 10)
plt.ylabel('some numbers')
plt.xticks(xax, list(municipalities), rotation='vertical')
plt.show()
