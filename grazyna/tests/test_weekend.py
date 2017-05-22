""" simple pytests for weekend plugin """
import asyncio
from datetime import datetime

import pytest
from grazyna.plugins.weekend import weekend


class MockBot(object):
    """ Mock for bot request """
    def reply(self, msg):
        """ method called by plugin to return msg for channel """
        pass

@pytest.mark.asyncio
def test_weekend():
    """ Test for calculating days to proper answers """
    class_bot = MockBot()
    assert (yield from weekend(class_bot, datetime(2017, 5, 22)))\
           == "Niestety dopiero Monday, musisz jeszcze poczekać..."
    assert (yield from weekend(class_bot, datetime(2017, 5, 23)))\
           == "Niestety dopiero Tuesday, musisz jeszcze poczekać..."
    assert (yield from weekend(class_bot, datetime(2017, 5, 24)))\
           == "Niestety dopiero Wednesday, musisz jeszcze poczekać..."
    assert (yield from weekend(class_bot, datetime(2017, 5, 25)))\
           == "Niestety dopiero Thursday, musisz jeszcze poczekać..."
    assert (yield from weekend(class_bot, datetime(2017, 5, 26)))\
           == "Niestety dopiero Friday, musisz jeszcze poczekać..."
    assert (yield from weekend(class_bot, datetime(2017, 5, 27)))\
           == "Tak, u mnie jest weekend. Omawiamy tylko lajtowe tematy, ok?"
    assert (yield from weekend(class_bot, datetime(2017, 5, 28)))\
           == "Tak, u mnie jest weekend. Omawiamy tylko lajtowe tematy, ok?"
