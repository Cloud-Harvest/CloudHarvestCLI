from cmd2 import CommandSet, with_default_category, with_argparser, as_subcommand_to
from typing import List
from .arguments import parser, map_parser, upload_parser


_pstar = ('Platform',
          'Service',
          'Type',
          'Account',
          'Region')

_required_meta_fields = _pstar + (
    'Module.FilterCriteria.0',  # FilterCriteria requires at least one value, so .0 is expected
    'Module.Name',
    'Module.Repository',
    'Module.Version',
    'Dates.DeactivatedOn',
    'Dates.LastSeen',
    'Active'
)


@with_default_category('Harvest')
class CacheCommand(CommandSet):

    @with_argparser(parser)
    def do_cache(self, args):
        pass

    @as_subcommand_to('cache', 'collect', map_parser)
    def collect(self, **kwargs):
        pass

    @as_subcommand_to('cache', 'map', map_parser)
    def map(self, **kwargs):
        pass

    @as_subcommand_to('cache', 'upload', upload_parser)
    def upload(self, args):
        from glob import glob

        def read_files(p: str):
            from json import load
            with open(p, 'r') as stream:
                yield load(stream)

        files = (f for path in args.paths for f in glob(path))

        from api import HarvestRequest
        HarvestRequest(path='/cache/upload',
                       method='PUT',
                       data=(read_files(file)for file in files))
