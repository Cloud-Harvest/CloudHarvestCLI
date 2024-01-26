from configuration import HarvestConfiguration
from urllib.request import getproxies
from requests import Request, Session
from logging import getLogger
logger = getLogger('harvest')


class HarvestRequest(Request):
    def __init__(self, host: str = None, path: str = None, method: str = 'GET', **kwargs):
        from urllib.parse import urljoin
        url = urljoin(host or HarvestConfiguration.api.get('host'), path)

        super().__init__(url=url, method=method.upper(), **kwargs)

    def query(self) -> dict or tuple:
        prepared_statement = self.prepare()

        session = Session()

        # include proxy configuration (if any)
        session.proxies = getproxies()

        # TODO: authentication methods (like getting a token)
        # session.auth = get_auth('')

        response = session.send(prepared_statement)

        if 200 <= response.status_code <= 299:
            return response.json()

        else:
            from messages import Messages, TextColors
            Messages.add(response.status_code, response.reason, style=TextColors.WARN)

            return response.status_code, response.reason


def get_auth(method: str) -> tuple:
    result = ()

    return result
