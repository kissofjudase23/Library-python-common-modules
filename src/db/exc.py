# -*- coding: utf-8 -*-


from ..exc import BaseError


class DbBaseError(BaseError):
    """ Base Error for DB Utilities
    """
    pass


class KeyBaseError(DbBaseError):
    """ Intermediate Error for DB Key
    """
    pass


class KeyNotFound(KeyBaseError):
    def __init__(self, key):
        super().__init__(f'key {key} cat not be found')


class DuplicateKey(KeyBaseError):
    def __init__(self, key):
        super().__init__(f'duplicate key {key}')


class InvalidCategory(DbBaseError):
    def __init__(self, category):
        super().__init__(f'Invalid Category {category}')


class InvalidVersion(DbBaseError):
    def __init__(self, version):
        super().__init__(f'Invalid Category {version}')


class InvalidStatus(DbBaseError):
    def __init__(self, status):
        super().__init__(f'Invalid Status {status}')


class ErrorTestCase(DbBaseError):
    def __init__(self, test_case, data):
        super().__init__(f'Invalid test_case {test_case} for data {data}')
