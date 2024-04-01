from typing import List
from commands.arguments.completers import BaseCompleter

class ServicesCompleter(BaseCompleter):
    def _run(self, *args, **kwargs) -> List[str]:
        from processes import ConcurrentProcesses
        report, keys = ConcurrentProcesses.report()
        return [o.get('Name') for o in report]
