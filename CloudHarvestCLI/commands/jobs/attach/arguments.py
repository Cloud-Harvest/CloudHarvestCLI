from CloudHarvestCLI.commands.jobs.completers import JobIdCompleter

from cmd2 import Cmd2ArgumentParser
from rich_argparse import RawTextRichHelpFormatter

job_id_completer = JobIdCompleter(path='tasks/list_tasks', refresh_delay=1)


attach_parser = Cmd2ArgumentParser(formatter_class=RawTextRichHelpFormatter, description='Attach a progress bar to a job.', add_help=False)
attach_parser.add_argument('job_id', type=str, completer=job_id_completer.run,
                           help='The name of the job to attach a progress bar to.')
attach_parser.add_argument('--timeout', type=int, default=60, help='The timeout for the job in seconds. Default is 60 seconds.')
