# implement your decorators here.
import logging
import signal
from .exceptions import TimeoutError

class count_calls(object):
    FUNCTION_COUNTS = {}

    def __init__(self, function):
        self.function = function
        self.FUNCTION_COUNTS[self.function.__name__] = 0

    @classmethod
    def counters(cls):
        return cls.FUNCTION_COUNTS

    def counter(self):
        return self.FUNCTION_COUNTS[self.function.__name__]

    def __call__(self, *args):
        self.FUNCTION_COUNTS[self.function.__name__] += 1
        return self.function(*args)


    @classmethod
    def reset_counters(cls):
        cls.FUNCTION_COUNTS = {}


class memoized(object):
    cache = {}
    def __init__(self, function):
        self.function = function

    def __call__(self, a, b):
        result = self.function(a, b)
        self.cache[(a, b)] = result
        return result



class debug(object):
    def __init__(self, logger=None):
        if logger:
            self.logger = logger
        else:
            logger = logging.getLogger('tests.test_decorators')
            logger.setLevel(logging.DEBUG)
            self.logger = logger

    def __call__(self, function):
        def wrapped(a, b):
            # logging.getLogger('tests.test_decorators')
            log_message_start = 'Executing "{0}" with params: ({1}, {2})'.format(function.__name__, a, b) + ', {}'
            self.logger.debug(log_message_start)
            result = function(a, b)
            log_message_finish = 'Finished "{}" execution with result: {}'.format(function.__name__,result)
            self.logger.debug(log_message_finish)
            return result
        return wrapped



class timeout(object):
    def __init__(self, timeout):
        self.timeout = timeout
  
    def _handle_timeout(self, signum, frame):
        raise TimeoutError("Function call timed out")
  
    def __call__(self, function):
        def wrapped():
            signal.signal(signal.SIGALRM, self._handle_timeout)
            signal.alarm(self.timeout)
            return function()
        return wrapped

def paramtype(original_function):
    def wrapped(param):
        param_type = type(param).__name__
        return "{} was called with {}: {}".format(original_function.__name__, param_type, param)
    return wrapped

    
def repeat_x_times(repeats=1):
    def wrapped(original_func):
        def some_func(param1, param2):
            return original_func(param1, param2) * repeats
        return some_func
    return wrapped

        