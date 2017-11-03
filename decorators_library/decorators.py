# implement your decorators here.
def timeout():
    pass


def memoized():
    pass


class count_calls(object):

    function_counts = {}

    def __init__(self, fn):
        self.fn = fn
        self.count = 0
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
        return fn(*args, **kwargs)
    return wrapper
