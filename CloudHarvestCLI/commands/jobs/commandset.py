from CloudHarvestCLI.commands.jobs.arguments import jobs_parser

from cmd2 import with_default_category, CommandSet, with_argparser


@with_default_category('Harvest')
class JobsCommand(CommandSet):

    @with_argparser(jobs_parser)
    def do_jobs(self, args):
        if not args.subcommand:
            from CloudHarvestCLI.messages import print_message
            print_message('ERROR', True, 'Please specify a subcommand for the "jobs" command.')
            jobs_parser.print_help()
