from rich.progress import TextColumn
from rich.style import Style

from CloudHarvestCLI.api import HTTP_REQUEST_TYPES, request
from CloudHarvestCoreTasks.dataset import WalkableDict

from concurrent.futures import Future, ThreadPoolExecutor, ProcessPoolExecutor
from enum import Enum
from logging import getLogger
from threading import Thread
from typing import Any, Dict, List, Tuple

from messages import add_message

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
    def report() -> Tuple[tuple, List[dict]]:
        report_keys = (
            'Name',
            'Status',
            'Progress',
            'Total',
            'Completed',
            'Description'
        )

        from collections import OrderedDict
        return report_keys, [OrderedDict(
            **{
                k: getattr(o, k.lower()) if hasattr(o, k.lower()) else ''
                for k in report_keys
            }
        )
            for o in ConcurrentProcesses.objects
        ]


class ProcessStatusCodes(Enum):
    INITIALIZED = 0
    RUNNING = 1
    COMPLETE = 2
    ERROR = 3
    KILL = 4


class HarvestThread(Thread):
    def __init__(self, description: str = None, **kwargs):
        self.description = description

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
    def __init__(self, name: str = None, description: str = None, max_workers: int = None,
                 alert_on_complete: bool = False, **kwargs):

        from uuid import uuid4
        self.name = name or str(uuid4())
        self.description = description
        self.alert_on_complete = alert_on_complete
        self.futures: Dict[Future, Any] = {}
        self.status = ProcessStatusCodes.INITIALIZED

        from datetime import datetime
        self.started = datetime.now()

        from multiprocessing import cpu_count
        self.max_workers = max_workers if max_workers > 0 else cpu_count() * 2

        super().__init__(max_workers=self.max_workers, **kwargs)

        ConcurrentProcesses.add(self)

    def add(self, parent: Any, function, *args, **kwargs):
        self.status = ProcessStatusCodes.RUNNING

        future = self.submit(function, *args, **kwargs)

        self.futures[future] = parent

        return self

    def shutdown(self, wait: bool = True, *, cancel_futures: bool = False):
        super().shutdown(wait=wait, cancel_futures=cancel_futures)

        if self.alert_on_complete and all(future.done() for future in self.futures):
            self.on_complete()

    def attach_progressbar(self):
        # attaches a progressbar to the console
        try:
            with HarvestProgressBar(description=self.description, pool=self) as pb:
                pb.attach()

        except KeyboardInterrupt:
            from CloudHarvestCLI.messages import add_message
            add_message(self, 'INFO', True, f'Sending process {self.name} to background.')
            if self.alert_on_complete:
                self.start_monitor_thread()

    def kill(self, wait: bool = False):
        self.status = ProcessStatusCodes.KILL

        # notify the parent objects that they need to stop if the parent supports the kill() function
        [parent.kill() for parent in self.futures.values() if hasattr(parent, 'kill')]

        # notify the pool it needs to cancel
        self.shutdown(wait=wait, cancel_futures=True)

        # sets this process status to KILL
        if all([parent.status == ProcessStatusCodes.COMPLETE for parent in self.futures.values()]):
            self.status = ProcessStatusCodes.COMPLETE

        return self

    @property
    def completed(self) -> int:
        return len([future for future in self.futures if future.done()])

    @property
    def duration(self) -> float:
        from datetime import datetime
        return (datetime.now() - self.started).total_seconds()

    @property
    def progress(self) -> dict:
        result = {code: 0 for code in ProcessStatusCodes}

        [sum(result[parent.status: ProcessStatusCodes], 1) for future, parent in self.futures.items()]

        return result

    @property
    def total(self) -> int:
        return len(self.futures)

    def on_complete(self):
        from CloudHarvestCLI.messages import add_message
        add_message(self, 'INFO', True, f'{self.name} job has completed.')

    def start_monitor_thread(self):
        from threading import Thread

        def monitor():
            while True:
                if self.status == ProcessStatusCodes.KILL:
                    # we can wait here because the shutdown is happening in the background via the monitoring thread
                    self.kill(wait=True)
                    break

                elif self.status == ProcessStatusCodes.COMPLETE:
                    self.shutdown()
                    break

                from time import sleep
                sleep(1)

        t = Thread(target=monitor)
        t.start()

        return self


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

                    progress.update(main_task, completed=self.pool.completed, total=self.pool.total)
                    if self.pool.completed == self.pool.total:
                        break

                    from time import sleep
                    sleep(.25)

        except KeyboardInterrupt:
            from CloudHarvestCLI.messages import add_message
            add_message(self, 'INFO', True, f'Sending thread `{self.pool.name}` to background.')

class HarvestRemoteJobAwaiter:
    def __init__(self,
                 endpoint: str,
                 request_type: HTTP_REQUEST_TYPES = 'get',
                 request_data: dict = None,
                 name_key: str = 'redis_name',
                 desired_status: str = 'complete',
                 position_key: str = 'position',
                 total_key: str = 'total',
                 status_key: str = 'status',
                 check_interval: int = 1,
                 timeout: int = 300,
                 with_notification: bool = False,
                 with_progress_bar: bool = False):

        """
        This class is used to poll the API for the status of a job and exit when the job is complete or an error occurs.
        Polling is done at a specified interval and the job is considered complete when one of the following
        conditions is met:
            - The timeout is reached
            - The job reaches 100% completion
            - The job status is equal to the desired status
            - The job reaches one of these error states (as defined in the `percent()` property):
                - 'complete'
                - 'error'
                - 'skipped'

        Arguments
        endpoint: (str) The endpoint to poll.
        request_type: (str, optional) The type of request to make. Defaults to 'get'.
        request_data: (str, optional) The data to send with the request. Defaults to None.
        name_key: (str, optional) The key to use to get the name of the job. Defaults to 'name'.
        desired_status: (str, optional) The status to wait for. Defaults to 'complete'.
        position_key: (str, optional) The key to use to get the position of the job. Defaults to 'position'.
        total_key: (str, optional) The key to use to get the total of the job. Defaults to 'total'.
        status_key: (str, optional) The key to use to get the status of the job. Defaults to 'status'.
        check_interval: (int, optional) The interval to wait between requests. Defaults to 1 second.
        timeout: (int, optional) The timeout to wait before giving up. Defaults to 300 seconds.
        with_notification: (bool, optional) Whether to show a notification when the job is complete. Defaults to False.
        with_progress_bar: (bool, optional) Whether to show a progress bar. Defaults to False.
        """

        # Arguments
        self.endpoint = endpoint
        self.request_type = request_type
        self.request_data = request_data
        self.name_key = name_key
        self.desired_status = desired_status
        self.position_key = position_key
        self.total_key = total_key
        self.status_key = status_key
        self.check_interval = check_interval
        self.timeout = timeout
        self.with_notification = with_notification
        self.with_progress_bar = with_progress_bar

        # Programmatic variables
        self.attempts = 0
        self.data = WalkableDict()
        self.start_time = None
        self.end_time = None
        self.progress_indicator = None
        self.worker_thread = None

        # Terminate
        self.terminate = False

    @property
    def name(self):
        """
        Returns the name of the job.
        """

        if isinstance(self.data, WalkableDict):
            return self.data.get(self.name_key) or 'awaiting task creation'

        else:
            return 'unknown'

    @property
    def status(self) -> str:
        """
        Returns the status of the job.
        """

        if isinstance(self.data, WalkableDict):
            return self.data.get(self.status_key) or 'unknown'

        else:
            return 'unknown'

    @property
    def position(self) -> int:
        """
        Returns the position of the job.
        """

        if isinstance(self.data, WalkableDict):
            return self.data.get(self.position_key) or 0

        else:
            return 0

    @property
    def total(self) -> int:
        """
        Returns the total of the job.
        """

        if isinstance(self.data, WalkableDict):
            return self.data.get(self.total_key) or 0

        else:
            return 0

    @property
    def percent(self) -> float:
        """
        Returns the percent of the job.
        """

        from CloudHarvestCoreTasks.tasks.base import TaskStatusCodes

        # Each of the following codes indicates that the job will make no further progress. We therefore consider the
        # job to be complete, even if the percent is not 100.
        exit_loop_status_codes = (
            TaskStatusCodes.complete,
            self.desired_status
        )

        # We consider any job in the desired, complete, or an exit state to be 100% complete even if its total would not
        # be 100%.
        if self.status in exit_loop_status_codes:
            return 100.0

        # Make sure we don't try to divide by zero
        elif self.total > 0:
            return (self.position / self.total) * 100

        else:
            return 0.0

    def attach(self):
        from rich.progress import (
            Progress,
            BarColumn,
            TimeElapsedColumn,
            TimeRemainingColumn,
            SpinnerColumn,
            TextColumn
        )

        from CloudHarvestCLI.text.styling import TextColors

        status_color = TextColors.ERROR if self.status == 'error' else TextColors.HEADER

        config = (
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}", style=TextColors.INFO),
            TextColumn("{task.fields[status]}", style=Style(color=status_color)),
            BarColumn(),
            "[progress.percentage]{task.percentage:3.0f}%",
            TimeElapsedColumn(),
            "/",
            TimeRemainingColumn(),
            "[progress.completed]{task.completed}/[progress.total]{task.total}"
        )

        from CloudHarvestCLI.messages import add_message

        from time import sleep
        with Progress(*config) as progress:
            task_id = progress.add_task(description=self.name, total=self.total, completed=self.position, visible=True, status=self.status)

            while True:
                try:
                    progress.update(task_id=task_id, description=self.name, total=self.total, completed=self.position, status=self.status)

                    if self.percent >= 100:
                        break

                    if self.terminate:
                        progress.stop()
                        break

                except KeyboardInterrupt:
                    add_message(self, 'INFO', True, f'Sending thread `{self.name}` to background.')
                    # When going to background, make sure to notify the user when the task is complete
                    self.with_notification = True

                    # Set the check interval to 60 seconds so we don't hammer the API
                    self.check_interval = 60
                    break

                except Exception as ex:
                    add_message(self, 'ERROR', True, f'Error updating progress bar: {ex}')
                    break

                sleep(.25)

    def fetch(self) -> 'HarvestRemoteJobAwaiter':
        """
        Fetches the data from the API and returns it as a WalkableDict object.
        """

        response = request(request_type=self.request_type,
                           endpoint=self.endpoint,
                           data=self.request_data)

        if response is None:
            return self

        if isinstance(response, str):
            from json import loads
            response = loads(response)


        if isinstance(response, dict):
            if 'result' in response:
                response = response.get('result')

            response = WalkableDict(response)

        else:
            raise TypeError(f'Expected a dictionary, got {type(response)}')

        self.data = WalkableDict(response)

        return self

    def run(self) -> 'HarvestRemoteJobAwaiter':
        """
        Runs the job awaiter until an exit condition is met.
        """

        from threading import Thread
        self.worker_thread = Thread(target=self._worker, name=self.name, daemon=True)
        self.worker_thread.start()

        if self.with_progress_bar:
            self.attach()

        return self

    def _worker(self):
        from CloudHarvestCLI.messages import add_message

        from datetime import datetime
        from time import sleep

        self.start_time = datetime.now()
        was_timeout = False

        failed_attempts = 0
        while True:
            try:
                if self.terminate:
                    break

                self.fetch()

                if self.percent >= 100:
                    break

                if self.timeout and (datetime.now() - self.start_time).total_seconds() > self.timeout:
                    self.terminate = True
                    was_timeout = True
                    break

            except Exception as ex:
                failed_attempts += 1

                if failed_attempts >= 10:
                    add_message(self, 'ERROR', True, f'{self.name} failed at least ten times to get the status of the task: {ex}')
                    self.terminate = True
                    break

            sleep(self.check_interval)

        self.end_time = datetime.now()

        if was_timeout or self.with_notification:
            final_status = 'timeout' if was_timeout else self.data.walk(self.status_key) or 'unknown'

            add_message(self, 'INFO', True, f'{self.name} has finished with status: {final_status}')
