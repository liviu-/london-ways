#!/usr/bin/env python
"""Proces csv file and store key-value pair of columns in redis"""

import csv
import json
import redis
import sys

REDIS_HOST = 'localhost'
CONN = redis.Redis(REDIS_HOST)

def get_csv_data(csv_file, **columns):
    """ Extract columns from CSV file

    Args:
        csv_file (str): Path to CSV file to process
        columns (iter of int): Columns that will be  returned

    """
    col1, col2 = columns['columns']
    with open(csv_file, encoding='utf-8') as csvf:
        csv_data = csv.reader(csvf)
        return [(i[col1], i[col2]) for i in csv_data]

def store_data(data):
    """ Stores data in the redis server

    Args:
        data (iter): data[0] will be used for key,
                     data[1] will be used for value
    """

    for i in data:
        if i[1] not in CONN:
            CONN.set(i[0], i[1])
    return data

def main():
    if len(sys.argv) < 2:
        sys.exit("usage: python {file} file.csv [column1, column2]"
                 .format(file=__file__))
    csv_file = sys.argv[1]
    columns = list(map(int, sys.argv[2:4])) or [1, 3]
    data = get_csv_data(csv_file, columns=columns)
    print(json.dumps(store_data(data)))

if __name__ == '__main__':
    main()
