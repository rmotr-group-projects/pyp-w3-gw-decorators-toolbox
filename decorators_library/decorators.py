import functools
import collections
import signal
from decorators_library.exceptions import FunctionTimeoutException

def inspect(function):
    @functools.wraps(function)
    def wrapper(x, y, operation='add'):
        if operation == 'add':
            result = function(x, y)
            print('{} invoked with {}, {}. Result: {}'.format(function.__name__, x, y, result))
        else:
            result = function(x, y, operation)
            print('{} invoked with {}, {}, operation={}. Result: {}'.format(function.__name__, x, y, operation, result))
        return result
    return wrapper


class timeout(object):
    def __init__(self, duration, exception=FunctionTimeoutException):
        self.duration = duration
        self.exception = exception
    
    def raise_alarm(self, signum, stack):
        raise self.exception("Function call timed out")

    def __call__(self, function):
        @functools.wraps(function)
        def wrapped(*args, **kwargs):
            signal.signal(signal.SIGALRM, self.raise_alarm)
            signal.alarm(self.duration)
            return function(*args, **kwargs)
        signal.alarm(0)
        return wrapped


class memoized(object):
    def __init__(self, function):
        self.function = function
        self.cache = {}
    
    def __call__(self, *args):
        if not isinstance(args, collections.Hashable):
            return self.function(args)
        if args in self.cache:
            return self.cache[args]
        else:
            value = self.function(*args)
            self.cache[args] = value
            return value


class count_calls(object):
    FUNCTION_COUNTERS = {}
    
    def __init__(self, function):
        self.function = function
        self.calls = 0
        count_calls.FUNCTION_COUNTERS[function] = self

    
    def __call__(self, *args, **kwargs):
        self.calls += 1
        return self.function(*args, **kwargs)
    
    def counter(self):
        return count_calls.FUNCTION_COUNTERS[self.function].calls
    
    @classmethod
    def counters(cls):
        return dict([(f.__name__, cls.FUNCTION_COUNTERS[f].calls)
                     for f in cls.FUNCTION_COUNTERS])

    @classmethod
    def reset_counters(cls):
        cls.FUNCTION_COUNTERS = {}


class debug(object):
    def __init__(self, logger=None):
        self.logger = logger
  
    def __call__(self, fn):
        @wraps(fn)
        def new_fn(*args, **kwargs):
            kwarg_lst = ', '.join(['{}={}'.format(key, val) for key, val in kwargs.items()])
            arg_str = ', '.join(map(str,args))
            
            if not self.logger:
                self.logger = logging.getLogger('tests.test_decorators')
            
            self.logger.debug('Executing "{}" with params: ({}), {{{}}}'.format(fn.__name__, arg_str, kwarg_lst))
            fn_result = fn(*args, **kwargs)
            self.logger.debug('Finished "{}" execution with result: {}'.format(fn.__name__, str(fn_result)))
            return fn_result
        return new_fn
