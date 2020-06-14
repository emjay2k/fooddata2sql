'''
Created on Jun 13, 2020

@author: Matthias Jung
'''

from sqlhelper import SqlHelper
from abc import ABC, abstractmethod


class SqlConnection(ABC):
    '''
    encapsulate sql database connection and queries
    '''

    def __init__(self):
        self._open_db()

    @abstractmethod
    def _open_db(self):
        pass
    
    def query(self, query):
        return SqlHelper.execute_query(self.connection, query)
