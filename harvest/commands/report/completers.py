from typing import List
from commands.arguments.completers import RemoteBaseCompleter


class ReportNameCompleter(RemoteBaseCompleter):
    def _run(self, *args, **kwargs) -> List[str]:
        if isinstance(self.result, list):
            return [report['name'] for report in self.result]

        else:
            return []
