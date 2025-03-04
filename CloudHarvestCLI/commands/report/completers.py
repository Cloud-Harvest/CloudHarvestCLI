from logging import getLogger
from typing import List
from CloudHarvestCLI.commands.arguments.completers import RemoteBaseCompleter

logger = getLogger('harvest')

class ReportNameCompleter(RemoteBaseCompleter):
    def _run(self, *args, **kwargs) -> List[str]:
        try:
            return [r['Name'] for r in self.result['result']['data']]

        except Exception as ex:
            logger.debug(ex)

            return []
