from cmd2 import Cmd2ArgumentParser
from rich_argparse import RawTextRichHelpFormatter

plugin_parser = Cmd2ArgumentParser(formatter_class=RawTextRichHelpFormatter, add_help=False)

subparsers = plugin_parser.add_subparsers(dest='plugins_subcommand', help='Subcommands for theme management')

# Subparser for the 'add' subcommand
add_parser = subparsers.add_parser('add', help='Add a plugin')
add_parser.add_argument('url_or_package_name', type=str, help='The URL or package name of the plugin to add')
add_parser.add_argument('branch', type=str, help='The branch name or version number to add')

install_parser = subparsers.add_parser('install', help='Install the plugins in the plugins.txt file')
install_parser.add_argument('--quiet', action='store_true', help='Suppress output from the installation process')

# Subparser for the 'list' subcommand
list_parser = subparsers.add_parser('list', help='List configured plugins.')

# Subparser for the 'remove' subcommand
remove_parser = subparsers.add_parser('remove', help='Remove a plugin')
