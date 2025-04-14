from cmd2 import Cmd2ArgumentParser
from rich_argparse import RawTextRichHelpFormatter
from CloudHarvestCLI.commands.arguments.parts import *
from CloudHarvestCLI.commands.report.completers import *


report_name_completer = ReportNameCompleter(path='/tasks/list_available_templates')
report_parser = Cmd2ArgumentParser(formatter_class=RawTextRichHelpFormatter,
                                   parents=[
                                       key_manipulation_parser,
                                       matching_parser,
                                       format_parser,
                                       refresh_parser,
                                       variables_parser
                                   ],
                                   description='Run a report on the Harvest cache.')

report_parser.add_argument('report_name', default='list', completer=report_name_completer.run,
                           nargs='?', help='The name of the report to run. Double-tap TAB to see a list of available reports.')
report_parser.add_argument('--count', action='store_true', help='Displays a count of records instead of'
                                                                ' the records themselves.')
report_parser.add_argument('--describe', action='store_true',
                           help='Show the report headers, description, and logic.')
report_parser.add_argument('--limit', type=int, help='Maximum number of records to return.')
report_parser.add_argument('--performance', action='store_true',
                           help='Returns performance statistics for the report.')
report_parser.add_argument('--sort', nargs='*', type=str,
                           help='\n'.join(['Override the sort order for the report.',
                                           'Each entry can be a key or a key with a direction (default \'asc\').',
                                           'Example: `--sort key1 key2:asc key3:desc`',
                                           'When not provided, the report will use the default sort order based on'
                                           ' the visible fields.']))
report_parser.add_argument('--timeout', type=int, default=15,
                           help='\n'.join(['The maximum number of seconds to wait for the report to complete. If the timeout is',
                                ' exceeded, the user will be returned to the prompt. The report itself may still',
                                ' complete on the remote agent. Check the `harvest.jobs` report for a list of jobs.']))
