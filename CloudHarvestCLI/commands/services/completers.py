from typing import List
from CloudHarvestCLI.commands.arguments.completers import BaseCompleter

class ServicesCompleter(BaseCompleter):
    def _run(self, *args, **kwargs) -> List[str]:
        from CloudHarvestCLI.processes import ConcurrentProcesses
        keys, report = ConcurrentProcesses.report()
        return [o.get('Name') for o in report]
