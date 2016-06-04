from decorators_library.exceptions import *
from functools import wraps
import signal 


def timeout(seconds=10, error_message='Function call timed out'):
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
    
def debug(func):
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        print('Executing {} with params: {}'.format(func.__name__, args)) 
        # Need to add {} at the very end. dunno what those are for yet
        result = func(*args, **kwargs)
        print('Finished "{}" execution with result: {}'.format(func.__name__, result))
        return result
    return wrapper