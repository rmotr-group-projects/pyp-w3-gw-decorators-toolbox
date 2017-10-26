# implement your decorators here.
from functools import wraps

def inspect(fn):
    @wraps(fn)
    def new_fn(*args, **kwargs):
        kwarg_lst = tuple('{}={}'.format(key, val) for key, val in kwargs.items())
        arg_str = ', '.join(map(str,args  + kwarg_lst))
        
        print('{} invoked with {}. Result: {}'.format(fn.__name__, arg_str, str(fn(*args, **kwargs))))
        return fn(*args, **kwargs)
    return new_fn

def timeout(fn):
    pass

def debug(fn):
    pass

def count_calls(fn):
    pass

def memoized(fn):
    pass