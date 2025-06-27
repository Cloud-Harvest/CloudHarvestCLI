from CloudHarvestCLI.commands.settings.banner.arguments import banner_parser
from CloudHarvestCLI.commands.settings.plugin.arguments import plugin_parser
from CloudHarvestCLI.commands.settings.theme.arguments import theme_parser

from cmd2 import Cmd2ArgumentParser
from rich_argparse import RawTextRichHelpFormatter


settings_parser = Cmd2ArgumentParser(formatter_class=RawTextRichHelpFormatter, add_help=False)
subparsers = settings_parser.add_subparsers(dest='subcommand')

subparsers.add_parser('banner', parents=[banner_parser], help='View banners and their rules.')
subparsers.add_parser('plugin', parents=[plugin_parser], help='Manage plugins.')
subparsers.add_parser('theme', parents=[theme_parser], help='Manage text color themes.')
