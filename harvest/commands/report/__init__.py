from cmd2 import CommandSet, with_default_category, with_argparser
from logging import getLogger

from commands.report.arguments import report_parser

logger = getLogger('harvest')


@with_default_category('Harvest')
class ReportCommand(CommandSet):

    @with_argparser(report_parser)
    def do_report(self, args):
        from os.path import expanduser, exists
        from text.printing import print_feedback, print_data

        keys = []
        if args.report_name_or_file == 'list':
            keys = ['name', 'description']
            output = self._list_reports()

        elif exists(expanduser(args.report_name_or_file)):
            filename = expanduser(args.report_name_or_file)
            print_feedback(f'Loading data from {filename}', color='INFO')

            output = self._load_file(filename=filename)

        else:
            from api import HarvestRequest
            output = HarvestRequest(path='report/run', params=args).query()

        if isinstance(output, tuple):
            text, color = output
            print_feedback(text=text, color=color)

        else:
            print_data(data=output,
                       keys=keys or args.header_order,
                       output_format=args.format,
                       flatten=args.flatten,
                       unflatten=args.unflatten,
                       page=args.page)

    def _list_reports(self):
        from api import HarvestRequest

        report_list = HarvestRequest(path='reports/list').query()

        if report_list:
            return report_list

        else:
            return 'No reports found.', 'WARN'

    def _load_file(self, filename: str):
        from text.formatting import get_formatter

        extension = filename.split('.')[-1]
        converter = get_formatter(method='from', extension=extension)

        if converter:
            return converter(filename=filename)

        else:
            return f'Harvest does not support files with the `{extension}` extension.', 'WARN'
