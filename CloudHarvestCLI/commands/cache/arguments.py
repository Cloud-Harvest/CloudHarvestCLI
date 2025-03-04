from cmd2 import Cmd2ArgumentParser
from cmd2 import Cmd

from CloudHarvestCLI.commands.arguments.parts import pstar_parser_optional, thread_parser, yes_parser
from rich_argparse import RawTextRichHelpFormatter

# completers
from CloudHarvestCLI.commands.cache.completers import PlatformRemoteCompleter, ServiceRemoteCompleter, TypeRemoteCompleter
platform_remote_completer = PlatformRemoteCompleter(path='/cache/get/data_collections')
service_remote_completer = ServiceRemoteCompleter(path='/cache/get/data_collections')
type_remote_completer = TypeRemoteCompleter(path='/cache/get/data_collections')

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
