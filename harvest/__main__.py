#!/usr/bin/env python
# package imports
from cmd2 import Cmd, DEFAULT_SHORTCUTS
from cmd2.plugin import PrecommandData, PostcommandData
from rich.console import Console

# harvest imports
import configuration
from banner import get_banner
from text.styling import colorize, TextColors

from commands import BannerCommand, ReportCommand


class Harvest(Cmd):
    def __init__(self, **kwargs):
        self.configuration = configuration.load()

        # _console is used to print certain objects
        self._console = Console()

        # _banners display loading banners
        self._banner = get_banner(banner_configuration=self.configuration['banners'])

        # application version
        self._version = self.configuration['version']

        shortcuts = DEFAULT_SHORTCUTS | self.configuration.get('shortcuts') or {}

        from os.path import expanduser
        super().__init__(persistent_history_file=expanduser('~/.harvest/history'),
                         persistent_history_length=5000000,
                         shortcuts=shortcuts,
                         **kwargs)

        self.register_precmd_hook(self._pre_command_hook)
        self.register_postcmd_hook(self._post_command_hooks)

        # the prompt will always have a new line at the beginning for spacing
        self.prompt = colorize('\n[harvest] ', color=TextColors.PROMPT)

        self._console.print()  # provides a space between the first line and the banner
        self._console.print(self._banner)
        self.pfeedback(colorize(f'v{self._version}', color=TextColors.HEADER))

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return None

    def _pre_command_hook(self, data: PrecommandData) -> PrecommandData:

        return data

    def _post_command_hooks(self, data: PostcommandData) -> PostcommandData:
        from messages import Messages
        for message in Messages.read():
            text, color = message

            self.pfeedback(colorize(text=text, color=color))

        return data


if __name__ == '__main__':
    with Harvest() as harvest:
        harvest.cmdloop()
