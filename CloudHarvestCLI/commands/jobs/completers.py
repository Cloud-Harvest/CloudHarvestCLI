from typing import List
from CloudHarvestCLI.commands.arguments.completers import RemoteBaseCompleter


class JobIdCompleter(RemoteBaseCompleter):
    def _run(self, *args, **kwargs) -> List[str]:

        result = self.result.get('result')

        if isinstance(result, list):
            return result

        return []
