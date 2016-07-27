# -*- coding: utf-8 -*-
import time
import unittest
from testfixtures import LogCapture
from functools import reduce

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
        def add(*args):
            return sum(args)

        self.assertEqual(add(1, 2, 3), 6)
        self.assertEqual(add(2, 3), 5)
        self.assertEqual(add.cache, {(1, 2, 3): 6, (2, 3): 5})
        self.assertEqual(add(1, 2, 3), 6)
        self.assertEqual(add.cache, {(1, 2, 3): 6, (2, 3): 5})
        self.assertEqual(add(3, 4), 7)
        self.assertEqual(add.cache, {(1, 2, 3): 6, (2, 3): 5, (3, 4): 7})
        
    def test_conc(self):
        @concatenate
        def subtract(*args):
            return reduce(lambda x, y: x-y, args)
        
        self.assertEqual(subtract(5,1,2), 512)
        self.assertEqual(subtract(1,7,2), 172)    
        self.assertEqual(subtract(8,5,9), 859)
        self.assertEqual(subtract(4,2,0), '420 blaze it')
        
    def test_conc_raises(self):
        @concatenate
        def subtract():
            return reduce(lambda x, y: x-y, args)
        with self.assertRaisesRegexp(TypeError, 'Argument supplied not of type int'):
            subtract('string')
            
    def test_binary_result(self):
        @binary_result
        def add(*args):
            return reduce(lambda x, y: x+y, args)
        
        self.assertEqual(add(5,1,13), '0b10011')
        self.assertEqual(add(1,7), '0b1000')    
        self.assertEqual(add(8,5,9), '0b10110')
        self.assertEqual(add(4,2,0), '0b110')
        
    def test_binary_result_raises(self):
        @binary_result
        def add(*args):
            return reduce(lambda x, y: x+y, args)
        with self.assertRaisesRegexp(TypeError, 'Result not of type int'):
            add(4,2.3)

