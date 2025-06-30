from CloudHarvestCLI.commands.jobs.arguments import jobs_parser

from cmd2 import with_default_category, CommandSet, with_argparser


@with_default_category('Harvest')
class JobsCommand(CommandSet):

    @with_argparser(jobs_parser)
    def do_jobs(self, args):
        match str(args.subcommand):
            case 'attach':
                from CloudHarvestCLI.commands.jobs.attach.commandset import do_attach
                do_attach(args)

            case 'terminate':
                from CloudHarvestCLI.commands.jobs.terminate.commandset import do_terminate
                do_terminate(args)

            case _:
                from CloudHarvestCLI.messages import print_message
                print_message('ERROR', True, 'Please specify a subcommand for the "jobs" command.')
                jobs_parser.print_help()
