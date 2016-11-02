import signal
import logging


# implement your decorators here.
class count_calls(object):
    """
    Keeps track of how many times certain function was called:
    """
    # dictionary to track count of all decorated functions
    _counters = {}

    def __init__(self, fn):
        self._counter = 0
        self.fn = fn
        count_calls._counters[self.fn.__name__] = 0

    def counter(self):
        return self._counter

    def __call__(self):
        self._counter += 1
        self._counters[self.fn.__name__] += 1
        return self.fn()

    @classmethod
    def counters(cls):
        return cls._counters

    @classmethod
    def reset_counters(cls):
        cls._counters = {}


class memoized(object):
    """
    This decorator should keep track of previous executions of the decorated
    function and the result of the invokations. If the decorated function is
    execution again using the same set of arguments sent in the past,
    the result must be immediately returned by an internal cache instead
    of re executing the same code again.
    """

    def __init__(self, fn):
        self.cache = {}
        self.fn = fn

    def __call__(self, *args):
        if args not in self.cache:
            self.cache[args] = self.fn(*args)
        return self.cache[args]


class timeout(object):
    """
    Useful to given functions a certain max time for execution.
    The decorator is suppose to track the execution time
    and raise and exception if the time exceeds given timeout range.
    """

    def __init__(self, secs):
        self.secs = secs

    def __call__(self, fn):
        def _handle_timeout(signum, frame):
            raise TimeoutError('Function call timed out')

        def wrapper(*args, **kwargs):
            signal.signal(signal.SIGALRM, _handle_timeout)
            signal.alarm(self.secs)
            return fn(*args, **kwargs)

        return wrapper


class debug(object):
    """
    This decorator is suppose to debug the executions of the decorated function
    by logging a message before starting the execution including given params,
    and a second message after the execution is finished
    with the returned result.
    """

    def __init__(self, logger=None):
        self.logger = logger

    def __call__(self, fn):
        def wrapper(*args, **kwargs):
            if not self.logger:
                self.logger = logging.getLogger(fn.__module__)
            self.logger.debug('Executing "{}" with params: {}, {}'
                              .format(fn.__name__, args, kwargs))
            self.logger.debug('Finished "{}" execution with result: {}'
                              .format(fn.__name__, fn(*args, **kwargs)))
            return fn(*args, **kwargs)

        return wrapper


def on_condition(decorator, condition):
    """
    This decorator will only decorate the function if the condition
    is met. Otherwise it will return the undecorated function.
    The idea is to use it with the other decorators to only decorate under
    certain condition. Condition could be a callable that returns true under
    certain events such as temperature sensors, alarm sensors, etc.
    """

    def wrapper(f):
        if not condition:
            return f
        return decorator(f)

    return wrapper


class html_wraps(object):
    """
    This decorator is suppose to debug the executions of the decorated function
    by logging a message before starting the execution including given params,
    and a second message after the execution is finished
    with the returned result.
    """

    TEMPLATE = """
    <!doctype html>
    <html lang="en">
        <head>
        <meta charset="utf-8">
        <title></title>
        </head>
        <body>\n{}\n</body>
    </html>
    """

    def __init__(self, template=None):
        self.template = template if template else self.TEMPLATE

    def __call__(self, fn):
        def wrapper(*args, **kwargs):
            return self.template.format(fn(*args, **kwargs))
        return wrapper
