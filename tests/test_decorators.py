# -*- coding: utf-8 -*-
import time
import unittest
import re
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

    def test_word_replace(self):
        @WordReplace("cloud", "butt")
        def word_counter(text):
            count_dict = {}
            text = re.sub(r'[\?\"\.]', '', text)
            for word in text.split(" "):
                if word in count_dict:
                    count_dict[word] += count_dict[word]
                    continue
                count_dict[word] = 1
            counter = 0
            stats = "Here are the top 10 word count statisics\n\n"
            for word, count in sorted(count_dict.items(),
                                    key=lambda x: (x[1],x[0]),
                                    reverse=True):
                counter += 1
                stats += "{}: {}\n".format(word, count)
                if counter == 10:
                    break
            return stats

        test_text = ("What is the cloud? Where is the cloud? Are we in the cloud now?"
                     " These are all questions you've probably heard or even asked yourself."
                     " The term \"cloud computing\" is everywhere.")
        expected_results = ("Here are the top 10 word count statisics\n\nbutt: 8\nthe: 4\n"
                            "is: 4\nyourself: 1\nyou've: 1\nwe: 1\nterm: 1\nquestions: 1\n"
                            "probably: 1\nor: 1\n") 
        results = word_counter(test_text)
        self.assertEqual(results, expected_results)
        
        
    def test_retry(self):       
        @retry
        def connection(x):
            calls.append(x)
            if x == 3:
                return True
            return False
        calls = []
        for i in range(1,4):
            test = connection(i)
        self.assertEqual(calls, [1, 1, 1, 2, 2, 2, 3])