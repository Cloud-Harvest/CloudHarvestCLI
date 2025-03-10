from cmd2 import with_default_category, CommandSet, with_argparser
from typing import List
from argparse import Namespace

from CloudHarvestCLI.messages import add_message
from CloudHarvestCLI.commands.report.arguments import report_parser

@with_default_category('Harvest')
class ReportCommand(CommandSet):

    @with_argparser(report_parser)
    def do_report(self, args):
        from messages import print_message

        if args.report_name == 'list':
            output = self._list_reports()

            self._print_report_output(report_response=output, args=args, list_separator=', ')
            return

        try:
            from api import request
            while True:
                endpoint = f'tasks/queue/1/reports/{args.report_name}'

                # Arguments which will be sent to the TaskChain via the Api
                passable_args = {}

                # Not filters: describe, flatten, unflatten, page, and timeout
                # Filters: add_keys, count, exclude_keys, header_order, limit, matches, sort
                # Constructs the user-defined filters which will be passed to the TaskChain
                filters = {
                    'add_keys': args.add_keys,
                    'count': args.count,
                    'exclude_keys': args.exclude_keys,
                    'headers': args.header_order,
                    'limit': args.limit,
                    'matches': args.matches,
                    'sort': args.sort,
                }

                # Add the filters to the passable arguments
                passable_args['filters'] = filters

                output = request(request_type='post', endpoint=endpoint, data=passable_args)

                if output.get('reason') != 'OK':
                    add_message(self, 'ERROR', True, 'Could not generate the report.', output.get('reason'))
                    return

                request_id = output.get('result', {}).get('id')

                # Check the API for the task results
                from datetime import datetime
                start_time = datetime.now()
                while True:
                    output = request(request_type='get', endpoint=f'/tasks/get_task_results/{request_id}')
                    reason = output.get('reason')

                    match reason:
                        case 'OK':
                            break

                        case 'NOT FOUND':
                            from time import sleep
                            sleep(1)

                    if (datetime.now() - start_time).total_seconds() > args.timeout:
                        add_message(self, 'WARN', True, f'Task {request_id} took too long to complete.')
                        return

                output = output.get('result') or {}

                if not isinstance(output.get('data'), list):
                    return

                if args.refresh > 0:
                    from rich.live import Live
                    from os import system

                    system('clear -x')

                    from datetime import datetime
                    print_message(text=f'{args.report_name}: {datetime.now()} | refresh {args.refresh}/seconds',
                                  color='INFO',
                                  as_feedback=True)

                    self._print_report_output(report_response=output, args=args)

                    from time import sleep
                    sleep(args.refresh)

                else:
                    self._print_report_output(report_response=output, args=args)
                    break

        except KeyboardInterrupt:
            print_message('Keyboard interrupt acknowledged.', color='INFO', as_feedback=True)
            return

    @staticmethod
    def _list_reports() -> list:
        from api import request

        report_list = request('get', 'tasks/list_available_tasks/reports').get('result') or []

        return report_list or []

    @staticmethod
    def _load_file(filename: str):
        from text.formatting import get_formatter

        extension = filename.split('.')[-1]
        converter = get_formatter(method='from', extension=extension)

        if converter:
            return converter(filename=filename)

        else:
            from exceptions import HarvestClientException
            return HarvestClientException(f'Harvest does not support files with the `{extension}` extension.',
                                          log_level='warning')

    @staticmethod
    def _print_report_output(report_response: List[dict] or dict, args: Namespace, **kwargs):
        from text.printing import print_data
        from messages import print_message

        if isinstance(report_response, list):
            # Recursively print each report in the list
            [
                ReportCommand._print_report_output(report_response=report, args=args, **kwargs)
                for report in report_response
            ]

        elif isinstance(report_response, dict):
            errors = report_response.get('errors') or []
            data = report_response.get('data') or {}
            meta = report_response.get('meta') or {}
            metrics = report_response.get('metrics') or {}

            if data:
                print_data(data=report_response['data'],
                           keys=meta.get('headers'),
                           title=meta.get('title'),
                           output_format='pretty-json' if args.describe else (args.format or 'table'),
                           flatten=args.flatten,
                           unflatten=args.unflatten,
                           page=args.page,
                           with_record_count=False,
                           **kwargs)

            if errors:
                for error in errors:
                    for key, value in error.items():
                        print_message(text=f'{key}: {value}', color='ERROR', as_feedback=True)

            if metrics and metrics[-1].get('Duration'):
                    print_message(text=f'{len(data)} records in {metrics[-1]["Duration"] * 1000:.2f} ms',
                                  color='INFO',
                                  as_feedback=True)
