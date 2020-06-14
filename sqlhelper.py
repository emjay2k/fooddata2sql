'''
Created on Jun 13, 2020

@author: Matthias Jung
'''

from enum import Enum
from contextlib import closing
from os.path import basename
from sqlite3 import Error
from helper import Helper


class DbType(Enum):
    '''
    Database type enum
    '''
    
    NULL = 0
    BOOLEAN = 1
    INTEGER = 2
    FLOAT = 3
    DATE = 4
    TEXT = 5

    @staticmethod
    def order_max(n, m):
        if n.value > m.value:
            return DbType.TEXT if n == DbType.DATE and m != DbType.NULL else n
        elif n.value == m.value:
            return n
        else:
            return DbType.TEXT if m == DbType.DATE and n != DbType.NULL else m


class SqlHelper(object):
    '''
    SQL-related static helper methods and data structures
    '''

    db_sanitize_map = { ' ': '_', 'table': 'table_name' }

    @staticmethod
    def classify_dbtype(n):
        if len(n) == 0:
            return DbType.NULL
        if Helper.is_boolean(n):
            return DbType.BOOLEAN
        if Helper.is_integer(n):
            return DbType.INTEGER
        elif Helper.is_float(n):
            return DbType.FLOAT
        elif Helper.is_date(n, '%Y-%m-%d'):
            return DbType.DATE
        else:
            return DbType.TEXT

    @staticmethod
    def type_to_dbstatement(n, n_type):
        if n_type == DbType.NULL:
            return 'NULL'
        elif n_type == DbType.BOOLEAN:
            nl = n.lower()
            return str(int(nl == 'y' or nl == '1' or nl == 'true'))
        elif n_type == DbType.INTEGER or n_type == DbType.FLOAT:
            return '0' if len(n) == 0 else n
        else:  # text or date
            return 'NULL' if len(n) == 0 else '\'' + n.replace('\'', '') + '\''

    @staticmethod
    def get_tablename(file):
        return basename(file).split(".")[0]

    @staticmethod
    def sanitize_colname(colname):
        sanitized_value = colname
        for key, val in SqlHelper.db_sanitize_map.items():
            sanitized_value = sanitized_value.lower().replace(key, val)

        return sanitized_value

    @staticmethod
    def execute_statement(connection, statement):
        try:
            with closing(connection.cursor()) as cursor:
                cursor.execute(statement)

                return True
        except Error as e:
            Helper.print_error('SQL error: ' + str(e))
            Helper.print_error('Statement was: ' + statement)
        except:
            Helper.print_error('SQL error')
            Helper.print_error('Statement was: ' + statement)

            return False

    @staticmethod
    def execute_query(connection, query):
        try:
            with closing(connection.cursor()) as cursor:
                cursor.execute(query)

                return cursor.fetchall()
        except Error as e:
            Helper.print_error('SQL error: ' + str(e))
            Helper.print_error('Query was: ' + query)
        except:
            Helper.print_error('SQL error')
            Helper.print_error('Statement was: ' + query)

            return None

    @staticmethod
    def sql_create_table(table_name, col_list, type_list, primary_key=-1):
        sql_query = 'CREATE TABLE IF NOT EXISTS ' + table_name + ' ('

        for i in range(len(col_list) - 1):
            sql_query += col_list[i] + ' ' + type_list[i].name
            if i == primary_key:
                sql_query += ' PRIMARY KEY'
            sql_query += ', '

        if len(col_list) > 0:
            i = len(col_list) - 1
            sql_query += col_list[i] + ' ' + type_list[i].name + ');'

        return sql_query

    @staticmethod
    def sql_insert_query(name, values):
        sql_query = 'INSERT INTO ' + name + ' VALUES ('
        for i in range(len(values) - 1):
            sql_query += values[i] + ', '
        sql_query += values[len(values) - 1] + ');'

        return sql_query
