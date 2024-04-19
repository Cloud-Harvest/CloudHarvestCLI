from cmd2 import with_default_category, CommandSet, with_argparser
from .arguments import report_parser
from .exceptions import HarvestReportException


@with_default_category('Harvest')
class ReportCommand(CommandSet):

    @with_argparser(report_parser)
    def do_report(self, args):
        # from os.path import expanduser, exists
        from text.printing import print_message, print_data

        if args.report_name == 'list':
            output = self._list_reports()

        # elif exists(expanduser(args.report_name)):
        #     filename = expanduser(args.report_name)
        #     print_message(f'Loading data from {filename}', color='INFO', as_feedback=True)
        #
        #     output = self._load_file(filename=filename)

        else:
            input_variables = dict(vars(args))

            from api import HarvestRequest
            output = HarvestRequest(path='reports/run', json={
                k: v for k,  v in input_variables.items()
                if not k.startswith('cmd2')
            }).query()

        if not isinstance(output, dict):
            return

        error = output.get('error') or {}
        data = output.get('data') or {}
        meta = output.get('meta') or {}

        if error:
            print_message(text=output['error'], color='ERROR', as_feedback=True)

        if data:
            print_data(data=output['data'],
                       keys=args.header_order or meta.get('headers'),
                       output_format='pretty-json' if args.describe else args.format,
                       flatten=args.flatten,
                       unflatten=args.unflatten,
                       page=args.page,
                       with_record_count=False)

        if meta:
            if isinstance(meta, list):
                print_message(text=' '.join(meta), color='WARN', as_feedback=True)

            else:
                print_message(text=f'{len(data)} '
                                   + f'records in {meta["duration"]} seconds'
                                     if meta.get('duration') else '',
                              color='INFO',
                              as_feedback=True)

            # from api import HarvestRequest
            # test_request = HarvestRequest(path='/test/aws').query()
            # print(test_request)

    @staticmethod
    def _list_reports() -> dict or Exception:
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
