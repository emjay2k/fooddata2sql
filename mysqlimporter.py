'''
Created on Jun 13, 2020

@author: Matthias Jung
'''

import mysql.connector
from sqlimporter import SqlImporter
from helper import Helper


class MysqlImporter(SqlImporter):
    '''
    Untested mysql importer
    '''

    def __init__(self, user, password, host, port, database):
        super().__init__()
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.database = database

    def _open_db(self):
        try:
            self.connection = mysql.connector.connect(host=self.host, port=self.port, user=self.user, passwd=self.password, database=self.database)
            return True
        except mysql.connector.Error as e:
            Helper.print_error('SQL error: ' + str(e))
            Helper.print_error('database was: ' + self.db_file)

        return False
