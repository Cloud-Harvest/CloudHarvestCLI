from messages import Messages
from enum import Enum
from threading import Thread
from typing import Any, Dict
from concurrent.futures import Future, ThreadPoolExecutor, ProcessPoolExecutor


class ConcurrentProcesses:
    objects = []

    @staticmethod
    def add(o: (Thread, ThreadPoolExecutor, ProcessPoolExecutor)):
        ConcurrentProcesses.objects.append(o)

        return ConcurrentProcesses

    @staticmethod
    def prune():
        [
            ConcurrentProcesses.objects.remove(o)
            for o in ConcurrentProcesses.objects
            if o.status == ProcessStatusCodes.COMPLETE
        ]

        return ConcurrentProcesses


class ProcessStatusCodes(Enum):
    INITIALIZED = 0
    RUNNING = 1
    COMPLETE = 2
    ERROR = 3
    KILL = 4


class HarvestThread(Thread):
    pass


class ThreadPool(ThreadPoolExecutor):
    def __init__(self, **kwargs):
        self.futures: Dict[Future, Any] = {}
        self.status = ProcessStatusCodes.INITIALIZED

        super().__init__(**kwargs)

    def add(self, parent: Any, function, *args, **kwargs):
        future = self.submit(function, *args, **kwargs)

        self.futures[future] = parent

        return self

    def kill(self):
        # notify the pool it needs to cancel
        self.shutdown(wait=False, cancel_futures=True)

        # notify the parent objects that they need to stop if the parent supports the kill() function
        [parent.kill() for parent in self.futures.values() if hasattr(parent, 'kill')]

        # sets this process status to KILL
        if all([parent.status == ProcessStatusCodes.COMPLETE for parent in self.futures.values()]):
            self.status = ProcessStatusCodes.COMPLETE

        else:
            self.status = ProcessStatusCodes.KILL

        return self

    @property
    def progress(self) -> dict:
        result = {code: 0 for code in ProcessStatusCodes}

        [sum(result[parent.status: ProcessStatusCodes], 1) for future, parent in self.futures.items()]

        return result


if __name__ == '__main__':
    pass
