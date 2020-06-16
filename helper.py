'''
Created on Jun 13, 2020

@author: Matthias Jung
'''

from argparse import ArgumentTypeError
from datetime import datetime
from os.path import isfile, isdir
from os import access
from os import R_OK
from sys import stderr


class Helper(object):
    '''
    Generic static helper methods
    '''

    def __init__(self, params):
        '''
        Constructor
        '''

    @staticmethod
    def print_error(*args, **kwargs):
        print(*args, file=stderr, **kwargs)

    @staticmethod
    def print_list(data):
        for row in data:
            print(row)

    @staticmethod
    def _get_first_element(list_list):
        return list_list[0][0] if list_list and len(list_list[0]) > 0 else None

    @staticmethod
    def _get_pair_list(list_list):
        result = []
        for p in list_list:
            result.append((p[0], p[1]))

        return result

    @staticmethod
    def is_boolean(n):
        nl = n.lower()
        return nl == 'y' or nl == 'n' or nl == '0' or nl == '1' or nl == 'true' or nl == 'false'

    @staticmethod
    def is_float(n):
        try:
            float(n)
            return True
        except ValueError:
            return False

    @staticmethod
    def is_integer(n):
        if not Helper.is_float(n):
            return False
        else:
            return float(n).is_integer()

    @staticmethod
    def is_date(n, fmt):
        try:
            datetime.strptime(n, fmt)
            return True
        except:
            return False

    @staticmethod
    def is_file(file_name):
        if not isfile(file_name):
            raise ArgumentTypeError('{0} does not exist'.format(file_name))
        else:
            return file_name

    @staticmethod
    def not_is_file(file_name):
        if isfile(file_name):
            raise ArgumentTypeError('{0} already exists'.format(file_name))
        else:
            return file_name

    @staticmethod
    def is_readable_dir(dir_name):
        if not isdir(dir_name):
            raise ArgumentTypeError('{0} is not a directory'.format(dir_name))
        elif not access(dir_name, R_OK):
            raise ArgumentTypeError('{0} is not readable'.format(dir_name))
        else:
            return dir_name
