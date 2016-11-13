from csv_reader import *
from cell_names import *
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from itertools import groupby
from data_helpers import to_log


def get_avg_per_municipality(csv_file):
    avgs = []
    grouped = grouped_by_municipality(csv_file.rows, TIME_TO_STATEMENT)
    for key, group in grouped:
        times = map(lambda x: x[1], group)
        avgs.append(reduce(lambda x, y: x + y, times) / len(times))
    return avgs


def grouped_by_municipality(rows, param):
    sorted_by_municipality = sorted(map(lambda x: (x[MUNICIPALITY], x[param]), rows), key=lambda entry: entry[0])
    return groupby(sorted_by_municipality, lambda x: x[0])


def grouped_by_month(rows, param):
    sorted_by_month = sorted(map(lambda x: (int(x[MONTH]), x[param]), rows), key=lambda entry: entry[0])
    return groupby(sorted_by_month, lambda x: x[0])


def get_municipalities(rows):
    return set(map((lambda x: x[MUNICIPALITY]), rows))


# csv_file = CSVFile([APPLICATION_ID, MUNICIPALITY, TIME_TO_VERDICT, FILLING_TIME], "resources/aws_file_puunkaatamine.csv")
# applicationId,municipality,timeToVerdict,filling-time,time-to-statement,operation
# csv_file = CSVFile([APPLICATION_ID, MUNICIPALITY, TIME_TO_VERDICT, FILLING_TIME, TIME_TO_STATEMENT, OPERATION], "resources/aws_file_maalampo.csv")
csv_file = CSVFile([APPLICATION_ID, MUNICIPALITY, TIME_TO_VERDICT, FILLING_TIME, OPERATION, MONTH], "resources/aws_file_maalampo.csv")
# csv_file = CSVFile([APPLICATION_ID, MUNICIPALITY, TIME_TO_VERDICT, FILLING_TIME, OPERATION], "resources/aws_file.csv")


def plot_avgs():
    avgs = get_avg_per_municipality(csv_file)
    municipalities = get_municipalities(csv_file.rows)
    x_axel = map(lambda x: x * 20, range(0, len(avgs)))
    plt.bar(x_axel, avgs, 10)
    plt.ylabel('Avg answering time')
    plt.xticks(x_axel, list(municipalities), rotation='vertical')
    plt.show()


def plot_box_plot_by_municipalities():
    rows = csv_file.get_filtered_rows(TIME_TO_VERDICT, lambda x: x != 0)
    grouped = grouped_by_municipality(rows, TIME_TO_VERDICT)
    x = []
    for key, group in grouped:
        x.append(map(lambda x: x[1], group))

    municipalities = get_municipalities(rows)
    plt.boxplot(x)
    plt.ylabel('Time to verdict')
    plt.xlabel('Municipalities')
    plt.xticks(range(1, len(municipalities) + 1), list(municipalities))
    plt.show()


def plot_box_plot_by_month():
    rows = csv_file.get_filtered_rows(TIME_TO_VERDICT, lambda x: x != 0)
    grouped = grouped_by_month(rows, TIME_TO_VERDICT)
    x = []
    for key, group in grouped:
        x.append(map(lambda x: x[1], group))

    months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    plt.boxplot(x)
    plt.ylabel('Time to verdict')
    plt.xlabel('Months')
    plt.xticks(range(1, 1 + len(months)), list(months))
    plt.show()


colors = [
    "b",
    "g",
    "r",
    "c",
    "m",
    "y",
    "k",
    "w"
]


def time_by_filling_time():
    municipalities = list(get_municipalities(csv_file.rows))
    mun_color_map = {}
    for m in municipalities:
        mun_color_map[m] = colors[municipalities.index(m)]

    for m in municipalities:
        rows = csv_file.get_filtered_rows(MUNICIPALITY, lambda x: x == m)
        filling_times = map(lambda row: (row[FILLING_TIME]), rows)
        times_to_verdict = map(lambda row: (row[TIME_TO_VERDICT]), rows)
        plt.plot(filling_times, times_to_verdict, str(mun_color_map[m]) + "o", ms=10)

    plt.legend(map(lambda x: mpatches.Patch(color=x), mun_color_map.values()), mun_color_map.keys(), bbox_to_anchor=(1.1, 0.55))

    plt.xlabel("Filling time (s)")
    plt.ylabel("Time to verdict (s)")
    plt.show()


plot_box_plot_by_month()
# plot_box_plot_by_municipalities()
# time_by_filling_time()
