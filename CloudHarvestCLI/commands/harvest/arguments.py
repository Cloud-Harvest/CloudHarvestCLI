from cmd2 import Cmd2ArgumentParser
from rich_argparse import RawTextRichHelpFormatter
from CloudHarvestCLI.commands.arguments.parts import *
from CloudHarvestCLI.commands.harvest.completers import *


harvest_name_completer = HarvestNameCompleter(path='/tasks/list_available_templates')
harvest_parser = Cmd2ArgumentParser(formatter_class=RawTextRichHelpFormatter,
                                    parents=[
                                        pstar_parser_optional
                                    ],
                                    description='Collect data based on providers, services, types, accounts, and regions.')

harvest_parser.add_argument('--list', action='store_true',
                            help='List all available harvests.')

