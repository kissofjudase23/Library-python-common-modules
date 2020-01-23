import logging
from common.log.logger import LogFactory, LogMode


class TestLinkedList(object):

    def test_logger(self):
        logger = LogFactory.get_logger(name="test logger")
        logger.info("test info")
        logger.warning("test warning")
