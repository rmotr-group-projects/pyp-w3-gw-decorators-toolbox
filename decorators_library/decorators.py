import timeit
import time
import functools
from random import randint
import datetime
from .exceptions import FunctionTimeoutException
import signal
#from exceptions import FunctionTimeoutException

# implement your decorators here.

def inspect(func):
    @functools.wraps(func)
    def inspected(*args, **kwargs):
        result = func(*args, **kwargs)
        arg_str = ''.join(repr(arg) for arg in args)
        kwg_str =''.join(repr(kwg) for kwg in kwargs)
        func_name = func.__name__
        if kwargs:
            for key, value in kwargs.items():
                kwargs_holder = ("{}={}".format(key,value))
                print('{} invoked with {}, {}, {}. Result: {}'.format(func_name,arg_str[0], arg_str[1],kwargs_holder, result))
        else:
            print('{} invoked with {}, {}. Result: {}'.format(func_name,arg_str[0], arg_str[1], result))
        return result
    return inspected

@inspect    
def my_add(a, b):
    return a + b

class timeout(object):
    
    def __init__(self, max_time, exception=FunctionTimeoutException):
        self.max_time = max_time
        self.exception = exception
    
    def _handle_timeout(self,signum, frame):
        raise self.exception('Function call timed out')
    
    def __call__(self, func):
        def timer(*args, **kwargs):
            signal.signal(signal.SIGALRM, self._handle_timeout)
            signal.alarm(self.max_time)
            try:
                result = func(*args, **kwargs)
            finally:
                signal.alarm(0)
            return result

        return timer
    
@timeout(1)
def very_slow_function():
    time.sleep(3)
    
    
def debug(func):
    @functools.wraps(func)
    def debugger(*args, **kwargs):
        #Executing "my_add" with params: (1, 2), {}
        arg_str = ''.join(repr(arg) for arg in args)
        func_name = func.__name__
        print('Executing "{}" with params: ({}, {})'.format(func_name, arg_str[0], arg_str[1]))
        result = func(*args)
        #Finished "my_add" execution with result: 3
        print('Finished "{}" execution with result: {}'.format(func_name, result))
        return result
    return debugger

@debug
def my_add2(a, b):
    return a + b

class count_calls(object):
    
    def __init__(self, func):
        self.func = func
    
    count = 0
    counters_dict = {}

    @classmethod
    def counters(cls):
        if cls.counters_dict == {}:
            cls.counters_dict['my_func'] = 0
            return cls.counters_dict
        else:
            return cls.counters_dict

    @classmethod
    def reset_counters(cls):
        cls._reset_counter()
        cls._reset_counters_dict()
    @classmethod
    def _reset_counter(cls):
        cls.count = 0
        return cls.count
    @classmethod
    def _reset_counters_dict(cls):
        cls.counters_dict = {}
        return cls.counters_dict
    
    def counter(self):
        return self.count
        
    def __call__(self):
        self.count += 1
        result = self.func()
        self.counters_dict[self.func.__name__] = self.count
        return result
        

@count_calls
def my_func():
    pass

def memoized(func):
    
    cache = {}
    
    @functools.wraps(func)
    def wrapper(*args):
        if args not in cache:
            cache[args] = func(*args)
        wrapper.cache = cache
        return cache[args]
    return wrapper
    
@memoized
def add(a, b):
    return a + b



class trade_log(object):
    
    def __init__(self, func):
        self.func = func
    
    trade_dict = {}
    
    @classmethod
    def position(cls):
        return cls.trade_dict
    @classmethod
    def net_long_short(cls):
        net_position = 0
        for k, v in cls.trade_dict.items():
            net_position += v['Size']
        return net_position

    def strategy_position(self): 
        strategy_position_dict = {}
        strategy_position = 0
        for k,v in self.trade_dict.items():
            if v['Strategy'] == self.func.__name__:
                strategy_position += v['Size']
                strategy_position_dict[v['Strategy']] = strategy_position
        return strategy_position_dict
        
    def __call__(self, *args, **kwargs):
        time = datetime.datetime.now()
        position = self.func(*args, **kwargs)
        position['Strategy'] = self.func.__name__
        self.trade_dict[time] = position
        return self.func(*args)


@trade_log
def strategy_one(a, rand_int=randint(0,9)):
    if rand_int > a:
        position = 'Buy'
    else:
        position = 'Sell'
        a = -a
    trade_handler = {
        'Direction' : position,
        'Size' : a
    }
    
    return trade_handler

@trade_log
def strategy_two(a, rand_int=randint(0,9)):
    if rand_int > a:
        position = 'Buy'
    else:
        position = 'Sell'
        a = -a
    trade_handler = {
        'Direction' : position,
        'Size' : a
    }
    return trade_handler


#Event holder is a cache to hold 
class event_processor(object):
    def __init__(self, look_back = 5):
        self.look_back = look_back
        self.look_back_window = []
    
    def cut_look_back(self):
        if len(self.look_back_window) > self.look_back:
            self.look_back_window = self.look_back_window[:self.look_back]
        return self.look_back_window
    
    def __call__(self, func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            self.look_back_window.insert(0,result)
            self.cut_look_back()
            price_holder = 0
            for price in self.look_back_window:
                price_holder += price['price']
            return price_holder / len(self.look_back_window)
        return wrapper
        
    
@event_processor(look_back=10)
def event(price, volume):
    return_dict = {
        'price' : price,
        'volume' : volume,
    }
    return return_dict
