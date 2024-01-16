#!/usr/bin/env python

from cmd2 import Cmd, with_argparser
from rich.console import Console
from arguments import banner_parser, report_parser
from banner import get_banner
from startup import prepare
from text import stylize, colorize, TextColors


class Harvest(Cmd):
    def __init__(self, **kwargs):
        self.configuration = prepare()
        self.console = Console()
        self.banner = get_banner(banner_configuration=self.configuration['banners'])
        self.version = self.configuration['version']

        from os.path import expanduser
        super().__init__(persistent_history_file=expanduser('~/.harvest/history'),
                         persistent_history_length=5000000,
                         **kwargs)

        self.prompt = colorize('\n[harvest] ', color=TextColors.PROMPT)

        self.console.print()  # provides a space between the first line and the banner
        self.console.print(self.banner)

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
            self.console.print(f'\n {name}----------')
            self.console.print(banner)

    @with_argparser(report_parser)
    def do_report(self, args):
        pass


if __name__ == '__main__':
    with Harvest() as harvest:
        harvest.cmdloop()
