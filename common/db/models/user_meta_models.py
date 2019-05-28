# -*- coding: utf-8 -*-

import json

from enum import IntEnum, IntFlag, unique

from sqlalchemy import Column
from sqlalchemy.dialects.mysql import CHAR, VARCHAR, DATETIME, INTEGER, FLOAT, BOOLEAN

from sqlalchemy.schema import ForeignKeyConstraint
from sqlalchemy.sql.expression import func
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import validates
from sqlalchemy.ext.hybrid import hybrid_property

from .model_base import ModelUtils
from ...compare import Utils
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

    # composite primary key, cid + uid
    cid = Column(VARCHAR(128), primary_key=True)
    uid = Column(VARCHAR(128), primary_key=True)

    models = relationship('Model',
                          cascade='all, delete-orphan',
                          back_populates='user',
                          order_by='Model.meta_version')

    metas = relationship('Meta',
                         cascade='all, delete-orphan',
                         back_populates='user',
                         order_by='Meta.version')

    domain = Column(VARCHAR(256), nullable=True)

    create_time = Column(DATETIME(),
                         server_default=func.now(),
                         nullable=False)

    last_update_time = Column(DATETIME(),
                              server_default=func.now(),
                              onupdate=func.now(),
                              nullable=False)

    @staticmethod
    def merge(cid_, uid_, *, domain=None):
        with transaction_context() as session:

            cid = cid_.upper()
            uid = uid_.upper()

            kwargs = {'cid': cid, 'uid': uid}

            record = session.query(User).filter_by(**kwargs).one_or_none()

            if not record:
                record = User(cid, uid, domain=domain)
                session.merge(record)
            else:
                if domain and not record.domain:
                    record.domain = domain

    @staticmethod
    def delete(cid_, uid):
        with transaction_context() as session:
            cid = cid_.upper()

            kwargs = {'cid': cid, 'uid': uid}

            record = session.query(User).filter_by(**kwargs).one_or_none()

            if record:
                session.delete(record)

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

    @validates('cid')
    def validate_cid(self, _, cid_):
        return cid_.upper()

    @validates('uid')
    def validate_cid(self, _, uid):
        return uid.upper()

    def __init__(self, cid, uid,
                 *,
                 domain=None):

        self.cid = cid

        self.uid = uid

        self.domain = domain

    def __repr__(self):
        return f'[' \
               f'<cid:{self.cid}>\n' \
               f'<uid:{self.uid}>\n' \
               f'<domain:{self.domain}>\n' \
               f']'


class Meta(BASE, ModelUtils):

    __tablename__ = 'meta'

    # composite primary key, cid + uid + version + category
    # composite foreign key, cid + uid
    cid = Column(VARCHAR(128), primary_key=True)
    uid = Column(VARCHAR(128), primary_key=True)
    version = Column(INTEGER(unsigned=True, primary_key=True))
    category = Column(INTEGER(unsigned=True, primary_key=True))

    __table_args__ = (ForeignKeyConstraint([cid, uid],
                                           [User.cid, User.uid]),
                      {'mysql_engine': MYSQL_ENGINE,
                       'mysql_charset': MYSQL_CHARSET,
                       'mysql_collate': MYSQL_COLLATE})

    # models
    user = relationship('User',
                        back_populates='metas')

    count = Column(INTEGER(unsigned=True))

    create_time = Column(DATETIME(),
                         server_default=func.now(),
                         nullable=False)

    last_update_time = Column(DATETIME(),
                              server_default=func.now(),
                              onupdate=func.now(),
                              nullable=False)

    @staticmethod
    def verify_category(category):
        if category not in VALID_META_CATS:
            raise InvalidCategory(category)

    @staticmethod
    def verify_version(version):
        if version not in VALID_META_VERSIONS:
            raise InvalidVersion(version)

    @validates('category')
    def validate_category(self, _, category):
        Meta.verify_category(category)
        return category

    @validates('version')
    def validate_version(self, _, version):
        Meta.verify_version(version)
        return version

    def __init__(self,
                 cid,
                 uid,
                 version,
                 category,
                 *,
                 count=0):

        self.cid = cid
        self.uid = uid
        self.version = version
        self.category = category
        self.count = count

    def __repr__(self):
        return f'[\n' \
               f'<cid:{self.cid}>\n' \
               f'<uid:{self.uid}>\n' \
               f'<version:{self.version}>\n' \
               f'<category:{self.category}>\n' \
               f'<count:{self.count}>\n'\
               f'<create_time:{self.create_time}>\n' \
               f'<last_update_time:{self.last_update_time}>\n' \
               f']'


class Model(BASE, ModelUtils):

    __tablename__ = 'model'

    # composite primary key, cid + uid + version + meta_version
    # composite foreign key, cid + uid
    cid = Column(VARCHAR(128), primary_key=True)
    uid = Column(VARCHAR(128), primary_key=True)
    meta_version = Column(INTEGER(unsigned=True, primary_key=True))

    __table_args__ = (ForeignKeyConstraint([cid, uid],
                                           [User.cid, User.uid]),
                      {'mysql_engine': MYSQL_ENGINE,
                       'mysql_charset': MYSQL_CHARSET,
                       'mysql_collate': MYSQL_COLLATE})

    # models
    user = relationship('User',
                        back_populates='models')

    maturity = Column(FLOAT(unsigned=True))

    accuracy = Column(FLOAT(unsigned=True))

    is_ready = Column(BOOLEAN())

    create_time = Column(DATETIME(),
                         server_default=func.now(),
                         nullable=False)

    last_update_time = Column(DATETIME(),
                              server_default=func.now(),
                              onupdate=func.now(),
                              nullable=False)

    _languages = Column(VARCHAR(2048))

    @staticmethod
    def generate_id(meta_version, user_id):
        # meta_version should refer Version
        return HashUtility.get_normalized_str_sha256(f'{meta_version}{user_id}')

    @staticmethod
    def verify_meta_version(meta_version):
        if meta_version not in VALID_META_VERSIONS:
            raise InvalidVersion(meta_version)

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
                 cid,
                 uid,
                 meta_version,
                 *,
                 maturity=0.0,
                 accuracy=0.0,
                 is_ready=False,
                 languages=None):

        self.cid = cid
        self.uid = uid
        self.meta_version = meta_version

        self.maturity = maturity
        self.accuracy = accuracy
        self.is_ready = is_ready
        self.languages = languages

    def __repr__(self):
        return f'[\n' \
               f'<cid:{self.cid}>\n'\
               f'<uid:{self.uid}>\n'\
               f'<meta_version:{self.meta_version}>\n'\
               f'<maturity:{self.maturity}>\n'\
               f'<accuracy:{self.accuracy}>\n' \
               f'<create_time:{self.create_time}>\n' \
               f'<last_update_time:{self.last_update_time}>\n' \
               f'<languages:{self.languages}>\n' \
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
