import signal
from exceptions import FunctionTimeoutException

def inspect(func):
  def func_wrapper(*args, **kwargs):
    kwargs_str = ""
    for kw in kwargs.keys():
           kwargs_str = ", " + ( kw+'='+str( kwargs[kw] ) )
    arg_str = str(args)[1:-1] + kwargs_str
    print ("{} invoked with {}. Result: {}".format(func.__name__, arg_str, func(*args,**kwargs)))
    return func(*args,**kwargs)
  return func_wrapper  

class memoized(object):
  def __init__(self,func):
      self.func = func
      self.cache = {}

  def __call__(self,*args):
    if args in self.cache:
        return self.cache[args]
    result = self.func(*args)
    print ("Not using cached value")
    self.cache[args] = result
    return result
    return self.cache.keys(args)
    
class timeout(object):
  def __init__(self, time, exception=FunctionTimeoutException):
    self.time = time
    self.exception = exception

  def receive_alarm(self, signum, stack):
    raise self.exception('Function call timed out')

  def __call__(self, func):
    def new_fn(*args, **kwargs):
      signal.signal(signal.SIGALRM, self.receive_alarm)
      signal.alarm(self.time)
      result = func(*args, **kwargs)
      signal.alarm(0)
      return result
    return new_fn    