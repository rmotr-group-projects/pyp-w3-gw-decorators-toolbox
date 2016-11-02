# -*- coding: utf-8 -*-
import time
import unittest
from testfixtures import LogCapture

from decorators_library.decorators import *
from decorators_library.exceptions import *


class DecoratorsTestCase(unittest.TestCase):

    def test_timeout_doesnt_raise(self):
        @timeout(2)
        def very_slow_function():
            time.sleep(1)
        very_slow_function()

    def test_timeout_raises(self):
        @timeout(1)
        def very_slow_function():
            time.sleep(2)
        with self.assertRaisesRegexp(TimeoutError, 'Function call timed out'):
            very_slow_function()

    def test_debug_default_logger(self):
        @debug()
        def my_add(a, b):
            return a + b

        with LogCapture() as capture:
            res = my_add(1, 2)
            capture.check(
                ('tests.test_decorators', 'DEBUG', 'Executing "my_add" with params: (1, 2), {}'),
                ('tests.test_decorators', 'DEBUG', 'Finished "my_add" execution with result: 3')
            )
        self.assertEqual(res, 3)

    def test_debug_custom_logger(self):
        logging.basicConfig()
        error_logger = logging.getLogger('test_decorators.error_logger')
        error_logger.setLevel(logging.ERROR)

        @debug(logger=error_logger)
        def my_add(a, b):
            return a + b

        with LogCapture() as capture:
            res = my_add(1, 2)
            capture.check()  # nothing was logged
        self.assertEqual(res, 3)

    def test_count_calls(self):
        @count_calls
        def my_func():
           pass
        my_func()
        my_func()
        my_func()
        my_func()
        self.assertEqual(my_func.counter(), 4)
        self.assertEqual(count_calls.counters(), {'my_func': 4})
        count_calls.reset_counters()

    def test_count_calls_multi_function(self):
        @count_calls
        def my_func():
           pass

        @count_calls
        def my_other_func():
           pass

        my_func()
        my_func()
        my_func()
        my_other_func()
        self.assertEqual(my_func.counter(), 3)
        self.assertEqual(my_other_func.counter(), 1)
        self.assertEqual(count_calls.counters(),
                         {'my_func': 3, 'my_other_func': 1})
        count_calls.reset_counters()

    def test_count_calls_no_calls(self):
        @count_calls
        def my_func():
           pass
        self.assertEqual(my_func.counter(), 0)
        self.assertEqual(count_calls.counters(), {'my_func': 0})
        count_calls.reset_counters()

    def test_memoized(self):
        @memoized
        def add(a, b):
            return a + b

        self.assertEqual(add(1, 2), 3)
        self.assertEqual(add(2, 3), 5)
        self.assertEqual(add.cache, {(1, 2): 3, (2, 3): 5})
        self.assertEqual(add(1, 2), 3)
        self.assertEqual(add.cache, {(1, 2): 3, (2, 3): 5})
        self.assertEqual(add(3, 4), 7)
        self.assertEqual(add.cache, {(1, 2): 3, (2, 3): 5, (3, 4): 7})

    def test_html_wraps_default(self):
        @html_wraps(template=None)
        def say_hello():
            return '<p>Hello decorator world!</p>'

        self.assertIn('<body>\n<p>Hello decorator world!</p>\n</body', say_hello())


    def test_html_wraps_custom_template(self):
        @html_wraps(template='<div>{}</div>')
        def say_hello():
            return '<p>Hello decorator world!</p>'

        self.assertEqual('<div><p>Hello decorator world!</p></div>', say_hello())

    def test_abuse_html_wraps(self):
        # Having some fun chaining decorators :)
        @html_wraps(template='<div class="outer">{}</div>')
        @html_wraps(template='<div class="inner">{}</div>')
        @html_wraps(template='<span>{}</span>')
        def say_hello():
            return '<p>Hello decorator world!</p>'

        self.assertEqual('<div class="outer"><div class="inner"><span>'
                         '<p>Hello decorator world!</p></span></div></div>', say_hello())

    def test_execution_time(self):
        @execution_time()
        def example_function():
            time.sleep(1)
        
        self.assertEqual(example_function(), 1.0)
    
def pretty_result(original_function):
    def wrapper(*args):
        return "The result of the function '{}' is: {}" \
            .format(original_function.__name__, original_function(*args))
    return wrapper


class ConditionalDecoratorTestCase(unittest.TestCase):
    """
    Test the on_condition decorator with the pretty_result function
    being decorated conditionally on 'condition' param
    """
    @staticmethod
    @on_condition(pretty_result, True)
    def add(x, y):
        return x + y

    @staticmethod
    @on_condition(pretty_result, False)
    def subtract(x, y):
        return x - y

    def test_condition_true(self):
        self.assertEqual(self.add(2, 5), "The result of the function 'add' is: 7")

    def test_condition_false(self):
        self.assertEqual(
            self.subtract(13, 8), 5)
