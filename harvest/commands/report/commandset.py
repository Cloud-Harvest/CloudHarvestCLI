from cmd2 import with_default_category, CommandSet, with_argparser
from .arguments import report_parser
from .exceptions import HarvestReportException


@with_default_category('Harvest')
class ReportCommand(CommandSet):

    @with_argparser(report_parser)
    def do_report(self, args):
        from os.path import expanduser, exists
        from text.printing import print_message, print_data

        keys = []
        if args.report_name_or_file == 'list':
            keys = ['name', 'description']
            output = self._list_reports()

        elif exists(expanduser(args.report_name_or_file)):
            filename = expanduser(args.report_name_or_file)
            print_message(f'Loading data from {filename}', color='INFO', as_feedback=True)

            output = self._load_file(filename=filename)

        else:
            from api import HarvestRequest
            output = HarvestRequest(path='reports/run', json=dict(vars(args))).query()

        if isinstance(output, dict):
            # this indicates an error state but query error states are already printed from HarvestRequest.api()
            # More specific errors should be described here.
            from messages import add_message
            add_message(__name__, 'ERROR', output.get('error'))

        else:
            print_data(data=output,
                       keys=keys or args.header_order,
                       output_format=args.format,
                       flatten=args.flatten,
                       unflatten=args.unflatten,
                       page=args.page,
                       with_record_count=True)

    @staticmethod
    def _list_reports():
        from api import HarvestRequest

        report_list = HarvestRequest(path='reports/list').query()

        if report_list:
            return report_list

        else:
            return HarvestReportException('No reports found.', log_level='warning')

    @staticmethod
    def _load_file(filename: str):
        from text.formatting import get_formatter

        extension = filename.split('.')[-1]
        converter = get_formatter(method='from', extension=extension)

        if converter:
            return converter(filename=filename)

        else:
            return HarvestReportException(f'Harvest does not support files with the `{extension}` extension.',
                                          log_level='warning')
