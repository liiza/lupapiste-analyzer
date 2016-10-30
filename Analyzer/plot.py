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

plot_box_plot()
