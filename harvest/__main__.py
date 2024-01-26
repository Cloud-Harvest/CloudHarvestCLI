#!/usr/bin/env python
# package imports
from cmd2 import Cmd, with_argparser
from cmd2.plugin import PrecommandData, PostcommandData
from rich.console import Console

# harvest imports
from api import HarvestRequest, get_auth
import configuration
from arguments import banner_parser, report_parser
from banner import get_banner
from text.styling import colorize, TextColors


class Harvest(Cmd):
    def __init__(self, **kwargs):
        self.configuration = configuration.load()

        # _console is used to print certain objects
        self._console = Console()

        # _banners display loading banners
        self._banner = get_banner(banner_configuration=self.configuration['banners'])

        # application version
        self._version = self.configuration['version']

        from os.path import expanduser
        super().__init__(persistent_history_file=expanduser('~/.harvest/history'),
                         persistent_history_length=5000000,
                         **kwargs)

        self.register_precmd_hook(self._pre_command_hook)
        self.register_postcmd_hook(self._post_command_hooks)

        # the prompt will always have a new line at the beginning for spacing
        self.prompt = colorize('\n[harvest] ', color=TextColors.PROMPT)

        self._console.print()  # provides a space between the first line and the banner
        self._console.print(self._banner)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return None

    @with_argparser(banner_parser)
    def do_banner(self, args):
        if args.names:
            names = args.names

        else:
            names = self.configuration['banners'].keys()

        results = {
            name: get_banner(banner_configuration=self.configuration['banners'],
                             name=name,
                             text=args.text)
            for name in names
        }

        for name, banner in results.items():
            self._console.print(f'\n {name}----------')
            self._console.print(banner)

    @with_argparser(report_parser)
    def do_report(self, args):
        r = HarvestRequest(path='reports/list').query()

        if r:
            self._print_output(data=r, keys=['name', 'description'])

        else:
            self.pfeedback(colorize('no reports found', TextColors.WARN))

    def _pre_command_hook(self, data: PrecommandData) -> PrecommandData:

        return data

    def _post_command_hooks(self, data: PostcommandData) -> PostcommandData:
        from messages import Messages
        for message in Messages.read():
            text, color = message

            self.pfeedback(colorize(text=text, color=color))

        return data

    def _print_output(self, data: (list or dict), keys: list = None, flatten: str = None, unflatten: str = None, output_format: str = 'table'):
        from text.formatting import to_csv, to_json, to_table

        match output_format:
            case 'csv':
                self._console.print(to_csv(data=data, keys=keys))

            case 'json':
                self._console.print(to_json(data=data, keys=keys, flatten=flatten, unflatten=unflatten))

            case 'pretty-json':
                self._console.print_json(to_json(data=data, keys=keys, flatten=flatten, unflatten=unflatten))

            case 'table':
                self._console.print(to_table(data=data, keys=keys))

            case _:
                pass


if __name__ == '__main__':
    with Harvest() as harvest:
        harvest.cmdloop()
