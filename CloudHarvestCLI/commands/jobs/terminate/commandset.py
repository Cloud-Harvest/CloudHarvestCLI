from CloudHarvestCLI.commands.jobs.terminate.arguments import terminate_parser

def do_terminate(args):
    # TODO: Implement the logic to terminate a job.

    from CloudHarvestCLI.messages import print_message
    print_message('ERROR', True, 'This command is not implemented yet. Please check back later.')
    return

    # task_id = args.job_id[5:] if args.job_id.startswith('task:') else args.job_id
    #
    # from CloudHarvestCLI.processes import HarvestRemoteJobAwaiter
    # HarvestRemoteJobAwaiter(
    #     endpoint=f'tasks/get_task_status/{task_id}',
    #     with_progress_bar=True,
    #     timeout=args.timeout
    # ).run()
