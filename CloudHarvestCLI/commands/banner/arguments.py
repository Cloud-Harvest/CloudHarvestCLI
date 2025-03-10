from cmd2 import Cmd2ArgumentParser
from rich_argparse import RawTextRichHelpFormatter

from CloudHarvestCLI.commands.banner.completers import BannerCompleter


banner_completer = BannerCompleter()
banner_parser = Cmd2ArgumentParser(formatter_class=RawTextRichHelpFormatter)
banner_parser.add_argument('names', type=str, nargs='*', completer=banner_completer.run,
                           help='The name of the report to display. When not provided, all banners are displayed.')
banner_parser.add_argument('--text', type=str, default='HARVEST',
                           help='Allows the user to display arbitrary text using the banner code.')
