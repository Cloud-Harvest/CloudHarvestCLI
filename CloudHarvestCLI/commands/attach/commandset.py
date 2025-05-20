from CloudHarvestCLI.commands.attach.arguments import attach_parser

from cmd2 import with_default_category, CommandSet, with_argparser


@with_default_category('Harvest')
class AttachCommand(CommandSet):
    @with_argparser(attach_parser)
    def do_attach(self, args):
        task_id = args.job_id[5:] if args.job_id.startswith('task:') else args.job_id

        from CloudHarvestCLI.processes import HarvestRemoteJobAwaiter
        HarvestRemoteJobAwaiter(endpoint=f'tasks/get_task_status/{task_id}',
                                with_progress_bar=True,
                                timeout=args.timeout).run()
