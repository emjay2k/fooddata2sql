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

    def queries(self, query_list, result_index):
        result = None
        for i in range(len(query_list)):
            temp_result = self.query(query_list[i])
            if i == result_index:
                result = temp_result

        return result
