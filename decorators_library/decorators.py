# implement your decorators here.

#inspect
import logging
import signal
import time

from .exceptions import FunctionTimeoutException


def inspect(wrap):
    def inner(*args, **kwargs):
        
         if kwargs:
           args_str = ", ".join([str(g) for g in args] ) + ", "
         else:
           args_str = ", ".join([str(g) for g in args] )  
         kwargs_str = " ".join( ['='.join([str(j) for j in i]) for i in kwargs.items()])
     
         result=wrap( *args, **kwargs)
      
         print "{} invoked with {}{}. Result: {}".format(wrap.__name__, args_str, kwargs_str, result)
                                                       
         return result
    return inner
    
class timeout(object):
    def __init__(self, seconds, exception=FunctionTimeoutException):
      self.seconds=seconds
      self.exception=exception
       
    
    def __call__(self, func):
          
          def handle_timeout(signum, stack):
          
            raise self.exception('Function call timed out')
  
          def wrapper():
             signal.signal(signal.SIGALRM, handle_timeout)
             signal.alarm(self.seconds)
             func()
             signal.alarm(0)
             
          return wrapper



class count_calls(object):
    def __init__(self, function):
        self.function = function
        
        self.total_calls = 0

        count_calls.function_counter[function] = self

    function_counter = {}
    
    def __call__(self, *args):      #add to count when function called
        self.total_calls += 1
        return self.function(*args)

    def counter(self):              #create counter
        return count_calls.function_counter[self.function].total_calls

    @classmethod
    def counters(self):              #return items in counter in dictionary
        return dict(
            [(func.__name__, self.function_counter[func].total_calls)
                     for func in self.function_counter])

    @classmethod                    #reset to empty counter
    def reset_counters(self):
        self.function_counter = {}

class memoized(object):
    
    def __init__(self, f):  #setting up cache 
        self.f = f
        self.cache = {}
        
    def __call__(self, *args):   #identifying whether input is in cache already, per jason note 
        if args in self.cache:
            return self.cache[args]
        else:                  #add to cache 
            input = self.f(*args)     #using 'input' to reference the value that isn't already in cache
            self.cache[args] = input 
            return input 
 
class debug(object):
    
  def __init__(self, logger=None):
        self.logger=logger  
        
  message1= 'Executing "{}" with params: {}, {}'   
  message2= 'Finished "{}" execution with result: {}'     

  def __call__(self, func):
      
       # set logger if no logger was passed
        if not self.logger:
             self.logger=logging.getLogger('tests.test_decorators')
             self.logger.setLevel(logging.DEBUG)
             logging.basicConfig(level=logging.DEBUG, format='%(name)s:%(levelname)s:%(message)s:')
      
        def  wrap(*args, **kwargs):
            
            self.logger.debug(self.message1.format(func.__name__, args, kwargs))

            result = func(*args, **kwargs)

            self.logger.debug(self.message2.format(func.__name__,  result))

            return result

        return wrap
