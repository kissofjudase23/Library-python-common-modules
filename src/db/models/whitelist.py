# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod
from enum import IntEnum, unique

from sqlalchemy import Column
from sqlalchemy.dialects.mysql import CHAR, VARCHAR, DATETIME, SMALLINT
from sqlalchemy.sql.expression import func
import sqlalchemy.orm.exc as orm_exc
from sqlalchemy.orm import validates

from .model_base import ModelUtils
from ...common import Utils
from ..database import MYSQL_ENGINE, MYSQL_CHARSET, MYSQL_COLLATE
from ..database import BASE, transaction_context
from ..exc import KeyNotFound, DuplicateKey, InvalidCategory, InvalidStatus, ErrorTestCase
from ...hash_utils import HashUtility


@unique
class Status(IntEnum):
    DISABLE = 0
    ENABLE = 1


VALID_STATUS = [enum.value for enum in Status]


@unique
class Category(IntEnum):
    FROM_ADDRESS = 1
    MSG_ID = 2


VALID_CATEGORIES = [enum.value for enum in Category]


# mixin with ModelUtils
class WhiteList(BASE, ModelUtils):

    __tablename__ = 'white_list'

    __table_args__ = {'mysql_engine': MYSQL_ENGINE,
                      'mysql_charset': MYSQL_CHARSET,
                      'mysql_collate': MYSQL_COLLATE}

    @staticmethod
    def generate_id(category, data):
        return HashUtility.get_normalized_str_sha256(f'{category}/{data}')

    @classmethod
    def verify_duplicate_key(cls, category, data):

        record_id = cls.generate_id(category, data)

        with transaction_context() as session:
            if session.query(cls).filter(cls.id == record_id).one_or_none():
                raise DuplicateKey(record_id)

    @staticmethod
    def verify_category(category):
        if category not in VALID_CATEGORIES:
            raise InvalidCategory(category)

    @staticmethod
    def verify_status(status):
        if status not in VALID_STATUS:
            raise InvalidStatus(status)

    # sha256 of data and test_cases
    id = Column(CHAR(64), primary_key=True)

    # note, timezone is not used by the MySQL dialect
    create_time = Column(DATETIME(),
                         server_default=func.now(),
                         nullable=False)

    last_update_time = Column(DATETIME(),
                              server_default=func.now(),
                              onupdate=func.now(),
                              nullable=False)

    category = Column(SMALLINT(unsigned=True), nullable=False, index=True)
    status = Column(SMALLINT(unsigned=True), nullable=False, index=True)

    data = Column(VARCHAR(length=2048), nullable=False)
    test_case = Column(VARCHAR(length=2048), nullable=False)
    submitter = Column(VARCHAR(length=2048), nullable=False)
    comment = Column(VARCHAR(length=4096), nullable=True)

    @validates('category')
    def validate_category(self, _, category):
        WhiteList.verify_category(category)
        return category

    @validates('status')
    def validate_status(self, _, status):
        WhiteList.verify_status(status)
        return status

    def __init__(self,
                 category,
                 data,
                 test_case,
                 submitter,
                 *,
                 status=Status.ENABLE.value,
                 comment=None):

        self.category = category
        self.status = status
        self.data = data

        self.id = self.generate_id(self.category, self.data)

        self.test_case = test_case
        self.submitter = submitter

        if comment:
            self.comment = comment

    def __repr__(self):
        return f'[\n' \
               f'<data:{self.data}>\n' \
               f'<test_case:{self.test_case}>\n'\
               f'<id:{self.id}>\n' \
               f'<status:{self.status}>\n' \
               f'<category:{self.category}>\n'\
               f'<status:{self.status}>\n' \
               f'<submitter:{self.submitter}>\n' \
               f'<comment:{self.comment}>\n'\
               f'<create_time>:{self.create_time}\n'\
               f'<last_update_time>:{self.last_update_time}\n' \
               f']'

    def to_dict(self):

        res_dict = self.__dict__.copy()

        # remove this key for JSON serializable
        if '_sa_instance_state' in res_dict:
            res_dict.pop('_sa_instance_state', None)

        res_dict['last_update_time'] = str(res_dict['last_update_time'])
        res_dict['create_time'] = str(res_dict['create_time'])

        return res_dict


class WhiteListUtility(metaclass=ABCMeta):

    @classmethod
    @abstractmethod
    def get_instance(cls):
        raise NotImplementedError("user must define get instance class method")

    def __init__(self, verify_method, regex_compiled_method):
        self.verify_data = verify_method
        self.regex_compiled_method = regex_compiled_method

    @property
    @abstractmethod
    def category(self):
        raise NotImplementedError("user must define category property")

    def insert(self,
               data,
               test_case,
               submitter,
               status=Status.ENABLE.value,
               comment=None):

        if not self.verify_data(data, test_case):
            raise ErrorTestCase(test_case, data)

        WhiteList.verify_duplicate_key(self.category, data)

        # commit the new record
        with transaction_context() as session:
            new_record = WhiteList(self.category,
                                   data,
                                   test_case,
                                   submitter,
                                   status=status,
                                   comment=comment)

            session.add(new_record)
            new_record_id = new_record.id

        with transaction_context() as session:
            committed_record = session.query(WhiteList)\
                                      .filter(WhiteList.id == new_record_id)\
                                      .one().to_dict()

        return committed_record

    def update(self,
               record_id,
               submitter,
               test_case=None,
               status=None,
               comment=None):

        with transaction_context() as session:

            try:
                update_record = session.query(WhiteList)\
                                       .filter(WhiteList.id == record_id).one()
            except orm_exc.NoResultFound:
                raise KeyNotFound(record_id)
            except orm_exc.MultipleResultsFound:
                raise DuplicateKey(record_id)

            if test_case and not self.verify_data(update_record.data, test_case):
                raise ErrorTestCase(test_case, update_record.data)

            update_record.submitter = submitter

            if test_case:
                update_record.test_case = test_case

            # note, can not use true/false evaluation here, since status
            # may be 0
            if status is not None:
                update_record.status = status

            if comment:
                update_record.comment = comment

        with transaction_context() as session:
            committed_record = session.query(WhiteList)\
                                      .filter(WhiteList.id == record_id)\
                                      .one().to_dict()

        return committed_record

    def select(self, test_case=None, status=None):

        result = list()

        with transaction_context() as session:

            query_records = session.query(WhiteList)\
                                   .filter(WhiteList.category == self.category)

            # note, can not use true/false evaluation here, since status
            # may be 0
            if status is not None:
                WhiteList.verify_status(status)
                query_records = query_records.filter(WhiteList.status == status)

            records = query_records.all()

            if test_case:
                for record in records:
                    if self.verify_data(record.data, test_case):
                        result.append(record.to_dict())
            else:
                for record in records:
                    result.append(record.to_dict())

        return result

    @staticmethod
    def select_data(**filter_kwargs):
        data_list = list()

        with transaction_context() as session:
            records = session.query(WhiteList.data)\
                             .filter_by(**filter_kwargs)\
                             .distinct(WhiteList.data).all()

            for record in records:
                data_list.append(record.data)

        return data_list

    def get_compiled_regex_data(self, status=Status.ENABLE.value):

        data_list = self.select_data(category=self.category,
                                     status=status)

        return self.regex_compiled_method(data_list)

    @staticmethod
    def delete(record_id):

        with transaction_context() as session:
            try:
                record = session.query(WhiteList).filter(WhiteList.id == record_id).one()

            except orm_exc.NoResultFound:
                raise KeyNotFound(record_id)
            except orm_exc.MultipleResultsFound:
                raise DuplicateKey(record_id)

            session.delete(record)

        return record_id

# TODO, use metaclass
class WhiteListFromUtility(WhiteListUtility):

    _instance = None

    # use class method as factory
    @classmethod
    def get_instance(cls):
        if not cls._instance:
            cls._instance = cls(verify_method=Utils.is_re_match,
                                regex_compiled_method=Utils.compile_regex_data)
        return cls._instance

    def __init__(self, verify_method, regex_compiled_method):
        super().__init__(verify_method, regex_compiled_method)

    @property
    def category(self):
        return Category.FROM_ADDRESS.value


# TODO, use metaclass
class WhiteListMsgIdUtility(WhiteListUtility):

    _instance = None

    # use class method as factory
    @classmethod
    def get_instance(cls):
        if not cls._instance:
            cls._instance = cls(verify_method=Utils.is_re_match,
                                regex_compiled_method=Utils.compile_regex_data)
        return cls._instance

    def __init__(self, verify_method, regex_compiled_method):
        super().__init__(verify_method, regex_compiled_method)

    @property
    def category(self):
        return Category.MSG_ID.value
