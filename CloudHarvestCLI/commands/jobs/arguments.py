from CloudHarvestCLI.commands.jobs.attach.arguments import attach_parser
from CloudHarvestCLI.commands.jobs.terminate.arguments import terminate_parser

from cmd2 import Cmd2ArgumentParser
from rich_argparse import RawTextRichHelpFormatter


jobs_parser = Cmd2ArgumentParser(formatter_class=RawTextRichHelpFormatter, add_help=False)
subparsers = jobs_parser.add_subparsers(title='subcommands', dest='subcommand')

subparsers.add_parser('attach', parents=[attach_parser], help='Attach a progress bar to a job.')
subparsers.add_parser('terminate', parents=[terminate_parser], help='Terminates one or more jobs.')
