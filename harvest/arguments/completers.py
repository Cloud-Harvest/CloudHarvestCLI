from typing import Dict, List


class Completer:
    """
    A Completer is used in argument parsing to provide tab completion for users. This class is used for local data. If
    the output of a completer is generated from a remote source (such as the api), use the RemoteCompleter.
    """
    def __init__(self):
        self.result = None

        super().__init__()

    def run(self, *args, force: bool = False, **kwargs) -> list:
        if force or not self:
            self.result = self._run(*args, **kwargs)

        return self._select_return_value(*args)

    def _run(self, *args, **kwargs) -> list:
        """
        Override this function with your own logic.
        :return:
        """
        return []

    def _select_return_value(self, *args):
        if isinstance(self.result, dict):
            result = list(self.result.keys())

        else:
            result = self.result

        return [s for s in result if str(s).startswith(args[1])]


class RemoteCompleter(Completer):
    def __init__(self, path: str):
        self._path = path
        self._last_checked = None

        super().__init__()
        pass

    def run(self, *args, force: bool = False, **kwargs):
        from datetime import datetime
        if self._last_checked:
            if force or ((self._last_checked - datetime.now()).total_seconds() > 300) or isinstance(self.result, tuple):
                query_api = True

            else:
                query_api = False
        else:
            query_api = True

        if query_api:
            from harvest.api import HarvestRequest
            self._last_checked = datetime.now()
            self.result = HarvestRequest(path=self._path).query()
            self.result = self._run(*args, **kwargs)

        return self._select_return_value(*args)


class BannerCompleter(Completer):
    def _run(self, *args, **kwargs) -> List[str]:
        from configuration import HarvestConfiguration
        return list(HarvestConfiguration.banners.keys())


class ReportNameCompleter(RemoteCompleter):
    def _run(self, *args, **kwargs) -> List[str]:
        if isinstance(self.result, list):
            return [report['name'] for report in self.result]

        else:
            return []
