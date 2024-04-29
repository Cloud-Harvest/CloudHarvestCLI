from cmd2 import Cmd2ArgumentParser
from rich_argparse import RawTextRichHelpFormatter
from commands.arguments.parts import *
from .completers import *


report_name_completer = ReportNameCompleter(path='/reports/list')
report_parser = Cmd2ArgumentParser(formatter_class=RawTextRichHelpFormatter,
                                   parents=[
                                       key_manipulation_parser,
                                       matching_parser,
                                       format_parser,
                                       refresh_parser
                                   ],
                                   description='Run a report on the Harvest cache.')

report_parser.add_argument('report_name', default='list', completer=report_name_completer.run,
                           nargs='?', help='The name of the report to run. Use `list` to see available reports.')
report_parser.add_argument('--count', action='store_true', help='Displays a count of records instead of'
                                                                ' the records themselves.')
report_parser.add_argument('--describe', action='store_true',
                           help='Show the report headers, description, and logic.')
report_parser.add_argument('--limit', type=int, help='Maximum number of records to return.')
report_parser.add_argument('--sort', nargs='*', type=str,
                           help='\n'.join(['Override the sort order for the report.',
                                           'Each entry can be a key or a key with a direction (default \'asc\').',
                                           'Example: `--sort key1 key2:asc key3:desc`',
                                           'When not provided, the report will use the default sort order based on'
                                           ' the visible fields.']))
