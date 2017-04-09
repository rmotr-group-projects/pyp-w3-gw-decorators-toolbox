# -*- coding: utf-8 -*-
import time
import unittest
from testfixtures import LogCapture

from decorators import *
from exceptions import *


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
        
    def test_time_me_funct_does_nothing(self):
        @time_me
        def nothing_funct():
            pass
        nothing_funct()
        
        self.assertEqual(round(nothing_funct.timed), 0)
        
    def test_time_me_funct_one_sec(self):
        @time_me
        def second_funct():
            time.sleep(1)
            
        second_funct()
        
        self.assertEqual(round(second_funct.timed), 1)
        
    def test_time_me_funct_two_sec(self):
        @time_me
        def two_sec_funct():
            time.sleep(2)
            
        two_sec_funct()
        
        self.assertEqual(round(two_sec_funct.timed), 2)
        
    def test_check_permission_none(self):
        me = {
            'name': 'Gregory Steinhoff',
            'permissions': []
        }
        
        @check_permission('edit')
        def edit_something(user):
            output = user.get('name') + " is trying to edit something"
            return output
        with self.assertRaisesRegexp(PermissionError, 'Sorry, you do not have permission for this'):
            edit_something(me)
        
        
    def test_check_permission_edit(self):
        me = {
            'name': 'Gregory Steinhoff',
            'permissions': ['edit', 'view', 'delete' ]
        }
        
        @check_permission('edit')
        def edit_something(user):
            output = user.get('name') + " is trying to edit something"
            return output
        
        self.assertEqual(edit_something(me), 'Gregory Steinhoff is trying to edit something')    
        
    def test_check_permission_delete(self):
        me = {
            'name': 'Gregory Steinhoff',
            'permissions': ['edit', 'delete' ]
        }
        
        @check_permission('delete')
        def delete_something(user):
            output = user.get('name') + " is trying to delete something"
            return output
        
        self.assertEqual(delete_something(me), 'Gregory Steinhoff is trying to delete something')   
            