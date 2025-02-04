from typing import List
from commands.arguments.completers import RemoteBaseCompleter


class PlatformRemoteCompleter(RemoteBaseCompleter):
    def _run(self, *args, **kwargs) -> List[str]:
        try:
            result = list(set([collection.split('.')[0] for collection in self.result]))
            result.sort()

            return result

        except Exception:
            return []


class ServiceRemoteCompleter(RemoteBaseCompleter):
    def _run(self, *args, **kwargs) -> List[str]:
        try:
            platform = args[2].strip().split(' ')[2]

            result = list(set([
                collection.split('.')[1]
                for collection in self.result
                if collection.split('.')[0] == platform
            ]))
            result.sort()

            return result

        except Exception:
            return []


class TypeRemoteCompleter(RemoteBaseCompleter):
    def _run(self, *args, **kwargs) -> List[str]:
        platform, service = args[2].strip().split(' ')[2:4]

        try:
            result = list(set([
                collection.split('.')[2]
                for collection in self.result
                if collection.split('.')[0] == platform
                and collection.split('.')[1] == service
            ]))
            result.sort()

            return result

        except Exception:
            return []
