from typing import List
from commands.arguments.completers import BaseCompleter


class BannerCompleter(BaseCompleter):
    def _run(self, *args, **kwargs) -> List[str]:
        from configuration import HarvestConfiguration
        return list(HarvestConfiguration.banners.keys())
