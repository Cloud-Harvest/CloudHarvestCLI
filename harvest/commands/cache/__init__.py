from cmd2 import CommandSet, with_default_category, with_argparser, as_subcommand_to
from typing import List

import messages
from .arguments import parser, map_parser, upload_parser
from processes import ThreadPool

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
        argv = args.cmd2_statement._Cmd2AttributeWrapper__attribute.argv

        if len(argv) > 0:
            command = argv[1]

        else:
            command = ''

        if hasattr(self, command):
            getattr(self, command)(args)

        else:
            parser.print_help()

    @as_subcommand_to('cache', 'collect', map_parser, help='Start metadata collection jobs.')
    def collect(self, args):
        pass

    @as_subcommand_to('cache', 'map', map_parser, help='Display a JSON map of a resource type.')
    def map(self, args):
        pass

    @as_subcommand_to('cache', 'upload', upload_parser, help='Upload documents to the backend.')
    def upload(self, args):
        from glob import glob

        def read_file(p: str) -> List[dict]:
            from json import load
            with open(p, 'r') as stream:
                try:
                    return load(stream)

                except Exception as ex:
                    messages.add_message(self, 'WARN', 'Could not load json file', p, *ex.args)

        from api import HarvestRequest
        from processes import ThreadPool
        from os.path import abspath, isfile

        files = [
            abspath(file)
            for path in args.paths
            for file in glob(path)
            if isfile(file) and file.endswith('.json')
        ]

        from text.printing import print_message
        print_message(f'Preparing to upload {str(len(files))} files.', color='INFO')

        # cache upload ~/git/cloud-harvest/api-plugin-aws/tests/data/cache/rds.*random.json

        pool = ThreadPool(name='Upload', description='Upload files to cache', max_workers=args.max_workers)
        for file in files:
            j = read_file(file)
            if isinstance(j, (dict or list)):
                with HarvestRequest(path='/cache/upload', method='POST', json=j) as hr:
                    pool.add(parent=hr,
                             function=hr.query)

        pool.attach_progressbar()

        return
