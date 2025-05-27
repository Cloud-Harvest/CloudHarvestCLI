from cmd2 import with_default_category, CommandSet, with_argparser
from typing import List
from argparse import Namespace

from CloudHarvestCLI.messages import add_message
from CloudHarvestCLI.commands.report.arguments import report_parser

@with_default_category('Harvest')
class ReportCommand(CommandSet):

    @with_argparser(report_parser)
    def do_report(self, args):
        from CloudHarvestCLI.text.printing import print_task_response
        from CloudHarvestCLI.messages import print_message

        try:
            from CloudHarvestCLI.api import request
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
                passable_args['variables'] = {
                    var.split('=')[0]: var.split('=')[1] for var in
                    args.variables or []
                    if '=' in var
                }

                output = request(request_type='post', endpoint=endpoint, data=passable_args)

                if not output:
                    add_message(self, 'ERROR', True, 'No response from the server.')
                    return

                if output.get('reason') != 'OK':
                    add_message(self, 'ERROR', True, 'Could not generate the report.', output.get('reason'))
                    return

                request_id = output.get('result', {}).get('id')

                from CloudHarvestCLI.processes import HarvestRemoteJobAwaiter
                HarvestRemoteJobAwaiter(
                    endpoint=f'tasks/get_task_status/{request_id}',
                    with_progress_bar=True
                ).run()

                # Get the report results
                output = request(request_type='get', endpoint=f'tasks/get_task_result/{request_id}', data={'pop': True})
                output = output.get('result') or {}
                if output.get('errors'):
                    for error in output.get('errors'):
                        add_message(self, 'ERROR', True, error.get('message'))

                if args.refresh > 0:
                    from rich.live import Live
                    from os import system

                    system('clear -x')

                    from datetime import datetime
                    print_message(text=f'{args.report_name}: {datetime.now()} | refresh {args.refresh}/seconds',
                                  color='INFO',
                                  as_feedback=True)

                    print_task_response(report_response=output, args=args)

                    from time import sleep
                    sleep(args.refresh)

                else:
                    print_task_response(report_response=output, args=args)
                    break

        except KeyboardInterrupt:
            print_message('Keyboard interrupt acknowledged.', color='INFO', as_feedback=True)
            return

    @staticmethod
    def _load_file(filename: str):
        from CloudHarvestCLI.text.formatting import get_formatter

        extension = filename.split('.')[-1]
        converter = get_formatter(method='from', extension=extension)

        if converter:
            return converter(filename=filename)

        else:
            from CloudHarvestCLI.exceptions import HarvestClientException
            return HarvestClientException(f'Harvest does not support files with the `{extension}` extension.',
                                          log_level='warning')
