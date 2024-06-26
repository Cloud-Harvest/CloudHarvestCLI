from cmd2 import with_default_category, CommandSet, with_argparser, as_subcommand_to
from .arguments import parser, map_parser, upload_parser


@with_default_category('Harvest')
class CacheCommand(CommandSet):

    @with_argparser(parser)
    def do_cache(self, args):
        from commands.base import get_subtask
        get_subtask(parent=self, parser=parser, args=args)

    @as_subcommand_to('cache', 'attach', map_parser, help='Attaches a progress bar to a data collection job.')
    def attach(self, args):
        pass

    @as_subcommand_to('cache', 'collect', map_parser, help='Start metadata collection jobs.')
    def collect(self, args):
        pass

    @as_subcommand_to('cache', 'map', map_parser, help='Display a JSON map of a resource type.')
    def map(self, args):
        from api import HarvestRequest
        with HarvestRequest(path='/cache/map', json=args) as request:
            result = request.query()

        if isinstance(result, dict):
            from text.printing import print_data
            data = result.get('result')
            meta = result.get('meta')

            print_data(data=data,
                       flatten=args.flatten,
                       output_format='pretty-json')

            if meta:
                from text.printing import print_message
                print_message(f"\nReturned {meta.get('collection')} in {meta.get('duration')} seconds.",
                              color='INFO',
                              as_feedback=True)

    @as_subcommand_to('cache', 'upload', upload_parser, help='Upload documents to the database.')
    def upload(self, args):
        from app import upload_files
        upload_files(parent=self, paths=args.paths, api_path='/cache/upload', max_workers=args.max_workers, yes=args.yes)
