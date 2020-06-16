'''
Created on Jun 13, 2020

@author: Matthias Jung
'''

import csv
from sqlhelper import SqlHelper, DbType
from abc import ABC, abstractmethod


class SqlImporter(ABC):
    '''
    Abstract class for sql import. This contains the generic workflow. You have to override at least open_db()
    '''

    def __init__(self):
        self.count = [ 0, 0, 0 ]
        self.connection = None

    @abstractmethod
    def _open_db(self):
        pass

    def import_file(self, file, indices):
        if self._open_db():
            result = self._create_table(file, indices)
            SqlImporter._print_import_result(result, file)

            self.count[0] += result[0]
            self.count[1] += result[1]
            self.count[2] += result[2]

            self.connection.close()

    def print_total_result(self):
        print('import summary')
        print('added:')
        print('- tables        : {0}'.format(self.count[0]))
        print('- primary keys  : {0}'.format(self.count[2]))
        print('- data rows     : {0}'.format(self.count[1]))

    def _set_primarykey(self, table_name, primary_key, col_list=[], type_list=[]):
        sql_stm = 'ALTER TABLE {0} ADD PRIMARY KEY ({1});'.format(table_name, primary_key)

        return SqlHelper.execute_statement(self.connection, sql_stm)

    def _set_index(self, table_name, index, col_list=[], type_list=[]):
        sql_stm = 'CREATE INDEX {0}_{1}_idx ON {0}({1});'.format(table_name, col_list[index])

        return SqlHelper.execute_statement(self.connection, sql_stm)

    def _import_data_to_table(self, file, table_name, name_list, type_list):
        result = 0

        # read file
        with open(file, newline='') as csvfile:

            csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')

            firstLine = True
            for row in csvreader:
                # first row denotes table head
                if firstLine:
                    firstLine = False

                elif len(row) == len(name_list):
                    values = []
                    for i in range(len(row)):
                        v = SqlHelper.type_to_dbstatement(row[i], type_list[i])
                        values.append(v)

                    insert_query = SqlHelper.sql_insert_query(table_name, values)
                    success = SqlHelper.execute_statement(self.connection, insert_query)
                    result += int(success == True)

                else:
                    print('ignoring unexpected row: {0}'.format(row))

        return result

    def _create_table(self, file, indices):
        table_name = SqlHelper.get_tablename(file)

        result_create = 0
        result_data = 0
        result_key = 0

        # create table in database
        name_list, type_list = SqlImporter._extract_name_and_types(file)

        if len(name_list) > 0:
            create_query = SqlHelper.sql_create_table(table_name, name_list, type_list)
            create_success = SqlHelper.execute_statement(self.connection, create_query)
            self.connection.commit()

        if create_success:
            result_create = 1

            # import data into table
            result_data = self._import_data_to_table(file, table_name, name_list, type_list)
            self.connection.commit()

            # attempt to set primary key in first integer-type column
            primary_key = -1
            for i in range(len(type_list)):
                t = type_list[i]
                if t == DbType.INTEGER:
                    success = self._set_primarykey(table_name, i, name_list, type_list)
                    self.connection.commit()
                    if success:
                        result_key = 1
                        primary_key = i
                    break

            # set indices on _id named columns if specified
            if indices:
                for i in range(len(type_list)):
                    t = type_list[i]
                    if i != primary_key and t == DbType.INTEGER and (name_list[i] == 'id' or '_id_' in name_list[i] or name_list[i].endswith('_id')):
                        self._set_index(table_name, i, name_list, type_list)

        return result_create, result_data, result_key

    @staticmethod
    def _extract_name_and_types(file):
        name_list = []
        type_list = []

        # read file
        with open(file, newline='') as csvfile:

            csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')

            firstLine = True
            for row in csvreader:
                # first row denotes table head
                if firstLine:
                    firstLine = False

                    for i in range(len(row)):
                        name = SqlHelper.sanitize_colname(row[i])
                        name_list.append(name)
                        type_list.append(DbType.NULL)

                elif len(row) == len(name_list):
                    for i in range(len(row)):
                        type_class = SqlHelper.classify_dbtype(row[i])
                        type_list[i] = DbType.order_max(type_list[i], type_class)

        return name_list, type_list

    @staticmethod
    def _print_import_result(status, file):
        print('table: ' + SqlHelper.get_tablename(file))
        if status[0] > 0:
            print('- created')
        if status[1] > 0:
            print('- filled')
        if status[2] > 0:
            print('- primary key detected')
        print('---')
