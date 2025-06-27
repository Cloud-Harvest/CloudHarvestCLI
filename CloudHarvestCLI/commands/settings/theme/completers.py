from typing import List
from CloudHarvestCLI.commands.arguments.completers import BaseCompleter


class ThemeCompleter(BaseCompleter):
    def _run(self, *args, **kwargs) -> List[str]:
        from CloudHarvestCLI.configuration import HarvestConfiguration
        return list(HarvestConfiguration.themes.keys()) or []
