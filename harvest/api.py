from configuration import HarvestConfiguration
from argparse import Namespace
from urllib.request import getproxies
from requests import Request, Session
from logging import getLogger
logger = getLogger('harvest')


class HarvestRequest(Request):
    def __init__(self, host: str = None, path: str = None, method: str = 'GET', json: str = None, args: Namespace = None, **kwargs):
        from urllib.parse import urljoin
        url = urljoin(host or HarvestConfiguration.api.get('host'), path)
        params = vars(args) if args else {} | kwargs

        super().__init__(url=url, method=method.upper(), params=params, json=json)

    def query(self) -> dict or tuple:
        prepared_statement = self.prepare()

        session = Session()

        # include proxy configuration (if any)
        session.proxies = getproxies()

        # TODO: authentication methods (like getting a token)
        # session.auth = get_auth('')

        try:
            response = session.send(prepared_statement)

        # TODO: handle urllib3 connection errors
        except ConnectionError as ce:
            from exceptions import BaseHarvestException
            BaseHarvestException(*ce.args, log_level='error')
            return 400, 'Could not make connection to api.'

        logger.debug(f'{prepared_statement}[{response.status_code}')

        if 200 <= response.status_code <= 299:
            return response.json()

        else:
            from messages import add_message
            add_message(__name__, 'WARN', response.status_code, response.reason)

            return response.status_code, response.reason



def get_auth(method: str) -> tuple:
    result = ()

    return result
