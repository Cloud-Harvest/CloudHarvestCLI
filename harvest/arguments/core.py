from cmd2 import Cmd2ArgumentParser
from rich_argparse import RawTextRichHelpFormatter
from arguments.parents import *

banner_parser = Cmd2ArgumentParser(formatter_class=RawTextRichHelpFormatter)
banner_parser.add_argument('names', type=str, nargs='*',
                           help='The name of the report to display. When not provided, all banners are displayed.')
banner_parser.add_argument('--text', type=str, default='HARVEST',
                           help='Allows the user to display arbitrary text using the banner code.')

# reporting
report_parser = Cmd2ArgumentParser(formatter_class=RawTextRichHelpFormatter, parents=[key_manipulation_parser,
                                                                                      matching_parser,
                                                                                      format_parser,
                                                                                      refresh_parser])
report_parser.add_argument('report_name_or_file', help='The name of the report to run or a path to a'
                                                       ' CSV or JSON file.')
report_parser.add_argument('--count', action='store_true', help='Displays a count of records instead of'
                                                                ' the records themselves.')
report_parser.add_argument('--describe', action='store_true',
                           help='Show the report headers, description, and logic.')
