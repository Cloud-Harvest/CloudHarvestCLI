from cmd2 import with_default_category, CommandSet, with_argparser
from typing import List
from argparse import Namespace

from CloudHarvestCLI.messages import add_message
from CloudHarvestCLI.commands.report.arguments import report_parser
from text.printing import print_data


@with_default_category('Harvest')
class ReportCommand(CommandSet):

    @with_argparser(report_parser)
    def do_report(self, args):
        from CloudHarvestCLI.text.printing import print_task_response
        from CloudHarvestCLI.messages import print_message

        try:
            from CloudHarvestCLI.api import request
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
            passable_args['describe'] = args.describe
            passable_args['filters'] = filters
            passable_args['variables'] = {
                var.split('=')[0]: var.split('=')[1] for var in
                args.variables or []
                if '=' in var
            }

            # Initiate the report printing loop. This loop will continue to print the report until the user
            # interrupts it or if the report is not set to refresh.
            while True:
                # Queue the report generation task
                output = request(request_type='post', endpoint=endpoint, data=passable_args)

                if not output:
                    add_message(self, 'ERROR', True, 'No response from the server.')
                    return

                if output.get('reason') != 'OK':
                    add_message(self, 'ERROR', True, 'Could not generate the report.', output.get('reason'))
                    return

                # Get the request ID to monitor the task status
                request_id = output.get('result', {}).get('id')

                # Monitor the task until it is complete
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
                        add_message(self, 'ERROR', True, error)

                # Determine the refresh interval based on the user's input. Prefer --refresh over --refresh-all.
                refresh_interval = args.refresh or args.refresh_all

                if refresh_interval:
                    # Clear the terminal for the refreshed report.
                    from os import system
                    system('clear -x')

                    # Print the report header if the report is refreshing.
                    from datetime import datetime
                    print_message('INFO', True, f'{args.report_name}: {datetime.now()} | refresh {refresh_interval}/seconds')

                # Print the report contents
                print_task_response(report_response=output, args=args)

                # Escape the refresh loop if no refresh interval is set.
                if not refresh_interval:
                    break

                # Escape the loop if no data is returned and --refresh-all is not set.
                if not output.get('data') and not args.refresh_all:
                    print_message('WARNING', True, 'The report did not return any data. Ending refresh.')
                    break

                # Wait for the specified refresh interval before refreshing the report.
                from time import sleep
                sleep(refresh_interval)

                # Enqueue a data collection task to update the report data.
                data_collection_output = request(
                    request_type='post',
                    endpoint=f'pstar/queue_unique_identifiers/2',
                    data={
                        'full_refresh': args.refresh_all > 0,      # Refreshes the entire collection, not just the singletons.
                        'unique_identifiers': [
                            record['Harvest']['UniqueIdentifier']
                            for record in output.get('data') or []
                        ]
                    }
                )

                # Get the data collection request ID
                data_collection_request_id = data_collection_output.get('result', {}).get('parent_id')

                # Warn the user if any records were not queued for data collection.
                not_queued = data_collection_output.get('result', {}).get('not_queued', [])
                if not_queued:
                    print_message('WARNING', True, f'The following records were not queued for data collection: {not_queued}')
                    print_data(data=not_queued, keys=['unique_identifier', 'reason'], as_feedback=True)

                # If we could not queue the data collection task, exit the refresh loop.
                if not data_collection_request_id or not data_collection_output.get('result', {}).get('queued_tasks'):
                    print_message('ERROR', True, 'Could not queue data collection task to refresh the report. Ending refresh.')
                    return

                # Wait for the data collection task to complete before refreshing the report. This ensures that
                # the report is refreshed with the latest data.
                HarvestRemoteJobAwaiter(
                    endpoint=f'tasks/get_task_status/{data_collection_request_id}',
                    with_progress_bar=True
                ).run()

        except KeyboardInterrupt:
            print_message('INFO', True, 'Keyboard interrupt acknowledged.')
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
