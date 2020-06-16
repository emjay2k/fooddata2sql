'''
Created on Jun 13, 2020

@author: Matthias Jung
'''

import psycopg2
from mysqlimporter import MysqlImporter
from helper import Helper


class PgsqlImporter(MysqlImporter):
    '''
    Untested pgsql importer
    '''

    def __init__(self, user, password, host, port, database):
        super().__init__(user, password, host, port, database)

    def _open_db(self):
        try:
            self.connection = psycopg2.connect(host=self.host, port=self.port, user=self.user, passwd=self.password, database=self.database)
            return True
        except psycopg2.Error as e:
            Helper.print_error('SQL error: {0}'.format(str(e)))
            Helper.print_error('database was: {0}'.format(self.db_file))

        return False
