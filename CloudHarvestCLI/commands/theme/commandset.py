from cmd2 import with_default_category, CommandSet, with_argparser
from CloudHarvestCLI.commands.theme.arguments import theme_parser

@with_default_category('Harvest')
class ThemeCommand(CommandSet):
    @with_argparser(theme_parser)
    def do_theme(self, args):
        from CloudHarvestCLI.configuration import HarvestConfiguration
        from CloudHarvestCLI.messages import print_message
        from CloudHarvestCLI.text.printing import feedback_console

        themes = HarvestConfiguration.themes

        print_message(f'The current theme is `{str(HarvestConfiguration.theme)}`.', 'INFO', True, )

        if args.subcommand == 'list':
            from rich.table import Table, Row
            from rich.box import SIMPLE
            from rich.text import Text

            table = Table(title='Available Themes', box=SIMPLE)
            table.add_column('Name', overflow='fold')

            [table.add_column(col) for col in list(themes['default'].keys())]

            [
                table.add_row(
                    *[Text(theme_name)] + [Text('SAMPLE', style=color) for output_type, color in color_pallet.items()])
                for theme_name, color_pallet in themes.items()
            ]

            feedback_console.print(table)

        elif args.subcommand == 'set':
            old_theme = HarvestConfiguration.theme or 'default'
            new_theme = args.set_theme

            if new_theme != old_theme:
                HarvestConfiguration.theme = new_theme

                # set the colors
                from CloudHarvestCLI.text.styling import TextColors
                TextColors.set_colors(**HarvestConfiguration.themes.get(HarvestConfiguration.theme))

                HarvestConfiguration.update_config(key='theme', value=new_theme)

                from CloudHarvestCLI.app import HARVEST_CLI, get_prompt
                HARVEST_CLI.prompt = get_prompt()

                print_message(f'Set the theme to `{new_theme}`.', 'INFO', True, )

            else:
                print_message( f'Kept the `{new_theme}` theme.', 'INFO', True, )

        else:

            print_message('Invalid subcommand.', 'ERROR', True, )
            theme_parser.print_help()
