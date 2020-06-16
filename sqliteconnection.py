'''
Created on Jun 13, 2020

@author: Matthias Jung
'''

import sqlite3
from sqlite3 import Error
from helper import Helper
from sqlconnection import SqlConnection


class SqliteConnection(SqlConnection):
    '''
    encapsulate sqlite database connection and queries
    '''

    def __init__(self, db_file):
        self.db_file = db_file
        super().__init__()

    def _open_db(self):
        try:
            self.connection = sqlite3.connect(self.db_file)
            return True
        except Error as e:
            Helper.print_error('SQL error: {0}'.format(str(e)))
            Helper.print_error('database was: {0}'.format(self.db_file))

        return False
