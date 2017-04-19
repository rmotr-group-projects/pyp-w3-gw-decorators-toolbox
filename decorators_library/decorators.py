import signal 
import logging

from collections import Counter

from .exceptions import TimeoutError


class timeout(object):

    def __init__(self, timeout):
        self.timeout = timeout
         
    def __call__(self,original_function):
        
        def handler(signum, frame):
            raise TimeoutError('Function call timed out')
        def new_function():
            signal.signal(signal.SIGALRM, handler)
            signal.alarm(self.timeout)
            result = original_function()
            signal.alarm(0)
            return result
        return new_function

    
class memoized(object):
    def __init__(self, original_function):
        self.cache = {}
        self.original_function = original_function
        
    def __call__(self, *args, **kwargs):
        if args in self.cache:
            return self.cache[args]
        result = self.original_function(*args, **kwargs)
        self.cache[args] = result
        return result

    
class debug(object):
    
    def __init__(self, logger=None):
        if not logger:
            logging.basicConfig()
            self.logger = logging.getLogger('tests.test_decorators')            
        else:
            self.logger = logger
    
    def __call__(self, original_function):
        def new_function(a, b):
            result = original_function(a, b)
            function_name = original_function.__name__
            first_msg = 'Executing "{}" with params: ({}, {})'.format(
                function_name, a, b) + ', {}'
            second_msg = 'Finished "{}" execution with result: {}'.format(
                function_name, result)
            self.logger.debug(first_msg)
            self.logger.debug(second_msg)
            return result
        return new_function

        
class count_calls(object):
    
    list_of_functions = Counter()
    
    def __init__(self, original_function):
        if original_function.__name__ not in count_calls.list_of_functions:
            count_calls.list_of_functions[original_function.__name__] = 0 
        self.original_function = original_function
        
    def __call__(self):
        count_calls.list_of_functions[self.original_function.__name__] += 1

        def new_function():
            return self.original_function()
        return self.original_function()
    
    def counter(self):
        return count_calls.list_of_functions[self.original_function.__name__]
    
    @classmethod
    def reset_counters(cls):
        count_calls.list_of_functions = Counter()
        
    @classmethod
    def counters(cls):
        return dict(count_calls.list_of_functions)
