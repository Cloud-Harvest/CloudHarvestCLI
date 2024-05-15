from configuration import HarvestConfiguration
from argparse import Namespace
from typing import Any
from urllib.request import getproxies
from requests import Request, Session
from logging import getLogger
from processes import ProcessStatusCodes

logger = getLogger('harvest')


class HarvestRequest(Request):
    def __init__(self, host: str = None, path: str = None, method: str = 'GET', json: Any = None):
        from urllib.parse import urljoin
        url = ''.join([HarvestConfiguration.api.get('protocol'),
                       '://',
                       host or HarvestConfiguration.api.get('host'),
                       ':',
                       str(HarvestConfiguration.api.get('port') or 8000),
                       '/',
                       path or ''])

        if isinstance(json, str):
            str_json = json

        elif isinstance(json, Namespace):
            from json import dumps
            str_json = dumps({
                k: v for k, v in vars(json).items()
                if not k.startswith('cmd2')
            }, default=str)

        else:
            from json import dumps
            str_json = dumps(json, default=str)

        super().__init__(url=url,
                         method=method.upper(),
                         json=str_json)

        self.status = ProcessStatusCodes.INITIALIZED

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return None

    def query(self) -> dict or tuple:
        self.status = ProcessStatusCodes.RUNNING

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
            self.status = ProcessStatusCodes.ERROR

            from exceptions import BaseHarvestException
            BaseHarvestException(*ce.args, log_level='error')
            return 400, 'Could not make connection to api.'

        else:
            logger.debug(f'{prepared_statement}[{response.status_code}')

            if 200 <= response.status_code <= 299:
                return response.json()

            else:
                from messages import add_message
                add_message(__name__, 'WARN', response.status_code, response.reason)

                return response.status_code, response.reason

        finally:
            self.status = ProcessStatusCodes.COMPLETE


def get_auth(method: str) -> tuple:
    result = ()

    return result
