from cmd2 import with_default_category, CommandSet, with_argparser
from argparse import Namespace
from .arguments import report_parser
from .exceptions import HarvestReportException


@with_default_category('Harvest')
class ReportCommand(CommandSet):

    @with_argparser(report_parser)
    def do_report(self, args):
        from text.printing import print_message

        if args.report_name == 'list':
            output = self._list_reports()
            self._print_report_output(output=output, args=args)

            return

        try:
            while True:
                from api import HarvestRequest
                output = HarvestRequest(path='reports/run', json=args).query()

                if not isinstance(output, dict):
                    return

                if args.refresh > 0:
                    from rich.live import Live
                    from os import system

                    system('clear -x')

                    from datetime import datetime
                    print_message(text=f'{args.report_name}: {datetime.now()} | refresh {args.refresh}/seconds',
                                  color='INFO',
                                  as_feedback=True)

                    self._print_report_output(output=output, args=args)

                    if len(output['data']) == 0:
                        print_message('No data found. Stopping refresh.', color='WARN', as_feedback=True)
                        break

                    from time import sleep
                    sleep(args.refresh)

                else:
                    self._print_report_output(output=output, args=args)
                    break

        except KeyboardInterrupt:
            print_message('Keyboard interrupt acknowledged.', color='INFO', as_feedback=True)
            return

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

    @staticmethod
    def _print_report_output(output: dict, args: Namespace):
        from text.printing import print_message, print_data

        error = output.get('error') or {}
        data = output.get('data') or {}
        meta = output.get('meta') or {}

        if error:
            print_message(text=output['error'], color='ERROR', as_feedback=True)

        if data:
            print_data(data=output['data'],
                       keys=args.header_order or meta.get('headers'),
                       output_format='pretty-json' if args.describe else (args.format or 'table'),
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
