from cmd2 import Cmd2ArgumentParser
from rich_argparse import RawTextRichHelpFormatter

from CloudHarvestCLI.commands.settings.theme.completers import ThemeCompleter


theme_completer = ThemeCompleter()
theme_parser = Cmd2ArgumentParser(formatter_class=RawTextRichHelpFormatter, add_help=False)

subparsers = theme_parser.add_subparsers(dest='theme_subcommand', help='Subcommands for theme management')

# Subparser for the 'list' subcommand
list_parser = subparsers.add_parser('list', help='List the available themes')

# Subparser for the 'set' subcommand
set_parser = subparsers.add_parser('set', help='Set the current theme')
set_parser.add_argument('set_theme', type=str, completer=theme_completer.run, help='Theme to set')
