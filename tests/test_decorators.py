# -*- coding: utf-8 -*-
import time
import unittest
from testfixtures import LogCapture
import logging

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
           return 1
        my_func()
        my_func()
        my_func()
        self.assertEqual(my_func(), 1)
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

    def test_assert_type_length(self):
        @assert_type(int, int)
        def my_add(a, b):
            return a + b
        
        with self.assertRaisesRegexp(ValueError, 'Wrong number arguments. Expected: 2; Received: 3'):
            my_add(2, 23, 4)
        
    
    def test_assert_type_different_types(self):
        @assert_type(int, int)
        def my_add(a, b):
            return a + b
            
        self.assertEqual(my_add(1,2), 3)
        with self.assertRaises(TypeError):
            my_add("asd", 5)
        # with self.assertRaisesRegexp(TypeError, "Wrong type. Expected: ('int', 'int'); Received: ('str', 'int')"):
        #     my_add("ads", 2)
        
    def test_running_time(self):
        """tracks the running times for a function"""
        @running_time
        def my_add(a, b):
            return a +b
            
        my_add(10,20)
        my_add(50,20)
        my_add(1000,4259)
        
        self.assertEqual(my_add(1,2), 3)
        self.assertEqual(my_add.counter(), 4)
        self.assertTrue(0 < my_add.average_time() <  0.001)