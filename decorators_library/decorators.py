# implement your decorators here.
def timeout():
    pass


class memoized():
    
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
        return fn(*args, **kwargs)
    return wrapper
