from CloudHarvestCLI.commands.jobs.completers import JobIdCompleter

from cmd2 import Cmd2ArgumentParser
from rich_argparse import RawTextRichHelpFormatter

job_id_completer = JobIdCompleter(path='tasks/list_tasks', refresh_delay=1)


terminate_parser = Cmd2ArgumentParser(
    formatter_class=RawTextRichHelpFormatter,
    description='Terminates one or more jobs.',
    add_help=False
)

terminate_parser.add_argument(
    'job_id',
    nargs='*',
    completer=job_id_completer.run,
    help='The identifier of the job(s) to terminate. If multiple jobs or a parent job is specified, all child jobs '
         'will also be terminated.'
)
