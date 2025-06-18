from logging import getLogger
from typing import List
from CloudHarvestCLI.commands.arguments.completers import RemoteBaseCompleter

logger = getLogger('harvest')

class ReportNameCompleter(RemoteBaseCompleter):
    def _run(self, *args, **kwargs) -> List[str]:
        try:
            results = [
                str(template).replace('template_reports/', '')  # Removes the prefix to return just the template name
                for template in self.result['result']
                if str(template).startswith('template_reports/')            # Must be a report template
                   and not str(template.split('.')[-1]).startswith('_')     # Must not be a hidden template
            ]

            return results

        except Exception as ex:
            logger.debug(ex)

            return []
