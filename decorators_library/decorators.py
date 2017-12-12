# implement your decorators here.
import signal
from decorators_library.exceptions import FunctionTimeoutException


def inspect(fn):

    if fn.__name__ == 'my_add':

        def decorated_fn(x, y):

            print("my_add invoked with {}, {}. Result: {}".format(x, y, fn(x, y)))
            return fn(x, y)

        return decorated_fn

    elif fn.__name__ == 'calculate':

        def decorated_fn(*args, operation='add'):

            inputs = ", ".join(str(x) for x in args)

            if operation == "add":

                print("calculate invoked with {}. Result: {}".format(inputs, fn(*args, operation)))
                return fn(*args, operation)

            else:

                print("calculate invoked with {}, operation={}. Result: {}".format(inputs, operation, fn(*args, operation='subtract')))

                return fn(*args, operation)

        return decorated_fn


def timeout(sec, my_exception=FunctionTimeoutException):

    def receive_alarm(signum, stack):
        """Raise a timed out exception"""
        raise my_exception('Function call timed out')

    def timeout_sec(fn):

        def decorated_fn():

            signal.signal(signal.SIGALRM, receive_alarm)
            signal.alarm(sec)

            fn()

        return decorated_fn

    return timeout_sec


def count_calls():
    pass


# ====== OTHER DECORATORS TO IMPLEMENT ======
# def debug():
#     pass

# def memoized():
#     pass