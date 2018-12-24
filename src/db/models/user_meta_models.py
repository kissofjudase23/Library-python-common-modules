# -*- coding: utf-8 -*-

import json

from enum import IntEnum, IntFlag, unique

from sqlalchemy import Column
from sqlalchemy.dialects.mysql import CHAR, VARCHAR, DATETIME, INTEGER, FLOAT, BOOLEAN

from sqlalchemy.sql.expression import func
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import validates
from sqlalchemy.ext.hybrid import hybrid_property

from .model_base import ModelUtils
from ...common import Utils
from ..database import MYSQL_ENGINE, MYSQL_CHARSET, MYSQL_COLLATE
from ..database import BASE, transaction_context
from ..exc import DuplicateKey, InvalidCategory, InvalidVersion
from ...hash_utils import HashUtility


@unique
class MetaVersion(IntEnum):
    V1 = 1


VALID_META_VERSIONS = [enum.value for enum in MetaVersion]


@unique
class MetaCategory(IntFlag):
    RAW = 1


VALID_META_CATS = [enum.value for enum in MetaCategory]


class User(BASE, ModelUtils):

    __tablename__ = 'user'

    __table_args__ = {'mysql_engine': MYSQL_ENGINE,
                      'mysql_charset': MYSQL_CHARSET,
                      'mysql_collate': MYSQL_COLLATE}

    @staticmethod
    def merge(cid_, uid, *, domain=None):
        with transaction_context() as session:

            cid = cid_.upper()

            kwargs = {'cid': cid, 'uid': uid}

            record = session.query(User).filter_by(**kwargs).one_or_none()

            if not record:
                record = User(cid, uid, domain=domain)
                session.merge(record)
            else:
                if domain and not record.domain:
                    record.domain = domain

    @staticmethod
    def get_id(cid_, uid):
        with transaction_context() as session:

            cid = cid_.upper()

            kwargs = {'cid': cid, 'uid': uid}

            record = session.query(User).filter_by(**kwargs).one_or_none()

            if not record:
                return None

            return record.id

    @staticmethod
    def delete(cid_, uid):
        with transaction_context() as session:

            cid = cid_.upper()

            kwargs = {'cid': cid, 'uid': uid}

            record = session.query(User).filter_by(**kwargs).one_or_none()

            if record:
                session.delete(record)

    @staticmethod
    def generate_id(cid_, uid):
        cid = cid_.upper()
        return HashUtility.get_normalized_str_sha256(f'{cid}{uid}')

    @classmethod
    def verify_duplicate_key(cls, cid_, uid):

        record_id = cls.generate_id(cid_, uid)

        with transaction_context() as session:
            if session.query(cls).filter(cls.record_id == record_id).one_or_none():
                raise DuplicateKey(record_id)

    @staticmethod
    def select_domain(cid):

        data_list = list()

        with transaction_context() as session:
            # use User.domain.isnot(None) would get a False result (False,)
            records = session.query(User.domain)\
                             .filter(User.cid == cid)\
                             .distinct(User.domain).all()

            for record in records:
                if not record.domain:
                    continue

                data_list.append(record.domain)

        return data_list

    @staticmethod
    def get_compiled_regex_domain(cid):

        domain_list = User.select_domain(cid=cid)

        return Utils.compile_regex_data(domain_list)

    # sha256 of f'{cid}{uid}'
    id = Column(CHAR(64), primary_key=True)

    postman_models = relationship('PostmanModel',
                                  cascade='all, delete-orphan',
                                  back_populates='user',
                                  order_by='PostmanModel.meta_version'
                                  )

    metas = relationship('Meta',
                         cascade='all, delete-orphan',
                         back_populates='user',
                         order_by='Meta.version')

    cid = Column(VARCHAR(128), nullable=False, index=True)

    uid = Column(VARCHAR(128), nullable=False, index=True)

    domain = Column(VARCHAR(256), nullable=True, index=False)

    create_time = Column(DATETIME(),
                         server_default=func.now(),
                         nullable=False)

    last_update_time = Column(DATETIME(),
                              server_default=func.now(),
                              onupdate=func.now(),
                              nullable=False)

    @validates('cid')
    def validate_cid(self, _, cid_):
        return cid_.upper()

    def __init__(self, cid, uid,
                 *,
                 domain=None):

        self.cid = cid

        self.uid = uid

        self.id = User.generate_id(self.cid, self.uid)

        self.domain = domain

    def __repr__(self):
        return f'[' \
               f'<id:{self.id}>\n' \
               f'<cid:{self.cid}>\n' \
               f'<uid:{self.uid}>\n' \
               f'<domain:{self.domain}>\n' \
               f']'


class Meta(BASE, ModelUtils):

    __tablename__ = 'meta'

    __table_args__ = {'mysql_engine': MYSQL_ENGINE,
                      'mysql_charset': MYSQL_CHARSET,
                      'mysql_collate': MYSQL_COLLATE}

    @staticmethod
    def generate_id(version, category, user_id):
        return HashUtility.get_normalized_str_sha256(f'{version}{category}{user_id}')

    @classmethod
    def verify_duplicate_key(cls, version, category, user_id):

        record_id = cls.generate_id(version, category, user_id)

        with transaction_context() as session:
            if session.query(cls).filter(cls.id == record_id).one_or_none():
                raise DuplicateKey(record_id)

    @staticmethod
    def verify_category(category):
        if category not in VALID_META_CATS:
            raise InvalidCategory(category)

    @staticmethod
    def verify_version(version):
        if version not in VALID_META_VERSIONS:
            raise InvalidVersion(version)

    # sha256 of {meta_version}{meta_category}{user_id}
    id = Column(CHAR(64), primary_key=True)

    user_id = Column(CHAR(64), ForeignKey('user.id'), nullable=False, index=True)

    # models
    user = relationship('User',
                        back_populates='metas')

    version = Column(INTEGER(unsigned=True), index=True)

    category = Column(INTEGER(unsigned=True), index=True)

    count = Column(INTEGER(unsigned=True))

    create_time = Column(DATETIME(),
                         server_default=func.now(),
                         nullable=False)

    last_update_time = Column(DATETIME(),
                              server_default=func.now(),
                              onupdate=func.now(),
                              nullable=False)

    meta_last_update_time = Column(DATETIME(),
                                   server_default=func.now(),
                                   nullable=False)

    @validates('category')
    def validate_category(self, _, category):
        Meta.verify_category(category)
        return category

    @validates('version')
    def validate_version(self, _, version):
        Meta.verify_version(version)
        return version

    def __init__(self,
                 user_id,
                 version,
                 category,
                 *,
                 count=0):

        self.version = version

        self.category = category

        self.user_id = user_id

        self.id = Meta.generate_id(self.version,
                                   self.category,
                                   self.user_id)

        self.count = count

    def __repr__(self):
        return f'[\n' \
               f'<id:{self.id}>\n' \
               f'<user_id:{self.user_id}>\n' \
               f'<version:{self.version}>\n' \
               f'<category:{self.category}>\n' \
               f'<count:{self.count}>\n'\
               f'<create_time:{self.create_time}>\n' \
               f'<last_update_time:{self.last_update_time}>\n' \
               f']'


class PostmanModel(BASE, ModelUtils):

    __tablename__ = 'postman_model'

    __table_args__ = {'mysql_engine': MYSQL_ENGINE,
                      'mysql_charset': MYSQL_CHARSET,
                      'mysql_collate': MYSQL_COLLATE}

    @staticmethod
    def generate_id(meta_version, user_id):
        # meta_version should refer Version
        return HashUtility.get_normalized_str_sha256(f'{meta_version}{user_id}')

    @classmethod
    def verify_duplicate_key(cls, meta_version, user_id):

        record_id = cls.generate_id(meta_version, user_id)

        with transaction_context() as session:
            if session.query(cls).filter(cls.id == record_id).one_or_none():
                raise DuplicateKey(record_id)

    @staticmethod
    def verify_meta_version(meta_version):
        if meta_version not in VALID_META_VERSIONS:
            raise InvalidVersion(meta_version)

    # sha256 of {meta_version}{user_id}
    id = Column(CHAR(64), primary_key=True)

    user_id = Column(CHAR(64), ForeignKey('user.id'), nullable=False, index=True)

    # models
    user = relationship('User',
                        back_populates='postman_models')

    meta_version = Column(INTEGER(unsigned=True), index=True)

    target_meta_files_hash = Column(VARCHAR(64), nullable=True)

    maturity = Column(FLOAT(unsigned=True))

    accuracy = Column(FLOAT(unsigned=True))

    is_ready = Column(BOOLEAN())

    s3_version_id = Column(VARCHAR(64))

    create_time = Column(DATETIME(),
                         server_default=func.now(),
                         nullable=False)

    last_update_time = Column(DATETIME(),
                              server_default=func.now(),
                              onupdate=func.now(),
                              nullable=False)

    _languages = Column(VARCHAR(2048))

    @validates('meta_version')
    def validate_meta_version(self, _, meta_version):
        Meta.verify_version(meta_version)
        return meta_version

    @hybrid_property
    def languages(self):
        # load json string to dict if it is not None
        if not self._languages:
            return self._languages
        return json.loads(self._languages)

    @languages.setter
    def languages(self, languages):
        # dump to json string if it is not None
        if languages:
            self._languages = json.dumps(languages)
        else:
            self._languages = None

    def __init__(self,
                 user_id,
                 meta_version,
                 *,
                 maturity=0.0,
                 accuracy=0.0,
                 is_ready=False,
                 s3_version_id=None,
                 languages=None,
                 target_meta_files_hash=None):

        self.user_id = user_id

        self.meta_version = meta_version

        self.id = PostmanModel.generate_id(self.meta_version, self.user_id)

        self.maturity = maturity

        self.accuracy = accuracy

        self.is_ready = is_ready

        self.s3_version_id = s3_version_id

        self.languages = languages

        self.target_meta_files_hash = target_meta_files_hash

    def __repr__(self):
        return f'[\n' \
               f'<id:{self.id}>\n'\
               f'<meta_version:{self.meta_version}>\n'\
               f'<user_id:{self.user_id}>\n'\
               f'<maturity:{self.maturity}>\n'\
               f'<accuracy:{self.accuracy}>\n' \
               f'<s3_version_id:{self.s3_version_id}>\n' \
               f'<create_time:{self.create_time}>\n' \
               f'<last_update_time:{self.last_update_time}>\n' \
               f'<languages:{self.languages}>\n' \
               f'<languages:{self.target_meta_files_hash}>\n' \
               f']'

    def to_dict(self):

        res_dict = self.__dict__.copy()

        # remove this key for JSON serializable
        if '_sa_instance_state' in res_dict:
            res_dict.pop('_sa_instance_state', None)

        if '_languages' in res_dict:
            if res_dict['_languages'] is not None:
                # Don't be confused with this warning
                # Sqlalchemy use @hybrid_property instead of @property for more general
                # use case (eg, filter)
                res_dict['languages'] = self.languages
            else:
                res_dict['languages'] = None

            res_dict.pop('_languages', None)

        return res_dict
