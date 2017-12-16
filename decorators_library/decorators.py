from .exceptions import FunctionTimeoutException

import signal
import time

def inspect(op):
    def opx(*args, **kwargs):
        #result = x + y 
        args_ = ', '.join([str(arg) for arg in args])
        result = op(*args, **kwargs)
        if len(kwargs) == 0:
            print("{} invoked with {}. Result: {}".format(op.__name__,args_,result)) #  {}, {}. Result: {} , x, y, result))
        else:
            kwargs_ = ', '.join([value for key, value in kwargs.items()])    
            #print(kwargs_)
            print("{} invoked with {}, operation={}. Result: {}".format(op.__name__,args_,kwargs_,result)) #  {}, {}. Result: {} , x, y, result))
        #print(op(*args, **kwargs))    
        return op(*args, **kwargs)
    return opx
        


class count_calls(object):
    
    func_counter_dict = {}

    def __init__(self,original_function):
        self.original_function = original_function
        self.func_counter = 0
        count_calls.func_counter_dict[self.original_function.__name__] = self.func_counter
   
    def __call__(self):
        self.func_counter += 1
        print(self.original_function.__name__)
        count_calls.func_counter_dict[self.original_function.__name__] = self.func_counter
        return self.original_function()
    
    def counter(self):
        #print(self.original_function.__name__)
        return count_calls.func_counter_dict[self.original_function.__name__]
   
    @classmethod    
    def reset_counters(cls):
        count_calls.func_counter_dict = {} 
    
    @classmethod    
    def counters(cls):
        return count_calls.func_counter_dict


def timeout(max_time , exception = FunctionTimeoutException):  
    def receive_alarm(signum, stack):
        raise exception('Function call timed out')
        print('Alarm :', time.ctime())

    def wrapper(func):
        def func_wrapper(*args, **kwargs): 
            print(max_time)
            signal.signal(signal.SIGALRM, receive_alarm) 
            signal.alarm(max_time)
            t1 = time.time()
            try:
                result = func(*args, **kwargs)
            finally:
                signal.alarm(0)
            t2 = time.time() - t1
            #print('{} rans for {} secs'.format(func.__name__, t2))
            return result     
        return func_wrapper
    return wrapper    


class memoized(object):
    
    def __init__(self, func):
        self.func = func
        self.cache = {}
        #print('I am here')
   
    def __call__(self,x,y):
        if (x,y) in self.cache:
            print('{} was not executed for {} {} result was returned from internal cache'.format(self.func.__name__, x , y ))
            print(self.cache)
            return self.cache[(x,y)]
        else:
            self.cache[(x,y)] = self.func(x,y)
            print('{} was executed for {} {} result is {}'.format(self.func.__name__, x , y,self.func(x,y) ))
            #print('I am Here')
            return self.func(x,y)


import logging 

def debug(logger = None ):
    
    def wrapper(op):
        logger_ = logger
        if not logger_:
            logging.basicConfig(filename = 'example.log', level = logging.DEBUG)
            logger_ = logging.getLogger(op.__module__)
    
        def opx(x,y):
            #result = add(x,y)
            print('Executing "{}" with params: ({}, {}), {{}}'.format(op.__name__, x, y))
            logger_.debug('Executing "{}" with params: ({}, {}), {{}}'.format(op.__name__, x, y))
            result = op(x,y)
            logger_.debug('Finished "{}" execution with result: {}'.format(op.__name__, result))
            print('Finished "{}" execution with result: {}'.format(op.__name__, result))
            return op(x,y)
        return opx
    return wrapper    
@debug()
def my_add(a, b):
    return a + b

print(my_add(1, 2))
# #print(res)

#print(my_add.__name__)


