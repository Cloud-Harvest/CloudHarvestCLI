from typing import List
from commands.arguments.completers import RemoteBaseCompleter


class AvailablePstarRemoteCompleter(RemoteBaseCompleter):
    def _run(self, *args, **kwargs) -> List[str]:
        try:
            return self.result.get('result')

        except Exception as ex:
            return []

