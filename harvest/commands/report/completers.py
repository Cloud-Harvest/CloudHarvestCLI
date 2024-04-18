from typing import List
from commands.arguments.completers import RemoteBaseCompleter


class ReportNameCompleter(RemoteBaseCompleter):
    def _run(self, *args, **kwargs) -> List[str]:
        try:
            return [r['Name'] for r in self.result.get('data', [])]

        except Exception as ex:
            return []
