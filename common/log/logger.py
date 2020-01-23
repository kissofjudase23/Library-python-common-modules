#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import logging.handlers
from enum import IntEnum, unique


@unique
class LogMode(IntEnum):
    CONSOLE = 1
    SYSLOG = 2


class LogFactory(object):
    _SYSLOG_SOCKET = "/dev/log"
    _FORMATTER = logging.Formatter("[%(asctime)-15s] [%(levelname)-6s] [%(message)s]")
    _JSON_FORMATTER = logging.Formatter(
        "{'time':'%(asctime)s', 'name': '%(name)s', 'level': '%(levelname)s', 'message': '%(message)s'}")

    @classmethod
    def get_logger(cls,
                   *,
                   name,
                   mode=LogMode.CONSOLE,
                   log_level=logging.INFO,
                   optimize=False,
                   suppress_raise=True):

        """ custom logger
            Args:
                name:
                    name of your logger, use __name__ as a module level logger
                mode:
                    please refer LogMode
                log_level:
                    log level for your logger and handlers
                    ex: logging.INFO, logging.DEBUG
                optimize:
                    stop collecting extra info to sppeed up
                suppress_raise:
                    swallow exceptions while logging, suggest to use this option
                    on prod env
            Returns:
                logger obj
        """
        if optimize:
            logging._srcfile = None
            logging.logThreads = 0
            logging.logProcesses = 0

        if suppress_raise:
            logging.raiseExceptions = False

        logger = logging.getLogger(name)
        logger.setLevel(log_level)

        if mode & LogMode.CONSOLE:
            console_handler = logging.StreamHandler()
            console_handler.setLevel(log_level)
            console_handler.setFormatter(cls._FORMATTER)
            logger.addHandler(console_handler)

        if mode & LogMode.SYSLOG:
            sys_handler = logging.handlers.SysLogHandler(address=cls._SYSLOG_SOCKET)
            sys_handler.setLevel(log_level)
            sys_handler.setFormatter(cls._JSON_FORMATTER)
            logger.addHandler(sys_handler)

        return logger
