from typing import List


class Completer(list):
    """
    A Completer is used in argument parsing to provide tab completion for users. This class is used for local data. If
    the output of a completer is generated from a remote source (such as the api), use the RemoteCompleter.
    """
    def __init__(self):
        super().__init__()

    def run(self, *args, force: bool = False) -> List[str]:
        if force or not self:
            self.clear()
            self.extend(self._run(*args))

        return [s for s in self if str(s).startswith(args[1])]

    def _run(self, *args) -> list:
        """
        Override this function with your own logic.
        :return:
        """
        return []


class RemoteCompleter(Completer):
    def __init__(self, url_path: str):
        self._url_path = url_path
        self._last_checked = None

        super().__init__()
        pass

    def run(self, *args, force: bool = False) -> List[str]:
        from datetime import datetime, timedelta
        if self._last_checked:
            if force or (timedelta(self._last_checked - datetime.now()).total_seconds() > 300):
                query_api = True

            else:
                query_api = False
        else:
            query_api = True

        if query_api:
            result = self._run(*args)
            self.clear()
            self.extend(result)

        return [s for s in self if str(s).startswith(args[1])]

    async def _query_api(self):
        result = []

        from harvest.api import ApiRequest
        with ApiRequest(command=self._url_path) as api:
            await api

        return result


class BannerCompleter(Completer):
    def _run(self, *args) -> List[str]:
        from startup import HarvestConfiguration
        return list(HarvestConfiguration.banners.keys())


class ReportNameCompleter(RemoteCompleter):
    def _run(self, *args) -> List[str]:
        result = []

        api_result = self._query_api()

        return result
