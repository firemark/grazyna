from grazyna.modules import ExecutedCounter
from freezegun import freeze_time
from datetime import datetime


def test_counter_init():
    with freeze_time('2016-06-06'):
        counter = ExecutedCounter()
    assert counter.counter == 0
    assert counter.last_time == datetime(2016, 6, 6)


def test_counter_increase():
    counter = ExecutedCounter()
    counter.inc()
    assert counter.counter == 1
