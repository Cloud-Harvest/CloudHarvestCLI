from cmd2 import with_default_category, CommandSet, with_argparser

from CloudHarvestCLI.messages import add_message
from CloudHarvestCLI.commands.harvest.arguments import harvest_parser
from messages import print_message
from text.styling import TextColors


@with_default_category('Harvest')
class HarvestCommand(CommandSet):

    @with_argparser(harvest_parser)
    def do_harvest(self, args):
        """

        """
        from datetime import datetime
        from CloudHarvestCLI.api import request

        start = datetime.now()

        request_arguments = {
            'platform': args.platform,
            'service': args.service,
            'type': args.type,
            'account': args.account,
            'region': args.region,
        }

        if args.list:
            endpoint = 'pstar/list_pstar'
            request_type = 'get'

        else:
            endpoint = 'pstar/queue_pstar/2'    # data collection tasks should be queued at the lowest priority
            request_type = 'post'

        request_response = request(request_type=request_type, endpoint=endpoint, data=request_arguments)

        end = datetime.now()

        # Escape if there's an error
        if request_response['success'] is False:
            add_message(self, 'ERROR', True, 'Error retrieving PSTAR information.', request_response['reason'])
            return

        from CloudHarvestCLI.text.printing import print_data

        # print a list of the pstar
        if args.list:
            keys = ['platform', 'service', 'type', 'account', 'region', 'template']

            print_data(data=request_response['result'], keys=keys, sort_by_keys=keys)

            add_message(self, 'INFO', True, f'Found {len(request_response["result"])} results in {(end - start).total_seconds()} seconds.')

        # Queue the services
        else:
            results = {}

            for result in request_response['result']['tasks']:
                if result['reason'] not in results:
                    results[result['reason']] = 0

                results[result['reason']] += 1

            # If all the results were okay, just print the number of tasks queued
            if len(results.keys()) == 1 and 'OK' in results.keys():
                print_message(f'Queued {results["OK"]} tasks in {(end - start).total_seconds()} seconds.', 'INFO', True)

            else:
                # Otherwise, print the queue error messages
                # Now convert the results into a table where each key is a new row
                printable_results = [
                    {
                        'reason': reason,
                        'count': count
                    }
                    for reason, count in results.items()
                ]

                # Print the results
                keys = ['reason', 'count']
                print_data(data=printable_results, keys=keys, sort_by_keys=keys)
                add_message(self, 'WARN', True, 'Some tasks failed to queue.', f'Successfully queued {results.get("OK", {}).get("count") or 0} out of {len(request_response["result"])} tasks.')

            request_parent_id = request_response['result']['parent']

            from CloudHarvestCLI.processes import HarvestRemoteJobAwaiter
            HarvestRemoteJobAwaiter(endpoint=f'tasks/get_task_status/{request_parent_id}', with_progress_bar=True, timeout=3600).run()
