from functools import wraps
from decorators_library.exceptions import FunctionTimeoutException
import signal


def inspect(fn):
    @wraps(fn)
    def new_fn(*args, **kwargs):
        kwarg_lst = tuple('{}={}'.format(key, val) for key, val in kwargs.items())
        arg_str = ', '.join(map(str,args  + kwarg_lst))
        fn_result = fn(*args, **kwargs)
        
        print('{} invoked with {}. Result: {}'.format(fn.__name__, arg_str, str(fn_result)))
        return fn_result
    return new_fn

class timeout(object):
    def __init__(self, duration, exception=FunctionTimeoutException):
        self.duration = duration
        self.exception = exception
    
    def raise_alarm(self, signum, stack):
        raise self.exception("Function call timed out")

    def __call__(self, fn):
        @wraps(fn)
        def wrapped(*args, **kwargs):
            signal.signal(signal.SIGALRM, self.raise_alarm)
            signal.alarm(self.duration)
            return fn(*args, **kwargs)
        signal.alarm(0)
        return wrapped

class debug(object):
  def __init__(self):
    pass
  
  def __call__(self, fn):
    @wraps(fn)
    def new_fn(*args, **kwargs):
      kwarg_lst = ', '.join(['{}={}'.format(key, val) for key, val in kwargs.items()])
      arg_str = ', '.join(map(str,args))
        
      print('Executing "{}" with params: ({}), {{{}}}'.format(fn.__name__, arg_str, kwarg_lst))
      fn_result = fn(*args, **kwargs)
      print('Finished "{}" execution with result: {}'.format(fn.__name__, str(fn_result)))
      return fn_result
    return new_fn

class count_calls(object):
  FN_CALLS = {}
  
  def __init__(self, fn):
    self.fn = fn
    self.FN_CALLS[self.fn.__name__] = 0
  
  def __call__(self, *args, **kwargs):
    self.FN_CALLS[self.fn.__name__] += 1
    return self.fn(*args, **kwargs)
  
  def counter(self):
    return self.FN_CALLS[self.fn.__name__]
  
  @classmethod
  def counters(cls):
    return cls.FN_CALLS
  
  @classmethod
  def reset_counters(cls):
    cls.FN_CALLS = {}
    

def memoized(fn):
  cache = {}
  
  @wraps(fn)
  def new_fn(*args, **kwargs):
    if args in cache:
      return cache[args]
    else:
      fn_result = fn(*args, **kwargs)
      cache[args] = fn_result
      return fn_result
  
  new_fn.cache = cache
  return new_fn