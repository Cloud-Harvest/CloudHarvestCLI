from cmd2 import Cmd2ArgumentParser
from rich_argparse import RawTextRichHelpFormatter
from commands.arguments.parts import *
from .completers import *


report_name_completer = ReportNameCompleter(path='/reports/list')
report_parser = Cmd2ArgumentParser(formatter_class=RawTextRichHelpFormatter, parents=[key_manipulation_parser,
                                                                                      matching_parser,
                                                                                      format_parser,
                                                                                      refresh_parser])
report_parser.add_argument('report_name_or_file', default='list', completer=report_name_completer.run,
                           help='The name of the report to run or a path to a CSV or JSON file.')
report_parser.add_argument('--count', action='store_true', help='Displays a count of records instead of'
                                                                ' the records themselves.')
report_parser.add_argument('--describe', action='store_true',
                           help='Show the report headers, description, and logic.')
