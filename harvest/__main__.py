#!/usr/bin/env python

from cmd2 import Cmd, with_argparser
from rich.console import Console
from arguments import report_subparser
from banner import get_banner
from startup import prepare


class Harvest(Cmd):
    def __init__(self, **kwargs):
        self.configuration = prepare()
        self.console = Console()
        self.banner = get_banner(banner_configuration=self.configuration['banners'])
        self.version = self.configuration['version']

        super().__init__(**kwargs)

        self.prompt = '\n[harvest] '

        self.console.print(self.banner)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return None

    @with_argparser(report_subparser)
    def do_report(self, args):
        pass


if __name__ == '__main__':
    with Harvest() as harvest:
        harvest.cmdloop()
