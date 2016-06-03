# [pyp-w3] Decorators Library

Today we will work with `decorators`. This project aims to be a library of useful, multi purpose decorators.

We provide an initial set of decorators you must implement, with all their proper test cases, but the interesting thing about this project is that you must also use your imagination and creativity to implement new decorators out of the initial set we provide. Of course, all the new decorators must come with their own set of test cases.

## Decorators provided

This is the initial set of decorators you must implement:


### `timeout` decorator

Useful to given functions a certain max time for execution. The decorator is suppose to track the execution time and raise and exception if the time exceeds given timeout range. Example:

```python
@timeout(1)
def very_slow_function():
    time.sleep(2)

>>> very_slow_function()
TimeoutError: Function call timed out
```

### `debug` decorator

This decorator is suppose to debug the executions of the decorated function by logging a message before starting the execution including given params, and a second message after the execution is finished with the returned result. Example:

```python
@debug()
def my_add(a, b):
    return a + b

>>> my_add(1, 2)
Executing "my_add" with params: (1, 2), {}
Finished "my_add" execution with result: 3
3
```

### `count_calls` decorator

Keeps track of how many times certain function was called. Example:

```python
@count_calls
def my_func():
   pass

>>> my_func()
>>> my_func()
>>> my_func()
>>> my_func()
>>> my_func.counter()
4
```

### `memoized` decorator

This decorator should keep track of previous executions of the decorated function and the result of the invokations. If the decorated function is execution again using the same set of arguments sent in the past, the result must be immediately returned by an internal cache instead of re executing the same code again. Example:

```python
@memoized
def add(a, b):
    return a + b

>>> add(1, 2)
3
>>> add(2, 3)
5
>>> add(1, 2)
3  # `add` was not executed, result was returned from internal cache
```

As we said before, a second requirement of this group work is to also implement new decorators out of this initial set. We require at least *Two more decorators* with their proper test cases. Adding even more than 2 will give you some extra points.
