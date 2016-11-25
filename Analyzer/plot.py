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


def grouped_by(rows, target, param):
    sorted_by = sorted(map(lambda x: (x[target], x[param]), rows), key=lambda entry: entry[0])
    return groupby(sorted_by, lambda x: x[0])


def grouped_by_municipality(rows, param):
    return grouped_by(rows, MUNICIPALITY, param)


def grouped_by_month(rows, param):
    sorted_by = sorted(map(lambda x: (x[MONTH], x[param]), rows), key=lambda entry: int(entry[0]))
    return groupby(sorted_by, lambda x: x[0])


def grouped_by_operation(rows, param):
    return grouped_by(rows, OPERATION, param)


def get_municipalities(rows):
    return set(map((lambda x: x[MUNICIPALITY]), rows))


# applicationId,municipality,running-month,operation,time-to-verdict
csv_file = CSVFile([APPLICATION_ID, MUNICIPALITY, RUNNING_MONTH, OPERATION, TIME_TO_VERDICT], "resources/aws_file.csv")


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
    y = []
    for key, group in grouped:
        x.append(map(lambda x: x[1], group))
        y.append(key)

    plt.boxplot(x)
    plt.ylabel('Time to verdict (s)')
    plt.xlabel('Municipalities')
    plt.xticks(range(1, len(y) + 1), list(y))
    plt.show()


def plot_box_plot_by_month():
    rows = csv_file.get_filtered_rows(TIME_TO_VERDICT, lambda x: x != 0)
    grouped = grouped_by_month(rows, TIME_TO_VERDICT)
    x = []
    y = []
    for key, group in grouped:
        x.append(map(lambda x: to_log(x[1]), group))
        y.append(key)

    plt.boxplot(x)
    plt.ylabel('Time to verdict')
    plt.xlabel('Months')
    plt.xticks(range(1, 1 + len(y)), y)
    plt.show()


def sum_by_month():
    rows = csv_file.get_filtered_rows(TIME_TO_VERDICT, lambda x: x != 0)
    grouped = grouped_by_month(rows, TIME_TO_VERDICT)
    x = []
    y = []
    for key, group in grouped:
        x.append(len(map(lambda x: x, group)))
        y.append(key)

    w = 0.7
    plt.bar(range(len(x)), x, width=w)
    plt.ylabel('Applications')
    plt.xlabel('Months')
    plt.xticks(map(lambda x: x + w / 2, range(len(y))), y)
    plt.show()


def plot_box_plot_by_operation():
    rows = csv_file.get_filtered_rows(TIME_TO_VERDICT, lambda x: x != 0)
    grouped = grouped_by_operation(rows, TIME_TO_VERDICT)
    x = []
    y = []
    for key, group in grouped:
        x.append(map(lambda t: t[1], group))
        y.append(key)

    plt.boxplot(x)
    plt.ylabel('Time to verdict')
    plt.xlabel('Operation')
    plt.xticks(range(1, len(y) + 1), y)
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

    for index, m in enumerate(municipalities):
        rows = csv_file.get_filtered_rows(MUNICIPALITY, lambda x: x == m)
        filling_times = map(lambda row: to_log(row[FILLING_TIME]), rows)
        times_to_verdict = map(lambda row: to_log(row[TIME_TO_VERDICT]), rows)
        plt.subplot(len(municipalities), 1, index)
        plt.plot(filling_times, times_to_verdict, str(mun_color_map[m]) + "o", ms=5)
        plt.axis([4, 18, 12, 17])

    plt.legend(map(lambda x: mpatches.Patch(color=x), mun_color_map.values()), mun_color_map.keys(), bbox_to_anchor=(1.1, 0.55))
    # plt.legend(map(lambda x: mpatches.Patch(color=x), mun_color_map.values()), mun_color_map.keys(), bbox_to_anchor=(1.5, 0.95))
    # plt.xlabel("Filling Time)
    # plt.ylabel("Time to verdict ")
    plt.show()


def process_time_by_actions():
    municipalities = list(get_municipalities(csv_file.rows))
    mun_color_map = {}
    for m in municipalities:
        mun_color_map[m] = colors[municipalities.index(m)]

    for m in municipalities:
        rows = csv_file.get_filtered_rows(MUNICIPALITY, lambda x: x == m)
        actions = map(lambda row: (row[ACTION_COUNT]), rows)
        times_to_verdict = map(lambda row: (row[TIME_TO_VERDICT]), rows)
        plt.plot(actions, times_to_verdict, str(mun_color_map[m]) + "o", ms=10)

    plt.legend(map(lambda x: mpatches.Patch(color=x), mun_color_map.values()), mun_color_map.keys(), bbox_to_anchor=(1.1, 0.55))

    plt.xlabel("Action count")
    plt.ylabel("Time to verdict ")
    plt.show()


def process_time_by_attachment_count():
    municipalities = list(get_municipalities(csv_file.rows))
    mun_color_map = {}
    for m in municipalities:
        mun_color_map[m] = colors[municipalities.index(m)]

    for m in municipalities:
        rows = csv_file.get_filtered_rows(MUNICIPALITY, lambda x: x == m)
        actions = map(lambda row: (row[ATTACHMENT_COUNT]), rows)
        times_to_verdict = map(lambda row: (row[TIME_TO_VERDICT]), rows)
        plt.plot(actions, times_to_verdict, str(mun_color_map[m]) + "o", ms=10)

    plt.legend(map(lambda x: mpatches.Patch(color=x), mun_color_map.values()), mun_color_map.keys(), bbox_to_anchor=(1.1, 0.55))

    plt.xlabel("Attachment count")
    plt.ylabel("Time to verdict ")
    plt.show()


def process_time_by_running_month():
    mun_color_map, municipalities = get_municipality_color_map()

    for index, m in enumerate(municipalities):
        rows = csv_file.get_filtered_rows(MUNICIPALITY, lambda x: x == m)
        running_months = map(lambda row: (row[RUNNING_MONTH]), rows)
        process_times = map(lambda row: (row[TIME_TO_VERDICT]), rows)

        months, applications_per_month = applications_grouped_by_running_month(rows)

        plt.subplot(3, 2, 1 + index)
        plt.plot(running_months, process_times, str(mun_color_map[m]) + "o", months, map(lambda x: x * pow(10, 6), applications_per_month), 'r')

    # plt.legend(map(lambda x: mpatches.Patch(color=x), mun_color_map.values()), mun_color_map.keys(), bbox_to_anchor=(1.1, 0.55))

    plt.xlabel("Running month")
    plt.ylabel("Time to verdict")
    plt.show()


def applications_grouped_by_running_month(file_rows):
    applications_per_running_month = []
    months = []
    grouped = grouped_by(file_rows, RUNNING_MONTH, TIME_TO_VERDICT)
    for key, group in grouped:
        verdict_times_per_month = map(lambda t: t[1], group)
        applications_per_running_month.append(len(verdict_times_per_month))
        months.append(key)
    return months, applications_per_running_month


def get_municipality_color_map():
    municipalities = list(get_municipalities(csv_file.rows))
    mun_color_map = {}
    for m in municipalities:
        mun_color_map[m] = colors[municipalities.index(m)]
    return mun_color_map, municipalities


def histogram_of_applications_per_municipality():
    rows = csv_file.get_filtered_rows(TIME_TO_VERDICT, lambda x: x != 0)
    grouped = grouped_by_municipality(rows, TIME_TO_VERDICT)
    applications_per_municipality = []
    for key, group in grouped:
        applications_per_municipality.append(sum(1 for e in group))
    plt.hist(applications_per_municipality, bins=30, color="green")
    plt.xlabel("Applications")
    plt.ylabel("Municipalities")
    plt.title("Applications per municipality")
    plt.show()


# plot_box_plot_by_month()
# plot_box_plot_by_municipalities()
# plot_box_plot_by_operation()
# time_by_filling_time()
# time_by_filling_time(True)
# histogram_of_applications_per_municipality()
# process_time_by_actions()
# sum_by_month()
# process_time_by_attachment_count()
process_time_by_running_month()
