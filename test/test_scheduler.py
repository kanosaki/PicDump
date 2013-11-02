
import datetime
import time
import threading
import collections

from nose.plugins.attrib import attr
from nose.tools import *

utils = __import__('utils')
from picdump import scheduler


def mk_interval(ms):
    return datetime.timedelta(milliseconds=ms)


def get_now():
    return datetime.datetime.now()


def sleep(delta):
    if isinstance(delta, int):
        time.sleep(delta / 1000)
    elif isinstance(delta, datetime.timedelta):
        time.sleep(delta.total_seconds())
    else:
        raise TypeError()


class DummyWorker(scheduler.Worker):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self.exit_at = 0
        self.call_history = []
        self.previous_called_thread = None

    def work(self):
        self.call_history.append(get_now())
        self.previous_called_thread = threading.current_thread()
        if self.exit_at and self.called_count >= self.exit_at:
            self.stop()

    @property
    def called_count(self):
        return len(self.call_history)


@attr('slow')
class TestWorker:
    def setup(self):
        scheduler.IMMEDIATE_RUN_THRESH = 0  # Disable for testing

    def test_work_once(self):
        """A worker should be called once after Worker.start called
        """
        worker = DummyWorker(mk_interval(100), repeat=False)
        assert_equal(False, worker.is_working)
        worker.start()
        sleep(100)
        assert_equal(1, worker.called_count)
        assert_equal(False, worker.is_working)
        sleep(500)
        assert_equal(1, worker.called_count)

    def test_work_repeat(self):
        """A worker should be called until Worker.stop is called"""
        worker = DummyWorker(mk_interval(100))
        worker.exit_at = 3
        worker.start()
        sleep(50)
        assert_equal(1, worker.called_count)
        assert_equal(True, worker.is_working)
        sleep(100)
        assert_equal(2, worker.called_count)
        assert_equal(True, worker.is_working)
        sleep(100)
        assert_equal(3, worker.called_count)
        assert_equal(False, worker.is_working)
        sleep(100)
        assert_equal(3, worker.called_count)
        assert_equal(False, worker.is_working)


class HookedWorker(scheduler.Scheduler):
    def __init__(self):
        super().__init__()
        self.worker_history = collections.deque()

    def on_worker_call(self, worker):
        self.worker_history.append(worker)

    def pop_worker_history(self):
        return self.worker_history.popleft()


@attr('slow')
class TestScheduler:
    def setup(self):
        scheduler.IMMEDIATE_RUN_THRESH = 0  # Disable for testing

    def test_scheduler(self):
        sched = scheduler.Scheduler()
        worker = DummyWorker(mk_interval(100), scheduler=sched)
        worker.exit_at = 3
        worker.start()
        sleep(50)
        assert_equal(1, worker.called_count)
        assert_equal(True, worker.is_working)
        sleep(100)
        assert_equal(2, worker.called_count)
        assert_equal(True, worker.is_working)
        sleep(100)
        assert_equal(3, worker.called_count)
        assert_equal(False, worker.is_working)
        sleep(100)
        assert_equal(3, worker.called_count)
        assert_equal(False, worker.is_working)
