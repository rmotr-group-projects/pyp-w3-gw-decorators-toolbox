# implement your decorators here.
# implement your decorators here.
from functools import wraps
import errno
import os
import signal
import logging

#memoized decorator
def memoized(f):
    def new_func(*args, **kwargs):
        
        new_func.cache_result = {}
        
        if not hasattr(new_func, "cache"):
            setattr(new_func, "cache", new_func.cache_result)
        
        #if args in new_func.cache_result:
        new_func.cache_result[args] = f(*args, **kwargs)
        return f(*args, **kwargs)
    return new_func

  #if args in cache:
   #         return cache[args]
    #    else:
     #        cache[args] =  f(*args, **kwargs)
      #       return  f(*args, **kwargs)
#class Add:
#    def __init__(self, *args):
#       self.properties = args
#       self.cache ={}
#    
#    def add(self, args):
#        return sum(args)


## from stackoverflow , trying to understand it

#timeout decorator
class TimeoutError(Exception):
    pass

def timeout(seconds=10, error_message=os.strerror(errno.ETIME)):
    def decorator(func):
        def _handle_timeout(signum, frame):
            raise TimeoutError(error_message)

        def wrapper(*args, **kwargs):
            signal.signal(signal.SIGALRM, _handle_timeout)
            signal.alarm(seconds)
            try:
                result = func(*args, **kwargs)
            finally:
                signal.alarm(0)
            return result

        return wraps(func)(wrapper)

    return decorator

#debug decorator



#count_calls decorator 
class Count_calls:
    def __init__(self, func):
        self.properties = {}
        self.properties[func] = func
        self.properties['count'] = 0
    def func(self):
        print("I am running the func")
        self.properties['count'] += 1
    
    @property
    def count(self):
        return self.properties.get('count')
    @count.setter
    def count(self,c):
        self.properties['count'] = c
    @count.deleter
    def count(self):
        del self.properties['count']
    


