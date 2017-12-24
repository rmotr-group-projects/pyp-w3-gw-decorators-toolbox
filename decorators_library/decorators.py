import functools
import collections

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

def timeout():
    pass