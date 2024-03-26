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

        pool = ThreadPool(name='Upload', description='Upload files to cache', max_workers=args.max_workers)
        [
            pool.add(parent=self,
                     function=HarvestRequest(path='/cache/upload',
                                             method='POST',
                                             json=[
                                                 line.update(generate_metadata(platform=args.platform,
                                                                               service=args.service,
                                                                               type=args.type,
                                                                               account=args.account,
                                                                               region=args.region))
                                                 for line in read_file(file)
                                             ]).query())
            for file in files
        ]

        pool.attach_progressbar()

        return


def generate_metadata(platform: str, service: str, type: str, account: str, region: str) -> dict:
    def random_bool():
        from random import choice
        return choice([True, False])

    def random_date():
        from datetime import datetime
        from random import randint
        now_timestamp = int(datetime.now().timestamp())
        six_months_ago = int(now_timestamp - (60 * 60 * 24 * 30 * 6))
        return datetime.fromtimestamp(randint(six_months_ago, now_timestamp))

    from configuration import HarvestConfiguration

    result = {
        'Platform': platform,
        'Service': service,
        'Type': type,
        'Account': account,
        'Region': region,
        'Module': {
            'FilterCriteria': [''],
            'Name': 'harvest-client-cli',
            'Repository': 'https://github.com/Cloud-Harvest/client-cli',
            'Version': HarvestConfiguration.version
        },
        'Dates': {
            'DeactivatedOn': '',
            'LastSeen': random_date()
        },
        'Active': random_bool()
    }

    return result
