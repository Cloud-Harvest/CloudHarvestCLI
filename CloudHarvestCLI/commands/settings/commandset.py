from CloudHarvestCLI.commands.settings.arguments import settings_parser

from cmd2 import with_default_category, CommandSet, with_argparser


@with_default_category('Harvest')
class SettingsCommand(CommandSet):

    @with_argparser(settings_parser)
    def do_settings(self, args):
        match str(args.subcommand):
            case 'banner':
                from CloudHarvestCLI.commands.settings.banner.commandset import do_banner
                do_banner(args)

            case 'plugin':
                from CloudHarvestCLI.commands.settings.plugin.commandset import do_plugin
                do_plugin(args)

            case 'theme':
                from CloudHarvestCLI.commands.settings.theme.commandset import do_theme
                do_theme(args)

            case _:
                from CloudHarvestCLI.messages import print_message
                print_message('ERROR', True, 'Please specify a subcommand for the "settings" command.')
                settings_parser.print_help()
