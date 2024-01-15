from cmd2 import Cmd2ArgumentParser


parser = Cmd2ArgumentParser()

subparsers = parser.add_subparsers()
# banner
banner_subparser = subparsers.add_parser('banner', help='Display startup banners.')
banner_subparser.add_argument('names', type=str, nargs='*',
                              help='The name of the report to display. When not provided, all banners are displayed.')
banner_subparser.add_argument('--text', type=str, default='HARVEST',
                              help='Allows the user to display arbitrary text using the banner code.')

# reporting
report_subparser = subparsers.add_parser('report', help='Run reports.')
report_subparser.add_argument('report_name_or_file', help='The name of the report to run or a path to a CSV or JSON file.')
report_subparser.add_argument('-m', '--match', action='append', nargs='+', default=[],
                              help='Provide matching statements. Matches are defined in the following ways:\n'
                                   'One match statement: `-m Field=Value`\n'
                                   'A single `-m` are AND statements `-m Field=Value Field=Value`'
                                   'Each `-m` is an OR statement: `-m Field=Value` `-m Field=Value`')

parser.parse_args()
