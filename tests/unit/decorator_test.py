import time
from ratelimit import limits, RateLimitException
from tests import unittest

class TestDecorator(unittest.TestCase):

    @limits(calls=1, period=10)
    def increment(self):
        '''
        Increment the counter at most once every 10 seconds.
        '''
        self.count += 1

    @limits(calls=1, period=10, raise_on_limit=False)
    def increment_no_exception(self):
        '''
        Increment the counter at most once every 10 seconds, but w/o rasing an
        exception when reaching limit.
        '''
        self.count += 1

    def setUp(self):
        self.count = 0
        time.sleep(10)

    def test_increment(self):
        self.increment()
        self.assertEqual(self.count, 1)

    def test_exception(self):
        self.increment()
        self.assertRaises(RateLimitException, self.increment)

    def test_reset(self):
        self.increment()
        time.sleep(10)

        self.increment()
        self.assertEqual(self.count, 2)

    def test_no_exception(self):
        self.increment_no_exception()
        self.increment_no_exception()

        self.assertEqual(self.count, 1)
