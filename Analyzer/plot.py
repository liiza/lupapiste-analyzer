from csv_reader import *
from cell_names import *
import matplotlib.pyplot as plt
from itertools import groupby


def get_avg_per_municipality(csv_file):
    avgs = []
    grouped = times_grouped_by_municipality(csv_file)
    for key, group in grouped:
        times = map(lambda x: x[1], group)
        avgs.append(reduce(lambda x, y: x + y, times) / len(times))
    return avgs


def times_grouped_by_municipality(csv_file):
    sorted_by_municipality = sorted(map(lambda x: (x[MUNICIPALITY], x[TIME]), csv_file.rows), key=lambda entry: entry[0])
    return groupby(sorted_by_municipality, lambda x: x[0])


def get_municipalities(csv_file):
    return set(map((lambda x: x[MUNICIPALITY]), csv_file.rows))


csv_file = CSVFile([APPLICATION_ID, MUNICIPALITY, TIME, FILLING_TIME], "resources/aws_file.csv")


def plot_avgs():
    avgs = get_avg_per_municipality(csv_file)
    municipalities = get_municipalities(csv_file)
    x_axel = map(lambda x: x * 20, range(0, len(avgs)))
    plt.bar(x_axel, avgs, 10)
    plt.ylabel('Avg answering time')
    plt.xticks(x_axel, list(municipalities), rotation='vertical')
    plt.show()


def plot_box_plot():
    grouped_by_municipality = times_grouped_by_municipality(csv_file)
    x = []
    for key, group in grouped_by_municipality:
        x.append(map(lambda x: x[1], group))

    municipalities = get_municipalities(csv_file)
    plt.boxplot(x)
    plt.ylabel('Time to first statement by authorities')
    plt.xticks(range(1, len(municipalities) + 1), list(municipalities))
    plt.show()


colors = [
    'b',
    'g',
    'r',
    'c',
    'm',
    'y',
    'k',
    'w'
]


def time_by_filling_time():
    municipalities = list(get_municipalities(csv_file))
    mun_color_map = {}
    for m in municipalities:
        mun_color_map[m] = colors[municipalities.index(m)]

    for m in get_municipalities(csv_file):
        rows = csv_file.get_filtered_rows(MUNICIPALITY, m)
        times = map(lambda row: row[TIME], rows)
        filling_times = map(lambda row: row[FILLING_TIME], rows)
        symbol = str(mun_color_map[m]) + "o"
        plt.plot(filling_times, times, symbol)

    plt.ylabel("Times from submit to first statement")
    plt.xlabel("Filling times")
    plt.show()


# plot_box_plot()
time_by_filling_time()
