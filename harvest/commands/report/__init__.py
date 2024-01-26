from cmd2 import CommandSet, with_default_category, with_argparser
from logging import getLogger

from commands.report.arguments import report_parser

logger = getLogger('harvest')


@with_default_category('Harvest')
class ReportCommand(CommandSet):

    @with_argparser(report_parser)
    def do_report(self, args):
        from api import HarvestRequest
        from text.formatting import print_output
        from text.styling import TextColors, colorize

        r = HarvestRequest(path='reports/list').query()

        if r:
            print_output(data=r, keys=['name', 'description'])

        else:
            self._cmd.pfeedback(colorize('no reports found', TextColors.WARN))

