import signal
import time
from decorators_library.exceptions import FunctionTimeoutException


class timeout(object):

    def __init__(self, time_limit, exception=FunctionTimeoutException):
        self.time_limit = time_limit
        self.exception = exception

    def raise_timeout_exception(self, signum, stack):
        raise self.exception('Function call timed out')

    def __call__(self, fn):
        def wrapper(*args, **kwargs):
            signal.signal(signal.SIGALRM, self.raise_timeout_exception)
            signal.alarm(self.time_limit)
            result = fn(*args, **kwargs)
            signal.alarm(0)
            return result
        return wrapper


class memoized(object):

    def __init__(self, fn):
        self.fn = fn
        self.cache = {}

    def __call__(self, *args):
        if args in self.cache:
            return self.cache[args]

        new_fn = self.fn(*args)
        self.cache[args] = new_fn
        return new_fn


class count_calls(object):

    function_counts = {}

    def __init__(self, fn):
        self.fn = fn
        count_calls.function_counts[self.fn.__name__] = 0

    def __call__(self, *args, **kwargs):
        self.increment_counter()
        return self.fn(*args, **kwargs)

    def increment_counter(self):
        count_calls.function_counts[self.fn.__name__] += 1

    def counter(self):
        return count_calls.function_counts[self.fn.__name__]

    @classmethod
    def counters(cls):
        return count_calls.function_counts

    @classmethod
    def reset_counters(cls):
        cls.function_counts = {}


def inspect(fn):
    def wrapper(*args, **kwargs):
        formatted_kwargs = []
        for key, value in kwargs.items():
            formatted_kwargs.append('{}={}'.format(key, value))
        all_args = list(args) + formatted_kwargs
        all_args = ', '.join(str(arg) for arg in all_args)
        result = fn(*args, **kwargs)
        print('{} invoked with {}. Result: {}'.format(fn.__name__, all_args,
                                                      result))
        return result
    return wrapper


def countdown(fn):
    def wrapper(*args, **kwargs):
        COUNTDOWN_SECONDS = 10
        for num in range(COUNTDOWN_SECONDS, 0, -1):
            print('{}'.format(num))
            time.sleep(1)
        return fn(*args, **kwargs)
    return wrapper


def timer(fn):
    def wrapper(*args, **kwargs):
        before_time = time.time()
        result = fn(*args, **kwargs)
        after_time = time.time()
        total_time = after_time - before_time
        print('Function took {} seconds to run.'
              .format(total_time))
        return result
    return wrapper
