# from configuration import HarvestConfiguration
# from argparse import Namespace
# from typing import Any
# from urllib.request import getproxies
# from requests import Request, Session
# from requests.exceptions import ConnectionError
# from logging import getLogger
# from processes import ProcessStatusCodes
#
# logger = getLogger('harvest')
#
#
# class HarvestRequest(Request):
#     def __init__(self, host: str = None, path: str = None, method: str = 'GET', json: Any = None):
#         from urllib.parse import urljoin
#         url = ''.join([HarvestConfiguration.api.get('protocol'),
#                        '://',
#                        host or HarvestConfiguration.api.get('host'),
#                        ':',
#                        str(HarvestConfiguration.api.get('port') or 8000),
#                        '/',
#                        path or ''])
#
#         if isinstance(json, str):
#             str_json = json
#
#         elif isinstance(json, Namespace):
#             from json import dumps
#             str_json = dumps({
#                 k: v for k, v in vars(json).items()
#                 if not k.startswith('cmd2')
#             }, default=str)
#
#         else:
#             from json import dumps
#             str_json = dumps(json, default=str)
#
#         super().__init__(url=url,
#                          method=method.upper(),
#                          json=str_json)
#
#         self.status = ProcessStatusCodes.INITIALIZED
#
#     def __enter__(self):
#         return self
#
#     def __exit__(self, exc_type, exc_val, exc_tb):
#         return None
#
#     def query(self) -> dict or list or tuple:
#         self.status = ProcessStatusCodes.RUNNING
#
#         prepared_statement = self.prepare()
#
#         session = Session()
#
#         # include proxy configuration (if any)
#         session.proxies = getproxies()
#
#         # TODO: authentication methods (like getting a token)
#         # session.auth = get_auth('')
#
#         try:
#             response = session.send(prepared_statement)
#
#         except ConnectionError as e:
#             from messages import add_message
#             connection_error_class = str(type(e.args[0].reason)).replace("<class 'urllib3.exceptions.", '').replace("'>", '')
#             add_message(__name__, 'ERROR', 'Could not connect to the server:', connection_error_class)
#
#             logger.debug(f'{connection_error_class}: {prepared_statement}: \n' + str(e.args))
#
#             return e
#
#         except Exception as e:
#             from messages import add_message
#             add_message(__name__, 'ERROR', 'Could not connect to the server:', e.args[0])
#
#             logger.debug(f'{e.args[0]}: {prepared_statement}: \n' + e.args[1])
#
#             return e
#
#         else:
#             logger.debug(f'{prepared_statement}[{response.status_code}')
#
#             if 200 <= response.status_code <= 299:
#                 return response.json()
#
#             else:
#                 from messages import add_message
#                 add_message(__name__, 'WARN', response.status_code, response.reason)
#
#                 return response.status_code, response.reason
#
#         finally:
#             self.status = ProcessStatusCodes.COMPLETE
#
#
# def get_auth(method: str) -> tuple:
#     result = ()
#
#     return result


from typing import Literal
from logging import getLogger

from requests import JSONDecodeError

logger = getLogger('harvest')


class Api:
    """
    Represents an Api object that can be used to make requests to the CloudHarvest API.
    """

    def __init__(self, host: str, port: int, token: str = None, pem: str = None, verify: (bool, str) = False):
        """
        Initializes the Api object.

        Arguments
        host: (str) The host of the API.
        port: (int) The port of the API.
        token: (str, optional) The token to authenticate with the API.
        pem: (str, optional) The certificate to use for SSL.
        verify: (bool, str, optional) Whether to verify the SSL certificate.
        """
        self.host = host
        self.port = port
        self.token = token
        self.pem = pem
        self.verify = verify

    def request(self, request_type: Literal['get', 'post', 'put', 'delete'], endpoint: str, data: dict = None, **requests_kwargs) -> dict:
        """
        Makes an API request to the CloudHarvest API.

        Arguments
        host: (str) The host of the API.
        port: (int) The port of the API.
        token: (str) The token to authenticate with the API.
        request_type: (str) The type of request to make (GET, POST, PUT, DELETE).
        endpoint: (str) The endpoint to make the request to.
        data: (dict) The data to send with the request.

        Returns
        {
            'id': (str) The request ID.
            'status_code': (int) The status code of the response.
            'response': (dict) The response from the API.
        }
        """

        from uuid import uuid4
        request_id = str(uuid4())

        response = None

        try:
            from requests.api import request
            logger.debug(f'request:{request_id}: {self.host}:{self.port}/{endpoint}')
            response = request(method=request_type,
                               url=f'https://{self.host}:{self.port}/{endpoint}',
                               cert=self.pem,
                               headers={
                                   'Authorization': f'Bearer {self.token}'
                               },
                               json=data,
                               verify=self.verify,
                               **requests_kwargs)

        except Exception as e:
            logger.error(f'request:{request_id}:An unexpected error occurred: {e}')

        finally:
            result = {
                'id': request_id,
                'response': self.safe_decode(response),
                'url': f'https://{self.host}:{self.port}/{endpoint}'
            }

            # Additional fields to include in the response
            response_fields = (
                ('status_code', 500),
                ('reason', 'Internal Server Error')
            )

            for code, default in response_fields:
                result[code] = getattr(response, code, default)

            return result

    @staticmethod
    def safe_decode(response):
        """
        Safely decodes a response from the API.

        Arguments
        response: (dict) The response to decode.

        Returns
        (dict) The decoded response.
        """
        result = None
        try:
            result = response.json()

        except JSONDecodeError as e:
            result = f'Failed to decode response JSON: {e}'

        finally:
            return result
