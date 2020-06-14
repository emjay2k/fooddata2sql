#!/usr/bin/python3

'''
Created on Jun 13, 2020

@author: matthias
'''

import argparse
from sqliteconnection import SqliteConnection
from helper import Helper

db_file = 'sqlite_output/usda_foundation_foods.sqlite'


def _get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-db', '--database', type=Helper.is_file, help='path to sqlite database', required=True)
    parser.add_argument('-e', '--exact', help='will search for the exact string', action="store_true")
    parser.add_argument('-i', '--id', help='lookup food for given id', action="store_true")
    parser.add_argument('keyword', help='keyword or id')

    args = parser.parse_args()

    return args


def search_food_db(connection, args):
    if args.id:
        query = 'SELECT description FROM food where fdc_id = ' + args.keyword + ';'
    elif args.exact:
        query = 'SELECT fdc_id,description FROM food where description = ' + '\'' + args.keyword + '\';'
    else:
        query = 'SELECT fdc_id,description FROM food where description LIKE ' + '\'%' + args.keyword + '%\';'

    rows = connection.query(query)

    for r in rows:
        print(r)


def main():
    args = _get_args()

    connection = SqliteConnection(args.database)
    search_food_db(connection, args)


if __name__ == '__main__':
    main()
