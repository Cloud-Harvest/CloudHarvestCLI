from cmd2 import Cmd2ArgumentParser
from rich_argparse import RawTextRichHelpFormatter
from CloudHarvestCLI.commands.services.completers import *

services_completer = ServicesCompleter()

# base parser
parser = Cmd2ArgumentParser(formatter_class=RawTextRichHelpFormatter)
subparser = parser.add_subparsers()

# services attach
services_attach_parser = Cmd2ArgumentParser(formatter_class=RawTextRichHelpFormatter)
services_attach_parser.add_argument('name',
                                    completer=services_completer.run,
                                    help='The name of a process.')
services_attach_parser.add_argument('--show-subtasks',
                                    action='store_true',
                                    help='Show individual subtask progress bars.')

# services kill
services_kill_parser = Cmd2ArgumentParser(formatter_class=RawTextRichHelpFormatter)
services_kill_parser.add_argument('names',
                                  nargs='*',
                                  completer=services_completer.run,
                                  help='One or more processes to terminate.')


# services list
services_list_parser = Cmd2ArgumentParser(formatter_class=RawTextRichHelpFormatter)
