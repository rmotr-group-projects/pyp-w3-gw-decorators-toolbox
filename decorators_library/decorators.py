# implement your decorators here.
import signal
from decorators_library.exceptions import FunctionTimeoutException
import logging


def inspect(fn):

    MESSAGE = "{} invoked with {}. Result: {}"

    def decorated_fn(*args, **kwargs):

        inputs = ", ".join(str(x) for x in args)

        if not kwargs:

            print(MESSAGE.format(fn.__name__, inputs, fn(*args)))
            return fn(*args)

        # parse kwargs and include in MESSAGE
        kwargs_list = ["{}={}".format(k, v) for k, v in kwargs.items()]
        inputs += ', {}'.format(kwargs_list[0])

        print(MESSAGE.format(fn.__name__, inputs, fn(*args, **kwargs)))

        return fn(*args, **kwargs)

    return decorated_fn


def timeout(sec, my_exception=FunctionTimeoutException):

    def receive_alarm(signum, stack):
        """Raise a timed out exception"""
        raise my_exception('Function call timed out')

    def timeout_sec(fn):

        def decorated_fn():

            signal.signal(signal.SIGALRM, receive_alarm)
            signal.alarm(sec)

            fn()

        return decorated_fn

    return timeout_sec


class count_calls(object):

    counters_record = {}

    def __init__(self, fn):
        """what exactly is self here ???"""
        self.fn = fn
        self.call_count = 0
        self.counters_record[fn] = self

    def __call__(self):
        self.call_count += 1
        return self.fn()

    def counter(self):
        """Return current count for self"""
        return count_calls.counters_record[self.fn].call_count

    # Class methods are methods that are not bound to an object, but to a class.
    # Do not need to initialize an instance of this class to use these methods
    @classmethod
    def counters(cls):
        return dict((key.__name__, value.call_count) for key, value in cls.counters_record.items())

    @classmethod
    def reset_counters(cls):
        cls.counters_record = {}


class memoized(object):

    previous_arguments = {}

    def __init__(self, fn):
        self.fn = fn

    def __call__(self, a, b):
        """Make class callable as a function"""

        prev_arg = memoized.previous_arguments

        if (a, b) in prev_arg:
            return prev_arg[(a, b)]

        else:

            prev_arg[(a, b)] = self.fn(a, b)

        return self.fn(a, b)

    @property
    def cache(self):
        return memoized.previous_arguments


def debug(logger=None):
    """
    - How does logging work??? what is it used for?
    """

    debug.logger = logger

    def wrapper(fn):
        logger = debug.logger
        if not logger:
            logger = logging.basicConfig(level=logging.DEBUG)
            logger = logging.getLogger(fn.__module__)

        def inner(*args, **kwargs):
            logger.debug('Executing "{}" with params: {}, {}'.format(fn.__name__, args, kwargs))
            results = fn(*args, **kwargs)
            logger.debug('Finished "{}" execution with result: {}'.format(fn.__name__, results))
            return results

        return inner

    return wrapper
