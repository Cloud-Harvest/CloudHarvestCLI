from cmd2 import with_default_category, CommandSet, with_argparser
from typing import List
from argparse import Namespace
from .arguments import report_parser

@with_default_category('Harvest')
class ReportCommand(CommandSet):

    @with_argparser(report_parser)
    def do_report(self, args):
        from text.printing import print_message

        if args.report_name == 'list':
            output = self._list_reports()
            self._print_report_output(output=output, args=args, list_separator=', ')
            return

        try:
            while True:
                output = HarvestRequest(path='reports/run', json=args).query()

                if not isinstance(output, list):
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
    def _print_report_output(output: List[dict], args: Namespace, **kwargs):
        from text.printing import print_message, print_data

        if not isinstance(output, list):
            return

        for o in output:
            error = o.get('error') or {}
            data = o.get('data') or {}
            meta = o.get('meta') or {}
    
            if error:
                print_message(text=o['error'], color='ERROR', as_feedback=True)
    
            if data:
                print_data(data=o['data'],
                           keys=args.header_order or meta.get('headers'),
                           title=meta.get('title'),
                           output_format='pretty-json' if args.describe else (args.format or 'table'),
                           flatten=args.flatten,
                           unflatten=args.unflatten,
                           page=args.page,
                           with_record_count=False,
                           **kwargs)
    
            if meta:
                if isinstance(meta, list):
                    print_message(text=' '.join(meta), color='WARN', as_feedback=True)
    
                else:
                    print_message(text=f'{len(data)} '
                                       + f'records in {meta["duration"]:.2f} seconds'
                                         if meta.get('duration') else '',
                                  color='INFO',
                                  as_feedback=True)
