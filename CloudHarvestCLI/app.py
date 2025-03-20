from cmd2 import Cmd, DEFAULT_SHORTCUTS
from cmd2.plugin import PrecommandData, PostcommandData
from logging import getLogger

from CloudHarvestCorePluginManager import register_all
from CloudHarvestCLI.banner import get_banner
from CloudHarvestCLI.configuration import HarvestConfiguration
from CloudHarvestCLI.text import console
from CloudHarvestCLI.text.styling import colorize, TextColors

# Activate any objects which are registered with the PluginManager Registry or cmd2.Cmd on definition. This is necessary
# to populate the commands available to a user.
from CloudHarvestCLI.__register__ import *

logger = getLogger('harvest')

# Make the application instance available to the entire application
HARVEST_CLI = None


class Harvest(Cmd):
    def __init__(self, **kwargs):
        global HARVEST_CLI
        HARVEST_CLI = self

        # Load the configuration
        HarvestConfiguration.load()

        from CloudHarvestCLI.api import Api
        Api.config(host=HarvestConfiguration.api.get('host'),
                   port=HarvestConfiguration.api.get('port'),
                   pem=HarvestConfiguration.api.get('pem'),
                   verify=HarvestConfiguration.api.get('verify'))

        if not Api.verify:
            from CloudHarvestCLI.messages import add_message
            add_message(self, 'WARN', True, 'API SSL verification is disabled. This is a security risk.')

        # Load installed plugins
        register_all()

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
        self.prompt = get_prompt()

        console.print()  # provides a space between the first line and the banner
        console.print(self._banner[0])
        if self._banner[1]:
            console.print(self._banner[1])

        self.pfeedback(get_load_version_line())

        # print any messages generated during load
        from CloudHarvestCLI.messages import print_all_messages
        print_all_messages()

        # start background processes
        self.last_command_timestamp = None
        self._start_notify_unread_messages_thread()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return None

    def _pre_command_hook(self, data: PrecommandData) -> PrecommandData:
        logger.debug(f'command: {data.statement.raw}')

        self.last_command_timestamp = None
        return data

    def _post_command_hooks(self, data: PostcommandData) -> PostcommandData:
        try:
            from CloudHarvestCLI.messages import print_all_messages
            print_all_messages()

        finally:
            from datetime import datetime
            self.last_command_timestamp = datetime.now().timestamp()

            return data

    def _start_notify_unread_messages_thread(self):
        def _thread():
            from datetime import datetime
            from CloudHarvestCLI.messages import Messages, print_all_messages
            from time import sleep
            while True:

                if self.last_command_timestamp:
                    if Messages.queue and self.last_command_timestamp > (datetime.now().timestamp() + 300):
                        print_all_messages()

                sleep(1)

        from CloudHarvestCLI.processes import HarvestThread
        t = HarvestThread(**{
            'name': 'message_monitor',
            'description': 'Delivers messages to users after commands are executed or when the system is idle.',
            'target': _thread,
            'daemon': True
        })

        from CloudHarvestCLI.processes import ConcurrentProcesses
        ConcurrentProcesses.add(t)

        t.start()

def get_load_version_line() -> str:
    """
    Get the version line for the application.
    If the application is running in a Docker container, the hostname is appended to the version.
    """

    from CloudHarvestCLI.configuration import HarvestConfiguration
    from CloudHarvestCLI.text.styling import colorize, TextColors

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
