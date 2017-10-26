from functools import wraps
from decorators_library.exceptions import FunctionTimeoutException
import signal

def inspect(fn):
    @wraps(fn)
    def new_fn(*args, **kwargs):
        kwarg_lst = tuple('{}={}'.format(key, val) for key, val in kwargs.items())
        arg_str = ', '.join(map(str,args  + kwarg_lst))
        
        print('{} invoked with {}. Result: {}'.format(fn.__name__, arg_str, str(fn(*args, **kwargs))))
        return fn(*args, **kwargs)
    return new_fn

class timeout(object):
    def __init__(self, duration, exception=FunctionTimeoutException):
        self.duration = duration
        self.exception = exception
    
    def raise_alarm(self, signum, stack):
        raise self.exception("Function call timed out")

    def __call__(self, fn):
        def wrapped(*args, **kwargs):
            signal.signal(signal.SIGALRM, self.raise_alarm)
            signal.alarm(self.duration)
            return fn(*args, **kwargs)
        return wrapped

def debug(fn):
    pass

def count_calls(fn):
    pass

def memoized(fn):
    pass