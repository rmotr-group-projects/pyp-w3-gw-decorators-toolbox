# Hint 1 - Decorator that receives arguments

`timeout`, `debug` are both decorators that receive arguments. An easy way to implement that with Python is through a _"Class Decorator"_. Example related to yesterday's class:

```python
class only_num_arguments(object):
    def __init__(self, ints=True, floats=True):
        self.ints = ints
        self.floats = floats

    def __call__(self, function):
        def wrapped(x, y):
            if not self.floats and any([type(x) == float for x in [x, y]]):
                raise ValueError("Floats not allowed")
            if not self.ints and any([type(x) == int for x in [x, y]]):
                raise ValueError("Ints not allowed")
            return function(x, y)
        return wrapped


@only_num_arguments(floats=False)
def add(x, y):
    return x + y
```

In this case, when `@only_num_arguments(floats=False)` is ran, we're **creating an only_num_arguments** instance. The `__init__` method is executed passing `floats=False`. When the **decorated** function `add` is invoked, the `__call__` method is actually invoked.

[https://repl.it/GFP1](https://repl.it/GFP1)
