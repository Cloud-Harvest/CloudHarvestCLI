from cmd2 import with_default_category, CommandSet, with_argparser, as_subcommand_to
from processes import ConcurrentProcesses
from .arguments import parser, services_attach_parser, services_kill_parser, services_list_parser


@with_default_category('Harvest')
class ServicesCommand(CommandSet):
    @with_argparser(parser)
    def do_services(self, args):
        from commands.base import get_subtask
        get_subtask(parent=self, parser=parser, args=args)

    @as_subcommand_to('services', 'attach', services_attach_parser, help='Attach a progress bar to a running job.')
    def attach(self, args):
        from messages import print_message

        for process in ConcurrentProcesses.objects:
            if process.name == args.name and hasattr(process, 'attach_progressbar'):
                process.attach_progressbar()

            else:
                print_message(text=f'No eligible running processes named `{args.name}`.',
                              color='INFO',
                              as_feedback=True)

    @as_subcommand_to('services', 'kill', services_kill_parser, help='Stop jobs.')
    def kill(self, args):
        from messages import print_message

        for process in ConcurrentProcesses.objects:
            if process.name in args.names and hasattr(process, 'kill'):
                process.kill()
                print_message(text=f'Sent kill command to `{process.name}`.', color='WARN', as_feedback=True)

            else:
                print_message(text=f'No eligible running processes named `{args.names}`.',
                              color='INFO',
                              as_feedback=True)

    @as_subcommand_to('services', 'list', services_list_parser, help='Get a list of running jobs')
    def list(self, args):
        from text.printing import print_data

        keys, data = ConcurrentProcesses().report()
        print_data(data=data, keys=keys)
