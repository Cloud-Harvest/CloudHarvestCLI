from cmd2 import Cmd2ArgumentParser
from cmd2 import Cmd

from commands.arguments.parts import pstar_parser, thread_parser
from rich_argparse import RawTextRichHelpFormatter

# base parser
parser = Cmd2ArgumentParser(formatter_class=RawTextRichHelpFormatter)
subparser = parser.add_subparsers()

# cache collect
collect_parser = Cmd2ArgumentParser(formatter_class=RawTextRichHelpFormatter,
                                    parents=[pstar_parser])

# cache map
map_parser = Cmd2ArgumentParser(formatter_class=RawTextRichHelpFormatter,
                                parents=[pstar_parser])

# cache upload command
upload_parser = Cmd2ArgumentParser(formatter_class=RawTextRichHelpFormatter,
                                   parents=[pstar_parser, thread_parser])
upload_parser.add_argument('paths', nargs='*', completer=Cmd.path_complete,
                           help='Path containing the file(s) to upload.')
