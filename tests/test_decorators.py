# -*- coding: utf-8 -*-
import time
import unittest
import os
from testfixtures import LogCapture
import  time

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



    def test_store_to_file(self):
        @store_to_file()
        def return_one():
            return 1

        return_one()
        return_one()

        with open('DataFolder/myData', 'rt') as fout:
            data = fout.read()
            data=data.split(" ")

        import shutil
        if os.path.exists('DataFolder'):
            shutil.rmtree('DataFolder')

        self.assertEqual(data, ['1', '1'])

    def test_word_frequency(self):
        @word_frequency('lorem')
        def my_func():
            return '''Lorem Ipsum is simply dummy text\
             of the printing and typesetting industry. \
             Lorem Ipsum has been the industry's standard \
             dummy text ever since the 1500s, when an unknown \
             printer took a galley of type and scrambled it \
             to make a type specimen book. It has survived not \
             only five centuries, but also the leap into
             electronic typesetting, remaining essentially \
             unchanged. It was popularised in the 1960s with \
             the release of Letraset sheets containing Lorem \
             Ipsum passages, and more recently with desktop \
             publishing software like Aldus PageMaker including \
             versions of Lorem Ipsum.'''

        result = my_func()
        string = 'The word lorem is found 4 times in the result of my_func function'

        self.assertEqual(result, string)