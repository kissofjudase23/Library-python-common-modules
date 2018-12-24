# -*- coding: utf-8 -*-

import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from contextlib import contextmanager

from ..log_utils import LogFactory, LogMode

try:
    _LOGGER = LogFactory.get_logger(name=__name__,
                                    mode=LogMode.SYSLOG,
                                    log_level=logging.ERROR)
except Exception:
    _LOGGER = LogFactory.get_logger(name=__name__,
                                    mode=LogMode.CONSOLE,
                                    log_level=logging.ERROR)

MYSQL_ENGINE = 'InnoDB'
MYSQL_CHARSET = 'utf8mb4'
MYSQL_COLLATE = 'utf8mb4_unicode_ci'


def _get_local_test_db_url():
    # For testing
    database = 'postman'
    username = 'root'
    password = '123'
    host = '127.0.0.1'
    port = '3306'
    db_charset = 'utf8mb4'

    db_url = f'mysql+pymysql://{username}:{password}@{host}:{port}/{database}?charset={db_charset}'

    return db_url


def get_db_url():
    # export LOCAL_TEST_DB_MODE=True before testing
    # if 'LOCAL_TEST_DB_MODE' in os.environ:
    return _get_local_test_db_url()


ENGINE = create_engine(get_db_url(), encoding="utf8", echo=False)

# DB_SESSION
DB_SESSION = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=True,
                                         bind=ENGINE))
BASE = declarative_base()
BASE.query = DB_SESSION.query_property()


@contextmanager
def transaction_context():
    session = DB_SESSION()

    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        DB_SESSION.remove()


def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    BASE.metadata.create_all(bind=ENGINE)
