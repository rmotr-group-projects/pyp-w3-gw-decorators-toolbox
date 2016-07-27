# implement your decorators here.
from time import sleep
import time
import signal

from decorators_library.exceptions import TimeoutError


def timeout(max_time):
    def decorate(func):
        def handler(signum, frame):
            # print("Here")
            raise TimeoutError()
            
        def new_f(*args, **kwargs):
            signal.signal(signal.SIGALRM, handler)
            signal.alarm(max_time)
            
            try:
                result = func(*args, **kwargs)
            finally:
                signal.alarm(0)
            return result
        new_f.func_name = func.func_name
        return new_f
    return decorate

class count_calls(object):
    def __init__(self, f):
        # self.counter = 0
        self.f = f
        self.dic = {}
        
        # {foo : 0, foo1 : 0}
    def __call__(self, *args, **kwargs):
        def wrapper(args, kwargs):
    key = "".join([function.__name__,".".join([str(i) for i in args])])
            if self.f.__name__ in self.dic:
                self.dic[self.f.__name__] += 1
                # self.counter += 1
            else:
                self.dic[self.f.__name__] = 1
                # self.dic + {self.f.__name__ : 1}
            return self.f(*args, **kwargs)
        # wrapper.counter = 0
        wrapper.__name__ = self.f.__name__
        print(self.dic)
        
    def counter(self):
        print ("HERE")
        return self.dic[self]
        
        
    
class debug():
    pass

 
class memoized(object):
    def __init__(self, f):
        self.cache = {}
        self.f = f
    
    def __call__(self, *args):
        #print('cache =',self.cache)
        key = args
        if key in self.cache:
            return self.cache[key]
        else:
            result = self.f(*args)
            self.cache[key] = result
            return result
        
   
        
'''
def func(arg1, arg2, namedarg=name1, namedarg=name2):
    args = [arg1, arg2]
    kwargs {namedarg1: name1,
            namedarg2: name2}
    args = [func2]

class wrapper(object):
    def __init__(self, func):
        self.func = func
    
    def __call__(self, *args, **kwargs):
        do something here
        result = self.func(*args, **kwargs)
        do something else
        return some kind of output


'''