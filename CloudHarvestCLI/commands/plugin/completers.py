from typing import List
from CloudHarvestCLI.commands.arguments.completers import BaseCompleter


class PluginCompleter(BaseCompleter):
    def _run(self, *args, **kwargs) -> List[str]:
        from CloudHarvestCLI.configuration import HarvestConfiguration
        return list(HarvestConfiguration.plugins.keys())
