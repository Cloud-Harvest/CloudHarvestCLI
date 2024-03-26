from cmd2 import Cmd2ArgumentParser
from rich_argparse import RawTextRichHelpFormatter


# base parser
parser = Cmd2ArgumentParser(formatter_class=RawTextRichHelpFormatter)
subparser = parser.add_subparsers()
