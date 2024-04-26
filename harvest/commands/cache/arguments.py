from cmd2 import Cmd2ArgumentParser
from cmd2 import Cmd

from commands.arguments.parts import format_parser, pstar_parser_optional, thread_parser, yes_parser
from rich_argparse import RawTextRichHelpFormatter

# completers
from .completers import AvailablePstarRemoteCompleter
platform_remote_completer = AvailablePstarRemoteCompleter(path='/cache/get/pstar_dimensions',
                                                          remote_api_kwargs={'dimension': 'platform'})
service_remote_completer = AvailablePstarRemoteCompleter(path='/cache/get/pstar_dimensions',
                                                         remote_api_kwargs={'dimension': 'service'})
type_remote_completer = AvailablePstarRemoteCompleter(path='/cache/get/pstar_dimensions',
                                                      remote_api_kwargs={'dimension': 'type'})

# base parser
parser = Cmd2ArgumentParser(formatter_class=RawTextRichHelpFormatter)
subparser = parser.add_subparsers()

# cache collect
collect_parser = Cmd2ArgumentParser(formatter_class=RawTextRichHelpFormatter,
                                    parents=[pstar_parser_optional])

# cache map
map_parser = Cmd2ArgumentParser(formatter_class=RawTextRichHelpFormatter)

map_parser.add_argument('platform', type=str, completer=platform_remote_completer.run,
                        help='Set the platform for the data.'
                             ' Example: `aws`')
map_parser.add_argument('service', type=str, completer=service_remote_completer.run,
                        help='Set the service name for the data.'
                             ' Example: `rds`')
map_parser.add_argument('type', type=str, completer=type_remote_completer.run,
                        help='Set the service subtype for the data.'
                             ' Example: instance')
map_parser.add_argument('--account', type=str,
                        help='Set the platform account name for the data.'
                             ' Example: aws-business-development')
map_parser.add_argument('--region', type=str,
                        help='The account geographical region.'
                             ' Example: us-east-1')
map_parser.add_argument('--flatten', type=str, default=None,
                        help='Flatten the data using the specified separator.'
                             ' Example: `.`')


# cache upload command
upload_parser = Cmd2ArgumentParser(formatter_class=RawTextRichHelpFormatter,
                                   parents=[thread_parser, yes_parser])
upload_parser.add_argument('paths', nargs='*', completer=Cmd.path_complete,
                           help='Path containing the file(s) to upload.')
