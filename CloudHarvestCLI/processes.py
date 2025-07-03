from CloudHarvestCLI.api import HTTP_REQUEST_TYPES, request
from CloudHarvestCoreTasks.dataset import WalkableDict

from logging import getLogger
from typing import Any

logger = getLogger('harvest')


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
                 max_attempts: int = -1,
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
        max_attempts: (int, optional) The maximum number of attempts to make before giving up. Defaults to -1 (no limit).
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
        self.max_attempts = max_attempts
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

        self._name = None
        self._status = None
        self._position = None
        self._total = None

    def _set_property(self, name: str, data_key: str = None, default = None) -> Any:
        """
        Sets the property value based on the data from the API or the instance's default value.

        Arguments
        name: (str) The name of the property to set.
        data_key: (str, optional) The key to use to get the value from the data. Defaults to None, which uses the name.
        default: (Any, optional) The default value to use if the data is not available. Defaults to None.
        """
        data_key = data_key or name

        if isinstance(self.data, WalkableDict):
            value = self.data.get(data_key)

            # Priority: 1) value from data, 2) value from the instance, 3) default value
            new_value = value or getattr(self, f'_{name}') or default

        else:
            new_value = getattr(self, f'_{name}') or default

        # Set the property value if it has changed
        setattr(self, f'_{name}', new_value)

        # Return the new value of the property
        return new_value

    @property
    def name(self):
        """
        Returns the name of the job.
        """
        return self._set_property('name', default='unknown')

    @property
    def status(self) -> str:
        """
        Returns the status of the job.
        """
        return self._set_property('status', default='unknown')

    @property
    def position(self) -> int:
        """
        Returns the position of the job.
        """

        return self._set_property('position', data_key=self.position_key,  default=0)

    @property
    def total(self) -> int:
        """
        Returns the total of the job.
        """

        return self._set_property('total', data_key=self.total_key, default=0)

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

        from CloudHarvestCLI.text.styling import Style, TextColors

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
                    from CloudHarvestCLI.text.inputs import input_boolean
                    send_to_background = input_boolean(f'Notify when remote process completes?')

                    if send_to_background:
                        add_message(self, 'INFO', True, f'Sending thread `{self.name}` to background.')
                        # When going to background, make sure to notify the user when the task is complete
                        self.with_notification = True

                        # Set the check interval to 60 seconds so we don't hammer the API
                        self.check_interval = 60

                    else:
                        add_message(self, 'INFO', True, f'No longer monitoring remote process `{self.name}`.')
                        self.terminate = True
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

                # Reset the failed attempts counter when we successfully fetch data
                failed_attempts = 0

                if self.percent >= 100.0:
                    break

                if self.timeout and (datetime.now() - self.start_time).total_seconds() > self.timeout:
                    self.terminate = True
                    was_timeout = True
                    break

            except Exception as ex:
                failed_attempts += 1

                if self.max_attempts > 0 and (failed_attempts >= self.max_attempts):
                    add_message(self, 'ERROR', True, f'{self.name} failed to get the status of the task ({failed_attempts}): {ex}')
                    self.terminate = True
                    break

            sleep(self.check_interval)

        self.end_time = datetime.now()

        if was_timeout or self.with_notification:
            final_status = 'timeout' if was_timeout else self.data.walk(self.status_key) or 'unknown'

            add_message(self, 'INFO', True, f'{self.name} has finished with status: {final_status}')
