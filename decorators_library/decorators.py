# implement your decorators here.
# implement your decorators here.
from .exceptions import FunctionTimeoutException 
def inspect(op):
  def wrapper(*args, **kwargs):
    arg_res = str(args)[1:-1]
    dic_res = ''
    for key, value in kwargs.iteritems():
      dic_res += str(key) + '=' + str(value)
    if 'operation' in dic_res:
      print('{} invoked with {}, {}. Result: {}'.format(op.__name__, arg_res, dic_res, op(*args, **kwargs)))
    else:
      print('{} invoked with {}. Result: {}'.format(op.__name__, arg_res, op(*args, **kwargs)))
    return op(*args, **kwargs)
  return wrapper
    
import signal
#timeout decorator

def timeout(t, exception=FunctionTimeoutException):
  secs = t
  def time_decorator(op):
    import time 
  
    def wrapper(*args, **kwargs):
      def receive_alarm(signum, stack):
        raise exception('Function call timed out')
    
      signal.signal(signal.SIGALRM, receive_alarm)
      signal.alarm(secs)
      op(*args, **kwargs)
      signal.alarm(0)
    return wrapper
  return time_decorator
  
class count_calls(object):
  CALL_HISTORY = {}
  def __init__(self, func):
    self.func = func
    self.CALL_HISTORY[self.func.__name__] = 0
    
  def __call__(self, *args, **kwargs):
    self.CALL_HISTORY[self.func.__name__] += 1
    return self.func(*args, **kwargs)
    
  def counter(self):
    return self.CALL_HISTORY[self.func.__name__]
  
  @classmethod
  def counters(cls):
    return cls.CALL_HISTORY
    
  @classmethod
  def reset_counters(cls):
    cls.CALL_HISTORY = {}
    
class memoized(object):
  cache = {}
  def __init__(self, func):
    self.func = func
  def __call__(self, x, y):
    if tuple((x, y)) in self.cache:
      return self.cache[tuple((x, y))]
    else:
      self.cache[tuple((x, y))] = self.func(x, y)
      return self.func(x, y)