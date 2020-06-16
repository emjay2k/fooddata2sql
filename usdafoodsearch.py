#!/usr/bin/python3

'''
Created on Jun 13, 2020

@author: matthias

Some example queries for demonstration purposes
'''

import argparse
from sqliteconnection import SqliteConnection
from helper import Helper
from sqlhelper import SqlHelper
from samba.samba3.libsmb_samba_internal import Conn

sql_query_food_descr_by_fdcid = 'SELECT description FROM food where fdc_id = {0};'
sql_query_food_descr_search = 'SELECT fdc_id,description FROM food where description LIKE \'%{0}%\';'
sql_query_food_descr_search_exact = 'SELECT fdc_id,description FROM food where description = \'{0}\';'
sql_script_nutrition_list_for_fdcid = [ 'CREATE TEMPORARY TABLE table_{0} AS SELECT nutrient_id, amount FROM food_nutrient WHERE fdc_id = {1};', 'SELECT b.name, a.amount, b.unit_name FROM table_{0} AS a INNER JOIN nutrient AS b ON a.nutrient_id = b.id ORDER BY b.rank;', 'DROP TABLE IF EXISTS table_{0};' ]


class NutrientElement:

    def __init__(self, name, amount, unit):
        self.name = name
        self.amount = amount
        self.unit = unit

    def __str__(self):
        return '{0},{1},{2}'.format(self.name, self.amount, self.unit.lower())


def _get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-db', '--database', type=Helper.is_file, help='path to sqlite database', required=True)
    parser.add_argument('-e', '--exact', help='will search for the exact string', action='store_true')
    parser.add_argument('-i', '--id', help='lookup food for given id', action='store_true')
    parser.add_argument('-n', '--nutrients', help='lookup nutrients for given id', action='store_true')
    parser.add_argument('keyword', help='keyword or id')

    args = parser.parse_args()

    return args


def _get_nutrient_list(list_list):
    result = []
    for n in list_list:
        result.append(NutrientElement(n[0], n[1], n[2]))

    return result


def _search_food_by_id(connection, id):
    query = sql_query_food_descr_by_fdcid.format(id)

    return Helper._get_first_element(connection.query(query))


def _search_food_by_name_like(connection, name):
    query = sql_query_food_descr_search.format(name)

    return Helper._get_pair_list(connection.query(query))


def _search_food_by_name(connection, name):
    query = sql_query_food_descr_search_exact.format(name)

    return Helper._get_first_element(connection.query(query))


def _search_nutrients_by_fdcid(connection, fdc_id):
    script = []
    rand_id = SqlHelper._get_rand_tableno()
    for l in sql_script_nutrition_list_for_fdcid:
        script.append(l.format(rand_id, fdc_id))
    result_index = 1

    return _get_nutrient_list(connection.queries(script, result_index))


def _search_food_sql(connection, args):
    if args.id:
        print(_search_food_by_id(connection, args.keyword))
    elif args.exact:
        print(_search_food_by_name(connection, args.keyword))
    else:
        Helper.print_list(_search_food_by_name_like(connection, args.keyword))

    if args.nutrients:
        print('====================')
        Helper.print_list(_search_nutrients_by_fdcid(connection, args.keyword))


def main():
    args = _get_args()

    connection = SqliteConnection(args.database)
    if connection:
        _search_food_sql(connection, args)


if __name__ == '__main__':
    main()
