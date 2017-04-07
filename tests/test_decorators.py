# -*- coding: utf-8 -*-
import time
import unittest
from testfixtures import LogCapture
from datetime import datetime as dt

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
        
    def test_memoized_sub(self):
        @memoized
        def subtract(a, b):
            return a - b

        self.assertEqual(subtract(3, 2), 1)
        self.assertEqual(subtract(1, 3), -2)
        self.assertEqual(subtract.cache, {(3, 2): 1, (1, 3): -2})
        self.assertEqual(subtract(3, 2), 1)
        self.assertEqual(subtract.cache, {(3, 2): 1, (1, 3): -2})
        self.assertEqual(subtract(6, 4), 2)
        self.assertEqual(subtract.cache, {(3, 2): 1, (1, 3): -2, (6, 4): 2})

    def test_time_log(self):
        @timelog
        def something():
            pass
        
        @timelog
        def something_else():
            pass
        
        something()
        something()
        something_else()
        time = dt.now().strftime('%Y-%m-%d %H:%M:%S')
        self.assertEqual(something.get_one_log(), [
                'something called at {}'.format(time),
                'something called at {}'.format(time)
                ])
        self.assertEqual(timelog.get_log(), {
            'something': [
                'something called at {}'.format(time),
                'something called at {}'.format(time)
                ],
            'something_else': [
                'something_else called at {}'.format(time)
                ]
        })
        timelog.clear_log()
        something_else()
        self.assertEqual(timelog.get_log(), {
            'something_else': [
                'something_else called at {}'.format(time)
                ]
        })
        
    def test_opposite(self):
        @opposite
        def thing(a, b, c, d):
            return a + b - c * d

        @opposite
        def anotherthing(a, b):
            return "{} {}'s Flying Circus".format(a, b)
            
        self.assertEqual(thing(1, 2, 3, 4), 5)
        self.assertEqual(anotherthing('Monty', 'Python'), "Python Monty's Flying Circus")
            
    def test_validarg(self):
        @validarg((int, float), (int, float))
        def add(x, y):
            return x + y
            
        @validarg(str, str)
        def concat(x, y):
            return x + y
            
        self.assertEqual(add(1,1), 2)
        with self.assertRaises(TypeError):
            add(1,'1')
        with self.assertRaises(IndexError):
            add(1, 2, 3)
        self.assertEqual(concat('abc', '123'), 'abc123')
        with self.assertRaises(TypeError):
            concat('1', 1)
        with self.assertRaises(IndexError):
            concat('a')
