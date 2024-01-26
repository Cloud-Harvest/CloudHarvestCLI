from cmd2 import CommandSet, with_default_category, with_argparser
from commands.banner.arguments import banner_parser


@with_default_category('Harvest')
class BannerCommand(CommandSet):
    @with_argparser(banner_parser)
    def do_banner(self, args):
        from configuration import HarvestConfiguration
        _banners = HarvestConfiguration.banners

        from banner import get_banner

        if args.names:
            names = args.names

        else:

            names = _banners

        results = {
            name: get_banner(banner_configuration=_banners,
                             name=name,
                             text=args.text)
            for name in names
        }

        for name, banner in results.items():
            from text import console
            console.print(f'\n {name}----------')
            console.print(banner)
