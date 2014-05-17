import datetime
import threading

from enum import Enum

IMMEDIATE_RUN_THRESH = 1  # 1 second


def default_run_worker(delay_secs, worker):
    if delay_secs <= IMMEDIATE_RUN_THRESH:
        timer = threading.Thread(target=worker)
    else:
        timer = threading.Timer(delay_secs, worker)
    timer.start()


# TODO: Synchronize
class Scheduler:
    def __init__(self):
        self.worker_queue = []
        self.next_timer = None

    def add(self, delay: datetime.timedelta, worker: callable, zero_run: bool = True):
        next_time = datetime.datetime.now() + delay
        self.worker_queue.append((next_time, worker))
        self.worker_queue.sort(key=lambda x: x[0])
        self.reschedule()

    def run_worker(self, delay_secs, worker):
        self.on_worker_call(worker)
        default_run_worker(delay_secs, worker)

    def reschedule(self):
        if self.next_timer is not None:
            self.next_timer.calcel()
        next_time, next_worker = self.worker_queue.pop()
        next_delay_secs = (next_time - datetime.datetime.now()).total_seconds()
        self.run_worker(next_delay_secs, next_worker)

    def on_worker_call(self, worker):
        pass


class WorkerStatus(Enum):
    ready = 'ready'
    working = 'working'
    waiting = 'waiting'
    stopped = 'stopped'


class Worker:
    def __init__(self, interval: datetime.timedelta, repeat=True, scheduler: Scheduler=None):
        self.interval = interval
        self.repeat = repeat
        self.scheduler = scheduler
        self.is_stop_invoked = False
        self._next_expected = None
        self.status = WorkerStatus.ready

    def next_time(self):
        if self._next_expected is None:
            raise RuntimeError('This worker have not been started yet.')
        else:
            return self._next_expected

    def start(self):
        """Start working.

        If interval is given in constructor (ant it is a valid timedelta object),
        the work will be executed at each interval after first working finished.

        So, works will be executed like following figure:

             'start called'                         'stop called'
                   |                                     |
                [Work] ---- interval ---> [Work] ---- interval ---> <<< Stopped >>>

        This will be run asynchronously, so control will be returned immediately in each case.
        """
        if self.is_stop_invoked:
            raise RuntimeError('This worker already stopped.')
        self.schedule_next(datetime.timedelta(0))

    def schedule_next(self, delay: datetime.timedelta):
        self._next_expected = datetime.datetime.now() + delay
        if self.scheduler is None:
            delay_secs = delay.total_seconds()
            default_run_worker(delay_secs, self)
        else:
            self.scheduler.add(delay, self)

    def stop(self):
        self.is_stop_invoked = True

    def __call__(self):
        if self.is_stop_invoked:
            return
        self.status = WorkerStatus.working
        self.work()
        if self.repeat and not self.is_stop_invoked:
            self.schedule_next(self.interval)
            self.status = WorkerStatus.waiting
        else:
            self.status = WorkerStatus.stopped

    def work(self):
        raise NotImplemented()

    @property
    def is_working(self):
        return self.status == WorkerStatus.working or \
            self.status == WorkerStatus.waiting
