#!/usr/bin/python3
'''
Created on Jun 13, 2020

@author: Matthias Jung
'''

from os import listdir
from os.path import isfile, join
import argparse
from helper import Helper
from sqliteimporter import SqliteImporter
# if you want to use mysql or pgsql
#from mysqlimporter import MysqlImporter
#from pgsqlimporter import PgsqlImporter


def _get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', type=Helper.is_readable_dir, help='path to csv input folder', required=True)
    # if you want to use mysql or pgsql an output file should not be required
    parser.add_argument('-o', '--output', type=Helper.not_is_file, help='path to sqlite output file', required=True)

    args = parser.parse_args()

    return args


def main():
    args = _get_args()

    importer = SqliteImporter(args.output)
    # if you want to use mysql or pgsql
    #importer = MysqlImporter(user='', password='', host='', port='', database='')
    #importer = PgsqlImporter(user='', password='', host='', port='', database='')

    for file in listdir(args.input):
        if isfile(join(args.input, file)) and file.endswith('.csv'):
            importer.import_file(args.input + '/' + file)

    importer.print_total_result()


if __name__ == '__main__':
    main()
