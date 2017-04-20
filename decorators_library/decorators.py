import signal
from .exceptions import TimeoutError
from functools import wraps
import logging
import os


# implement your decorators here.
class count_calls(object):
    cls_counter = {}

    def __init__(self, func):
        self.func = func
        self.count = 0
        count_calls.cls_counter[func.__name__] = 0

    def __call__(self, *args, **kwargs):
        self.count += 1
        count_calls.cls_counter[self.func.__name__] = self.count
        return self.func(*args, **kwargs)

    def counter(self):
        return self.count

    @classmethod
    def counters(cls):
        return cls.cls_counter

    @classmethod
    def reset_counters(cls):
        cls.cls_counter.clear()


class memoized(object):
    def __init__(self, func):
        self.func = func
        self.cache = {}

    def __call__(self, *args):
        if args in self.cache:
            return self.cache[args]
        else:
            value = self.func(*args)
            self.cache[args] = value
            return value


def timeout(seconds=10):
    "Simple decorator to stop after certain time"

    def decorator(func):

        def wrapper(*args, **kwargs):
            signal.signal(signal.SIGALRM, signal_handler)
            signal.alarm(seconds)
            try:
                result = func(*args, **kwargs)
            finally:
                signal.alarm(0)
            return result

        return wrapper

    return decorator


def signal_handler(signum, frame):
    raise TimeoutError("Function call timed out.")


def debug(logger=None):
    log = logger

    def real_dec(function):
        if not log:
            logger = logging.getLogger(function.__module__)
        else:
            logger = log

        def wrapper(*args, **kwargs):
            return_val = function(*args, **kwargs)
            logger.debug('Executing "{}" with params: {}, {{}}'.format(function.__name__, \
                                                                       tuple(args)))
            logger.debug('Finished "{}" execution with result: {}'.format(function.__name__, \
                                                                          return_val))
            return return_val

        return wrapper

    return real_dec


def store_to_file(file_name='myData', default_folder='DataFolder'):
    '''decorator that stores the result of a function in file'''
    def real_dec(func):

        def decorator(*args,**kwargs):
            result=func(*args, **kwargs)
            if not os.path.isdir(default_folder):
                os.mkdir(default_folder)
            if not os.path.isfile(default_folder + '/' + file_name):
                fout = open(os.getcwd()+ '/' + default_folder+ '/' + file_name, 'wt')
                fout.write(str(result))
            else:
                fout = open(os.getcwd()+ '/' +default_folder+ '/' + file_name, 'at')
                fout.write(' ' + str(result))
            fout.close()
            return result

        return decorator

    return real_dec

def word_frequency(word):
    '''counts the frequency of the given word if the function returns string'''
    def real_dec(func):

        def dec(*args, **kwargs):
            result = func(*args, **kwargs)
            count = 0
            if type(result)==str:
                result = result.split(' ')
            else:
                return result
            for x in result:
                if word.lower() == x.lower():
                    count += 1
            string = 'The word {} is found {} times in the result of {} function'.format(word, count, func.__name__)
            return string

        return dec

    return real_dec










