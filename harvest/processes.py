from messages import Messages
from enum import Enum
from threading import Thread
from typing import Any, Dict, List
from concurrent.futures import Future, ThreadPoolExecutor, ProcessPoolExecutor
from logging import getLogger

logger = getLogger('harvest')


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

    @staticmethod
    def report() -> List[dict]:
        return [
            {
                'Name': o.name,
                'Status': o.status
            }
            for o in ConcurrentProcesses.objects
        ]


class ProcessStatusCodes(Enum):
    INITIALIZED = 0
    RUNNING = 1
    COMPLETE = 2
    ERROR = 3
    KILL = 4


class HarvestThread(Thread):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.status = ProcessStatusCodes.INITIALIZED

    def start(self):
        self.status = ProcessStatusCodes.RUNNING

        super().start()

        return self

    def kill(self):
        self.status = ProcessStatusCodes.KILL

        return self


class ThreadPool(ThreadPoolExecutor):
    def __init__(self, name: str = None, description: str = None, max_workers: int = None, **kwargs):
        self.name = name
        self.description = description
        self.futures: Dict[Future, Any] = {}
        self.status = ProcessStatusCodes.INITIALIZED

        from multiprocessing import cpu_count
        self.max_workers = max_workers if max_workers > 0 else cpu_count() * 2

        super().__init__(max_workers=self.max_workers, **kwargs)

        ConcurrentProcesses.add(self)

    def add(self, parent: Any, function, *args, **kwargs):
        future = self.submit(function, *args, **kwargs)

        self.futures[future] = parent

        return self

    def attach_progressbar(self):
        # attaches a progressbar to the console
        try:
            with HarvestProgressBar(description=self.description, pool=self) as pb:
                pb.attach()

        except KeyboardInterrupt:
            from text.printing import print_message
            print_message('Interrupt acknowledged.', color='INFO', as_feedback=True)

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
    def completed(self) -> int:
        return len([future for future in self.futures if future.done()])

    @property
    def progress(self) -> dict:
        result = {code: 0 for code in ProcessStatusCodes}

        [sum(result[parent.status: ProcessStatusCodes], 1) for future, parent in self.futures.items()]

        return result

    @property
    def total(self) -> int:
        return len(self.futures)


class HarvestProgressBar:
    def __init__(self, pool: ThreadPool, description: str = None):
        self.pool: ThreadPool = pool
        self.description = description

        super().__init__()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return None

    def attach(self, pool: ThreadPool = None, subprocesses_as_tasks: bool = False):
        self.pool: ThreadPool = pool or self.pool

        subtask_ids = {

        }

        try:
            from rich.progress import Progress, BarColumn, TimeElapsedColumn, TimeRemainingColumn, SpinnerColumn

            config = (
                SpinnerColumn(),
                "[progress.description]{task.description}",
                BarColumn(),
                "[progress.percentage]{task.percentage:3.0f}%",
                TimeElapsedColumn(),
                "/",
                TimeRemainingColumn(),
                "[progress.completed]{task.completed}/[progress.total]{task.total}"
            )

            with Progress(*config) as progress:
                main_task = progress.add_task(description=f'{self.description} ({self.pool.max_workers})')
                while True:
                    if subprocesses_as_tasks:
                        for future, parent in self.pool.futures.items():
                            if future.running():
                                # don't add a task that shows 0/0
                                if parent.total == 0 and parent.status == 0:
                                    continue

                                elif future in subtask_ids.keys():
                                    progress.update(task_id=subtask_ids.get(future),
                                                    completed=parent.completed,
                                                    total=parent.total)

                                else:
                                    subtask_id = progress.add_task(description=f'└── {parent.name}',
                                                                   total=parent.total)

                                    logger.debug(f'Created {subtask_id} for {parent.name} / {future}')
                                    subtask_ids[future] = subtask_id

                            elif future.done():
                                if future in subtask_ids.keys():
                                    try:
                                        progress.remove_task(subtask_ids.get(future))
                                    finally:
                                        subtask_ids.pop(future)

                            if self.pool.progress.get('completed') == self.pool.total:
                                break

                    if self.pool.completed == self.pool.total:
                        break

                    from time import sleep
                    sleep(.25)

        except KeyboardInterrupt:
            from text.printing import print_message
            print_message('Interrupt acknowledged.', color='INFO', as_feedback=True)


if __name__ == '__main__':
    pass
