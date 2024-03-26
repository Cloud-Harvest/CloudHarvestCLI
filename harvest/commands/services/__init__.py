from cmd2 import CommandSet, with_default_category, with_argparser
from .arguments import parser


@with_default_category('Harvest')
class ServicesCommand(CommandSet):
    @with_argparser(parser)
    def do_services(self, args):
        from processes import ConcurrentProcesses
        from text.printing import print_data

        print_data(data=ConcurrentProcesses().report(), keys=['Name', 'Status'])
