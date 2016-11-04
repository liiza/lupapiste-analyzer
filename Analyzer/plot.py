from csv_reader import *
from cell_names import *
import matplotlib.pyplot as plt
from itertools import groupby


def get_avg_per_municipality(csv_file):
    avgs = []
    grouped = grouped_by_municipality(csv_file.rows, TIME)
    for key, group in grouped:
        times = map(lambda x: x[1], group)
        avgs.append(reduce(lambda x, y: x + y, times) / len(times))
    return avgs


def grouped_by_municipality(rows, param):
    sorted_by_municipality = sorted(map(lambda x: (x[MUNICIPALITY], x[param]), rows), key=lambda entry: entry[0])
    return groupby(sorted_by_municipality, lambda x: x[0])


def get_municipalities(rows):
    return set(map((lambda x: x[MUNICIPALITY]), rows))


csv_file = CSVFile([APPLICATION_ID, MUNICIPALITY, TIME, TIME_TO_VERDICT, FILLING_TIME], "resources/aws_file_verdict_times.csv")


def plot_avgs():
    avgs = get_avg_per_municipality(csv_file)
    municipalities = get_municipalities(csv_file.rows)
    x_axel = map(lambda x: x * 20, range(0, len(avgs)))
    plt.bar(x_axel, avgs, 10)
    plt.ylabel('Avg answering time')
    plt.xticks(x_axel, list(municipalities), rotation='vertical')
    plt.show()


def plot_box_plot():
    rows = csv_file.get_filtered_rows(TIME_TO_VERDICT, 0)
    grouped = grouped_by_municipality(rows, TIME_TO_VERDICT)
    x = []
    for key, group in grouped:
        x.append(map(lambda x: x[1], group))

    municipalities = get_municipalities(rows)
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
    municipalities = list(get_municipalities(csv_file.rows))
    mun_color_map = {}
    for m in municipalities:
        mun_color_map[m] = colors[municipalities.index(m)]

    for m in municipalities:
        rows = csv_file.get_filtered_rows(MUNICIPALITY, m)
        times = map(lambda row: row[TIME], rows)
        filling_times = map(lambda row: row[TIME_TO_VERDICT], rows)
        symbol = str(mun_color_map[m]) + "o"
        plt.plot(times, filling_times, symbol)

    plt.ylabel("Times from submit to first statement")
    plt.xlabel("Times to verdict")
    plt.show()


plot_box_plot()
# time_by_filling_time()
