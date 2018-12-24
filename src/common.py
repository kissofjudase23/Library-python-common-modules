import time
import re
from functools import wraps


def retry(exceptions, *, tries=4, delay=1, back_off=2, logger=None):
    """
    Retry calling the decorated function using an exponential back-off.

    Args:
        exceptions: The exception to check. may be a tuple of
            exceptions to check.
        tries: Number of times to try (not retry) before giving up.
        delay: Initial delay between retries in seconds.
        back_off: Back-off multiplier (e.g. value of 2 will double the delay
            each retry).
        logger: Logger to use. If None, print.
    """
    def deco_retry(f):

        @wraps(f)
        def f_retry(*args, **kwargs):

            m_tries, m_delay = tries, delay

            while m_tries > 1:
                try:
                    return f(*args, **kwargs)
                except exceptions as e:
                    msg = f'Retrying in {m_delay} seconds, err:{e}'
                    if logger:
                        logger.warning(msg)
                    else:
                        print(msg)
                    time.sleep(m_delay)
                    m_tries -= 1
                    m_delay *= back_off
            return f(*args, **kwargs)

        return f_retry

    return deco_retry


class Utils(object):

    @staticmethod
    def is_equal(data, test_case):
        if data == test_case:
            return True
        return False

    @staticmethod
    def is_re_match(data, test_case):
        if re.match(data, test_case, re.IGNORECASE):
            return True
        return False

    @staticmethod
    def compile_regex_data(data_list):
        """ Compile regex object from the data_list
            It's ok even the data_list is empty

        :param data_list:
        :return:
            compiled regex object
            empty list
        """

        # TODO, fix here
        # It is tricky here, since compiled regex from empty list would match anything
        # However, return empty list is not a good idea too
        # try to raise some useful info to let caller decide what to do
        if not data_list:
            return list()

        # re format should be  (expression1|expression2|expression3
        data_list_re = f"({'|'.join(data_list)})"

        compiled_data_list_re = re.compile(data_list_re, re.IGNORECASE)

        return compiled_data_list_re

    @staticmethod
    def compile_exactly_regex_data(data_list):
        """ Compile regex object from the data_list
            It's ok even the data_list is empty

        :param data_list:
        :return: compiled regex object
        """

        # TODO, fix here
        # It is tricky here, since compiled regex from empty list would match anything
        # However, return empty list is not a good idea too
        # try to raise some useful info to let caller decide what to do
        if not data_list:
            return list()

        # re format should be  (expression1|expression2|expression3)$
        data_list_re = f"({'|'.join(data_list)})$"

        compiled_data_list_re = re.compile(data_list_re, re.IGNORECASE)

        return compiled_data_list_re