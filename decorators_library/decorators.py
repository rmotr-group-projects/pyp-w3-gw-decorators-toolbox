import signal   # Used in timeout()
import logging # used in debug
import time # Used in cushion
from threading import Thread # Used in cushion
import os # used for no_print decorator
import sys # used for no_print decorator
from .exceptions import TimeoutError  # Used in timeout()

import itertools  #just used for testing

def timeout(limit):
    '''
    Creates and returns a decorator that operates using the time constraint
    defined in *limit*.
    Code was janked from http://goo.gl/4RYmJk, but was inspected and understood.
    '''
    def limit_decorator(f):
        '''
        Adds a timeout feature to function *f* and returns the decorated
        function.
        '''
        def _handle_timeout(sig_num, stack_frame):
            # Called by signal.signal() if a signal.SIGALRM is sent
            raise TimeoutError('Function call timed out')
            
        def g(*args, **kwargs):
            '''
            Returns results of f(*args, **kwargs), if the time limit is not
            exceeded.
            
            https://docs.python.org/3/library/signal.html#signal.signal
            '''
            # Set _handle_timeout as the handler for any signal.SIGALRM
            #  signal that is received
            signal.signal(signal.SIGALRM, _handle_timeout)
            
            # Set an alarm that will send a signal.SIGALRM signal after
            #  the number of seconds defined by *limit*
            signal.alarm(limit)
            
            # Run *f* and store its return value in *result*, if *f*
            #  completes before the alarm signal is sent.
            try:
                result = f(*args, **kwargs)
            
            # Cancel the alarm
            finally:
                signal.alarm(0)
                
            return result
        
        return g
    
    return limit_decorator
    
def debug(logger = None):
    '''
    Uses logging module to log the parameters passed in before a function is executed
    and then the result after the function is executed
    debug takes in an optional argument which is a custom logger
    
    decorating example:
    @debug()
    def my_add(a,b):
    
    is equivalent to:
    my_add = debug()(my_add)
    which is:
    my_add = debug_decorator(my_add)
    which is:
    my_add = debug_function
    
    so calling my_add(2,3) is really calling debug_function(2,3)
    
    The capture.check checks 3 fields of the logger:
        (ROOT, INFO, MSG)
        ROOT = The module that called it, for example 'test.test_decorators'
        INFO = 'DEBUG'
        MSG will be set by logging.debug(message)
    '''
 
    def debug_decorator(f):
        # need to create a local copy of logger
        # otherwise there are issues with it being out of scope here
        local_logger = logger
        
        if not local_logger:
            # if no custom logger was passed in then set the ROOT to
            # be the module of the function that we are decorating
            local_logger = logging.getLogger(f.__module__)
            
        def debug_function(*args, **kwargs):
            # args read in as tuple, kwargs as dict
            message = 'Executing "{}" with params: {}, {}'.format(
                f.__name__, args, kwargs)
            local_logger.debug(message)
            
            result = f(*args, **kwargs)
            
            message = 'Finished "{}" execution with result: {}'.format(
                f.__name__, result)
            local_logger.debug(message)
            return result
        return debug_function
    return debug_decorator

class count_calls(object):
    '''
    Decorator class that counts and records the number of calls to a function. 
    '''
    
    count = {}
    
    def __init__(self,f):
        self.f = f
        count_calls.count[self.f.__name__] = 0
    
    def __call__(self):
        count_calls.count[self.f.__name__] += 1
        self.f()
    
    def counter(self):
        '''
        Returns the number of times the function has been called.
        '''
        return count_calls.count[self.f.__name__]
    
    @classmethod
    def counters(cls):
        '''
        Returns a dictionary of {function:call_count} pairs
        '''
        return cls.count
    
    @classmethod
    def reset_counters(cls):
        cls.count = {}


class memoized(object):
    '''
    A decorator class that will cache function results every time a function
    is called, and return the cached results if the function is called again.
    '''
    def __init__(self, f):
        self.f = f
        self.cache = {}
    
    def __call__(self, *args):
        if args not in self.cache:
            self.cache[args] = self.f(*args)
        return self.cache[args]


class cushion(object):
    '''
    Uses threads to run function calls with a time cushion between them. If
    too many function calls are queued up, the cushion will raise an exception 
    (or optionally, the function call will be ignored).
    A cushioned function will always return None.
    
    *time_buffer* is the minimum amount of time in seconds between function
    calls.
    
    *max_queue* is the maximum number of function calls that can be in queue
    before an exception is raised.
    
    *drop* is whether function calls in excess of the maximum will be dropped
    instead of raising an exception.
    '''
    # Class attributes
    time_buffer = {}
    max_wait = {}
    drop = {}
    next_call = {}
    
    def __new__(cls, time_buffer=5, max_queue=3, drop=False):
        
        # Verify that valid values were passed for time_buffer and max_queue
        if time_buffer < 0:
            raise ValueError('Time buffer cannot be negative')
        
        if max_queue < 0:
            raise ValueError('Maximum queue size cannot be negative')
        
        def wrapper(f):
            
            # Set class attributes for the wrapped function
            f_name = f.__name__
            cls.time_buffer[f_name] = time_buffer
            cls.max_wait[f_name] = (max_queue + 1) * time_buffer
            cls.drop[f_name] = drop
            cls.next_call[f_name] = time.time() - time_buffer
            
            def check(*args, **kwargs):
                '''
                Verify that a new call to the wrapped function can be made. 
                Start a new thread to call *g* after a time cushion has passed.
                Using a new thread allows the main thread to continue execution
                before *g* finishes executing.
                Since *g* is run in a new thread, this will not return
                any value that *g* may return.
                '''
                # Determine how long to wait before calling the function
                now = time.time()
                wait = max(now, cls.next_call[f_name]) - now
                
                # If the wait has grown too large, either skip the function
                #  call, or raise an exception
                if wait > cls.max_wait[f_name]:
                    if cls.drop[f_name]:
                        return
                    raise RuntimeError('function call limit exceeded')
                
                # Set the cushion between this call and the next allowable one
                cls.next_call[f_name] = (
                    max(now, cls.next_call[f_name]) + cls.time_buffer[f_name]
                )
                
                # Set the time for this call, and start a new thread to run it
                new_args = args + (wait,)
                t = Thread(target=g, args=new_args, kwargs=kwargs)
                t.start()
            
            def g(*new_args, **kwargs):
                '''
                Execute *f* after a time cushion
                '''
                time.sleep(new_args[-1])
                args = new_args[:-1]
                f(*args, **kwargs)
            
            return check
        
        return wrapper

 
def no_print(f):
    '''
    Decorator that will prevent a function from printing anything to stdout
    stdout will be redirected to devnull
    '''
    
    def new_f(*args, **kwargs):
        old_stdout = sys.stdout # save current stdout to reset it later
        sys.stdout = open(os.devnull, 'w') # file path of the null device
        try:
            return f(*args, **kwargs) 
        finally:
            # finally will be executed even if the try/return succeeds
            # reset the stdout to what it was before
            sys.stdout.close()
            sys.stdout = old_stdout
    return new_f