from cmd2 import with_default_category, CommandSet, with_argparser, as_subcommand_to
from .arguments import parser, services_attach_parser, services_list_parser


@with_default_category('Harvest')
class ServicesCommand(CommandSet):
    @with_argparser(parser)
    def do_services(self, args):
        from commands.base import get_subtask
        get_subtask(parent=self, parser=parser, args=args)

    @as_subcommand_to('services', 'attach', services_attach_parser, help='Attach a progress bar to a running job.')
    def attach(self, args):
        from processes import ConcurrentProcesses

    @as_subcommand_to('services', 'list', services_list_parser, help='Get a list of running jobs')
    def list(self, args):
        from processes import ConcurrentProcesses
        from text.printing import print_data

        keys, data = ConcurrentProcesses().report()
        print_data(data=data, keys=keys)
