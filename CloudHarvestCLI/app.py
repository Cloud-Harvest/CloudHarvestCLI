from typing import Any, List
from cmd2 import Cmd, DEFAULT_SHORTCUTS
from cmd2.plugin import PrecommandData, PostcommandData

from CloudHarvestCorePluginManager.registry import Registry
from banner import get_banner
from configuration import HarvestConfiguration
from text import console
from text.styling import colorize, TextColors

# Activate any objects which are registered with the PluginManager Registry or cmd2.Cmd on definition. This is necessary
# to populate the commands available to a user.
from __register__ import *


class Harvest(Cmd):
    def __init__(self, **kwargs):
        # Load the configuration
        HarvestConfiguration.load()

        # Load installed plugins
        Registry.register_objects()

        # _banners display loading banners
        self._banner = get_banner(banner_configuration=HarvestConfiguration.banners or {})

        # application version
        self._version = HarvestConfiguration.version

        shortcuts = DEFAULT_SHORTCUTS | HarvestConfiguration.shortcuts or {}

        from os.path import expanduser
        super().__init__(persistent_history_file=expanduser('./app/history'),
                         persistent_history_length=5000000,
                         shortcuts=shortcuts,
                         **kwargs)

        self.register_precmd_hook(self._pre_command_hook)
        self.register_postcmd_hook(self._post_command_hooks)

        # the prompt will always have a new line at the beginning for spacing
        from os import environ
        self.prompt = get_prompt()

        console.print()  # provides a space between the first line and the banner
        console.print(self._banner[0])
        if self._banner[1]:
            console.print(self._banner[1])

        # print any messages generated during load
        from messages import read_messages
        from text.printing import print_message
        [print_message(text=message[2], color=message[1], as_feedback=True) for message in read_messages()]

        self.pfeedback(get_load_version_line())

        # start background processes
        self.last_command_timestamp = None
        self._start_notify_unread_messages_thread()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return None

    def _pre_command_hook(self, data: PrecommandData) -> PrecommandData:
        self.last_command_timestamp = None
        return data

    def _post_command_hooks(self, data: PostcommandData) -> PostcommandData:
        try:
            from messages import read_messages
            from text.printing import print_message
            for message in read_messages():
                source, color, text = message

                print_message(text=text, color=color, as_feedback=True)

        finally:
            from datetime import datetime
            self.last_command_timestamp = datetime.now().timestamp()

            return data

    def _start_notify_unread_messages_thread(self):
        def _thread():
            from datetime import datetime
            from messages import Messages, read_messages
            from text.printing import print_message
            from time import sleep
            while True:
                messages = len(Messages.queue)

                if self.last_command_timestamp:
                    if messages and self.last_command_timestamp > (datetime.now().timestamp() + 300):
                        for message in read_messages():
                            print_message(text=f'{message[0]}: {message[2]}',
                                          color=message[1],
                                          as_feedback=True)

                sleep(1)

        from processes import HarvestThread
        t = HarvestThread(**{
            'name': 'message_monitor',
            'description': 'Delivers messages to users after commands are executed or when the system is idle.',
            'target': _thread,
            'daemon': True
        })

        from processes import ConcurrentProcesses
        ConcurrentProcesses.add(t)

        t.start()


def get_load_version_line() -> str:
    """
    Get the version line for the application.
    If the application is running in a Docker container, the hostname is appended to the version.
    """

    from configuration import HarvestConfiguration
    from text.styling import colorize, TextColors

    result = colorize(f'v{HarvestConfiguration.version}', color=TextColors.PROMPT)

    if is_dockerized():
        from socket import gethostname
        result += (colorize(" | ", color=TextColors.WARN)
                   + colorize(gethostname(), color=TextColors.INFO))

    return result


def get_prompt() -> str:
    """
    Generates the Harvest prompt.
    """

    args = [
        '\n',       # prompt always has a new line at the beginning for spacing
        '['
    ]

    from os import environ
    if environ.get("USER"):
        args.append(environ.get("USER"))
        args.append('@')

    if is_dockerized():
        from socket import gethostname
        args.append(gethostname())
        args.append(':')

    args.append('harvest')

    args.append('] ')

    result = colorize(''.join(args), color=TextColors.PROMPT)

    return result


def is_dockerized() -> bool:
    """
    Check if the application is running in a Docker container.
    """
    from os import path
    return path.exists('/.dockerenv')


def upload_files(parent: Any, paths: List[str], api_path: str, max_workers: int = None, yes: bool = False, description: str = None):
    """
    Upload files to the cache.
    Args:
        parent: Parent process calling the upload.
        paths: Globs of files to upload.
        api_path: API path to upload the files to.
        max_workers: Maximum number of threads to use.
        yes: Automatically confirm the upload.
        description: Description of the upload process.

    Returns:
        None
    """

    from glob import glob
    from messages import add_message

    def read_file(p: str) -> List[dict] or None:
        from json import load
        try:
            with open(p, 'r') as stream:
                return load(stream)

        except Exception as ex:
            return None

    from processes import ThreadPool
    from os.path import abspath, expanduser, isfile

    files = [
        abspath(file)
        for path in paths
        for file in glob(abspath(expanduser(path)))
        if isfile(file) and file.endswith('.json')
    ]

    from text.printing import print_message
    if files:
        from text.inputs import input_boolean
        confirm = input_boolean(f'Are you sure you want to upload {len(files)} files?', yes_argument=yes)

        if not confirm:
            print_message('Upload cancelled.', color='WARN')
            return

        pool = ThreadPool(name='Upload',
                          description=description or f'Uploading {len(files)} files to the cache',
                          max_workers=max_workers,
                          alert_on_complete=True)

        for file in files:
            j = read_file(file)
            if isinstance(j, (dict, list)):
                from api import HarvestRequest
                with HarvestRequest(path=api_path, method='POST', json=j) as hr:
                    pool.add(parent=hr, function=hr.query)

            else:
                add_message(parent, 'WARN', 'Invalid JSON format: ', file)

        pool.attach_progressbar()

    else:
        print_message('No files found to upload.', color='WARN')

    return
