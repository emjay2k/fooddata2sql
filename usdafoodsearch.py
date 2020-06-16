#!/usr/bin/python3

'''
Created on Jun 13, 2020

@author: matthias
'''

import argparse
import random
from sqliteconnection import SqliteConnection
from helper import Helper

sql_query_food_descr_by_fdcid = 'SELECT description FROM food where fdc_id = {0};'
sql_query_food_descr_search = 'SELECT fdc_id,description FROM food where description LIKE \'%{0}%\';'
sql_query_food_descr_search_exact = 'SELECT fdc_id,description FROM food where description = \'{0}\';'
sql_script_nutrition_list_for_fdcid = [ 'CREATE TEMPORARY TABLE table_{0} AS SELECT nutrient_id, amount FROM food_nutrient WHERE fdc_id = {1};', 'SELECT b.name, a.amount, b.unit_name FROM table_{0} AS a INNER JOIN nutrient AS b ON a.nutrient_id = b.id ORDER BY b.rank;', 'DROP TABLE IF EXISTS table_{0};' ]


def _get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-db', '--database', type=Helper.is_file, help='path to sqlite database', required=True)
    parser.add_argument('-e', '--exact', help='will search for the exact string', action='store_true')
    parser.add_argument('-i', '--id', help='lookup food for given id', action='store_true')
    parser.add_argument('-n', '--nutrients', help='lookup nutrients for given id', action='store_true')
    parser.add_argument('keyword', help='keyword or id')

    args = parser.parse_args()

    return args


def search_food_db(connection, args):
    if args.id:
        query = sql_query_food_descr_by_fdcid.format(args.keyword)

        rand_id = random.randint(0, 65535)
        script = []
        for l in sql_script_nutrition_list_for_fdcid:
            script.append(l.format(rand_id, args.keyword))
        result_index = 1
    elif args.exact:
        query = sql_query_food_descr_search_exact.format(args.keyword)
    else:
        query = sql_query_food_descr_search.format(args.keyword)

    rows = connection.query(query)

    for r in rows:
        print(r)

    if args.nutrients:
        print('====================')
        rows = connection.queries(script, result_index)
        for r in rows:
            print(r)


def main():
    args = _get_args()

    connection = SqliteConnection(args.database)
    search_food_db(connection, args)


if __name__ == '__main__':
    main()
