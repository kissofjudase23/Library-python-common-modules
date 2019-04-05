import time
from functools import wraps


class Singleton(type):
    """
    https://stackoverflow.com/questions/6760685/creating-a-singleton-in-python
    Usage: class Logger(metaclass=Singleton):
            pass
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


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
