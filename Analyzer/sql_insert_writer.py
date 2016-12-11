from cell_names import *
from cell_names import SENT_DATE, LAT, LON, IS_CANCELLED, CANCELED_DATE
from csv_reader import CSVFile

SCHEMA = [DATE_TIME, APPLICATION_ID, USER_ID, ROLE, ACTION, TARGET, MUNICIPALITY_ID, STATE, OPERATION,
          SUBMITTED_DATE, SENT_DATE, VERDICT_GIVEN, CANCELED_DATE, IS_CANCELLED, LON, LAT]


def main():
    # log_data = "/Users/liisasa/Documents/LupapisteData/lupapiste-usage-20160914.csv"
    log_data_file = "/Users/liisasa/Documents/LupapisteData/short.csv"
    log_data = CSVFile([DATE_TIME, APPLICATION_ID, MUNICIPALITY_ID, USER_ID, ROLE, ACTION, TARGET], log_data_file, ";")

    operational_data_file = "/Users/liisasa/Dippa/applications-operative-on-20160914-20160918.csv"
    operational_data_columns = [APPLICATION_ID, MUNICIPALITY_ID, PERMIT_TYPE, STATE, OPERATION,
               "operationId2", "operationId3", "operations", CREATED_DATE, SUBMITTED_DATE, SENT_DATE,
               VERDICT_GIVEN, CANCELED_DATE, IS_CANCELLED, LON, LAT]
    operational_data = CSVFile(operational_data_columns, operational_data_file, ";")

    enriched_log_data = join(log_data, operational_data)
    sql = to_insert_sql_clause(enriched_log_data)
    with open('resources/insert_log_data.sql', 'w') as insert_sql:
        insert_sql.write(sql)


def join(log_data, operational_data):
    operational_data_map = dict(map(lambda r: (r[APPLICATION_ID], r), operational_data.rows))
    enriched_log_data = []
    for row in log_data.rows:
        if row[APPLICATION_ID] not in operational_data_map:
            continue
        enriched_log_data.append(merge_two_dicts(operational_data_map[row[APPLICATION_ID]], row))
    return enriched_log_data


def merge_two_dicts(x, y):
    z = x.copy()
    z.update(y)
    return z


def to_insert_sql_clause(enriched_log_data):
    sql = ("INSERT INTO log_data (" + ",".join(["{}"] * len(SCHEMA)) + ") VALUES").format(*SCHEMA)
    rows = []
    row_template = "(" + ",".join(["{}"] * len(SCHEMA)) + ")"
    for row in enriched_log_data:
        values = map(lambda column: to_value(row, column), SCHEMA)
        rows.append(row_template.format(*values))
    sql += ",".join(rows)
    sql += ";"
    return sql


def to_value(row, column):
    value = str(row[column])
    return "'" + value + "'" if value != "" else "NULL"


if __name__ == "__main__":
    main()
