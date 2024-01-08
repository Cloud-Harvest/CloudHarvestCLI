#!/usr/bin/env python

from cmd2 import Cmd, with_argparser
from arguments import report_subparser


class Harvest(Cmd):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.prompt = '[harvest] '

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
