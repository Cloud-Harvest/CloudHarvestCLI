class BaseCompleter:
    """
    A Completer is used in argument parsing to provide tab completion for users. This class is used for local data. If
    the output of a completer is generated from a remote source (such as the api), use the RemoteCompleter.
    """
    def __init__(self):
        self.result = None

        super().__init__()

    def run(self, *args, refresh: bool = False, **kwargs) -> list:
        if refresh or not self.result:
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

        if result:
            return [s for s in result if str(s).startswith(args[1])]

        else:
            return []


class RemoteBaseCompleter(BaseCompleter):
    """
    A RemoteBaseCompleter retrieves information from the API. The data is stored in memory where it is reused.
    """
    def __init__(self, path: str, refresh_delay: int = 300, remote_api_kwargs: dict = None):
        self._path = path
        self._last_checked = None
        self._api_kwargs = remote_api_kwargs or {}
        self.refresh_delay = refresh_delay

        super().__init__()
        pass

    def run(self, *args, refresh: bool = False, **kwargs):
        from datetime import datetime
        if self._last_checked:
            _conditions = any([
                refresh,
                (self._last_checked - datetime.now()).total_seconds() > self.refresh_delay,
                isinstance(self.result, tuple)
            ])

            if _conditions:
                query_api = True

            else:
                query_api = False
        else:
            query_api = True

        if query_api:
            from api import HarvestRequest
            self._last_checked = datetime.now()
            self.result = HarvestRequest(path=self._path, json=self._api_kwargs).query()
            self.result = self._run(*args, **kwargs)

        return self._select_return_value(*args)
