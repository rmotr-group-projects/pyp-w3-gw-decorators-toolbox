import time
from functools import wraps
from decorators_library.exceptions import FunctionTimeoutException

# class FunctionTimeoutException(Exception):
#     pass


def inspect(org_fun):
    def wrapper(*args):
        s = ','.join([str(a) for a in args])
        return "{} invoked with {} Result: {}".format(org_fun.__name__, s, org_fun(*args))
    return wrapper
    
# @inspect
# def my_add(a, b):
#     return a + b

# print(my_add(3, 5))  # 8
# Printed: "my_add invoked with 3, 5. Result: 8"





def timeout(time_limit, exception = FunctionTimeoutException, error_message='Function call timed out'):
    def real_decorator(org_fun):
        @wraps(org_fun)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            org_fun(*args, **kwargs)
            elapsed_time = time.time() + start_time
            if elapsed_time > time_limit:
                raise FunctionTimeoutException(error_message)
            return 
        return wrapper
    return real_decorator

# @timeout(1)
# def very_slow_function():
#     time.sleep(2)
# very_slow_function()
# FunctionTimeoutException: Function call timed out

# class MyVeryCoolException(Exception):
#     pass

# @timeout(1, exception=MyVeryCoolException, error_message='????')
# def very_slow_function():
#     time.sleep(2)

# very_slow_function()




class debug(object):
    def __init__(self):
        pass

    def __call__(self, org_fun):
        @wraps(org_fun)
        def wrapper(*args, **kwargs):
            print("Executing '{}' with params: {} {}".format(org_fun.__name__, args, kwargs))
            result = org_fun(*args, **kwargs)
            print("Finished '{}' execution with result: {}".format(org_fun.__name__, result))
            return
        return wrapper


# @debug()
# def my_add(a, b):
#     return a + b

# my_add(1, 2)
# Executing "my_add" with params: (1, 2), {}
# Finished "my_add" execution with result: 3



class count_calls(object):
    FUNCTION_COUNTERS = {}

    def __init__(self, org_fun):
        self.org_fun = org_fun
        self.num_of_calls = 0
        count_calls.FUNCTION_COUNTERS[org_fun] = self

    def __call__(self):
        self.num_of_calls += 1        
        @wraps
        def wrapper(*args, **kwargs):
            result = self.org_fun(*args, **kwargs)
            return result
        return wrapper        

    def counter(self):
        return self.num_of_calls

    @classmethod
    def counters(cls):
        return dict([(f.__name__, cls.FUNCTION_COUNTERS[f].num_of_calls) for f in cls.FUNCTION_COUNTERS])


# @count_calls
# def my_func():
#   pass

# my_func()
# my_func()
# my_func()
# my_func()
# print(my_func.counter())
# 4



class memoized(object):

    def __init__(self, org_fun):
        self.org_fun = org_fun
        self.cache = {}

    def __call__(self, *args):
        if args in self.cache:
            return self.cache[args]
        else:
            value = self.org_fun(*args)
            self.cache[args] = value
            return value


# @memoized
# def add(a, b):
#     return a + b

# print(add(1, 2))
#3
# print(add(2, 3))
# 5
# print(add(1, 2))
# 3  # `add` was not executed, result was returned from internal cache