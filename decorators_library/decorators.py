# implement your decorators here.
# import signal
# from decorators_library.exceptions import FunctionTimeoutException


# def inspect(fn):

#     if fn.__name__ == 'my_add':

#         def decorated_fn(x, y):

#             print("my_add invoked with {}, {}. Result: {}".format(x, y, fn(x, y)))
#             return fn(x, y)

#         return decorated_fn

#     elif fn.__name__ == 'calculate':

#         def decorated_fn(*args, operation='add'):

#             inputs = ", ".join(str(x) for x in args)

#             if operation == "add":

#                 print("calculate invoked with {}. Result: {}".format(inputs, fn(*args, operation)))
#                 return fn(*args, operation)

#             else:

#                 print("calculate invoked with {}, operation={}. Result: {}".format(inputs, operation, fn(*args, operation='subtract')))

#                 return fn(*args, operation)

#         return decorated_fn


# def timeout(sec, my_exception=FunctionTimeoutException):

#     def receive_alarm(signum, stack):
#         """Raise a timed out exception"""
#         raise my_exception('Function call timed out')

#     def timeout_sec(fn):

#         def decorated_fn():

#             signal.signal(signal.SIGALRM, receive_alarm)
#             signal.alarm(sec)

#             fn()

#         return decorated_fn

#     return timeout_sec


class count_calls(object):

    counters_record = {}

    def __init__(self, fn):
        """what exactly is self here ???"""
        self.fn = fn
        self.call_count = 0
        self.counters_record[fn] = self

    def __call__(self):
        self.call_count += 1
        return self.fn()

    def counter(self):
        """Return current count for self"""
        return count_calls.counters_record[self.fn].call_count

    # Class methods are methods that are not bound to an object, but to a class.
    # Do not need to initialize an instance of this class to use these methods
    @classmethod
    def counters(cls):
        return dict((key.__name__, value.call_count) for key, value in cls.counters_record.items())

    @classmethod
    def reset_counters(cls):
        cls.counters_record = {}


class memoized(object):

    previous_arguments = {}

    def __init__(self, fn):
        self.fn = fn

    def __call__(self, a, b):
        """Make class callable as a function"""

        prev_arg = memoized.previous_arguments

        if (a, b) in prev_arg:
            return prev_arg[(a, b)]

        else:

            prev_arg[(a, b)] = self.fn(a, b)

        return self.fn(a, b)

    @property
    def cache(self):
        return memoized.previous_arguments


# TESTING:

# @memoized
# # add = memoized(add)
# def add(a, b):
#     return a + b

# print(add.cache)
# print(dir(add))
# print(add(1, 2))
# print(add(3, 2))
# print(add(1, 2))
# print(add.cache)
# # print(add.cache)

# ====== OTHER DECORATORS TO IMPLEMENT ======
# def debug():
#     pass
