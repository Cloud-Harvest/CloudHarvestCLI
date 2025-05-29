from typing import Any, Literal
from logging import getLogger

from requests import JSONDecodeError

from CloudHarvestCLI.messages import add_message

logger = getLogger('harvest')
HTTP_REQUEST_TYPES = Literal['get', 'post', 'put', 'delete']


class Api:
    """
    Represents an Api object that can be used to make requests to the CloudHarvest API.
    """

    host = None
    port = None
    token = None
    pem = None
    verify = None

    @staticmethod
    def config(host: str, port: int, token: str = None, pem: str = None, verify: (bool, str) = False):
        """
        Configures the Api object.

        Arguments
        host: (str) The host of the API.
        port: (int) The port of the API.
        token: (str, optional) The token to authenticate with the API.
        pem: (str, optional) The certificate to use for SSL.
        verify: (bool, str, optional) Whether to verify the SSL certificate.
        """
        Api.host = host
        Api.port = port
        Api.token = token
        Api.pem = pem
        Api.verify = verify

    @staticmethod
    def safe_decode(response) -> Any:
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


def request(request_type: HTTP_REQUEST_TYPES, endpoint: str, data: dict = None, retries: int = 10, **requests_kwargs) -> Any:
    """
    Makes an API request to the CloudHarvest API.

    Arguments
    host: (str) The host of the API.
    port: (int) The port of the API.
    token: (str) The token to authenticate with the API.
    request_type: (str) The type of request to make (GET, POST, PUT, DELETE).
    endpoint: (str) The endpoint to make the request to.
    data: (dict) The data to send with the request.
    retries: (int) The number of times to retry the request if it fails.

    Returns
    (Any) The response from the API.
    """

    from uuid import uuid4
    request_id = str(uuid4())

    for attempt in range(retries + 1):
        try:
            # Disable SSL warnings which are raised when using self-signed certificates
            import urllib3
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

            from requests.api import request
            logger.debug(f'request:{request_id}: [{request_type}] {Api.host}:{Api.port}/{endpoint}')

            response = request(method=request_type,
                               url=f'https://{Api.host}:{Api.port}/{endpoint}',
                               cert=Api.pem,
                               headers={
                                   'Authorization': f'Bearer {Api.token}'
                               },
                               json=data or {},
                               verify=Api.verify,
                               **requests_kwargs)

        except KeyboardInterrupt:
            return {}

        except ConnectionResetError as cre:
            if attempt < retries:
                from time import sleep

                logger.debug(f'request:{request_id}: Retrying ({attempt + 1}/{retries})...')
                sleep(2 ** attempt)  # Exponential backoff
                continue

            else:
                add_message(None, 'ERROR', True, f'Connection reset error after {retries} retries: {cre}')
                break

        except Exception as e:
            add_message(None,'ERROR', True, f'An unexpected error occurred: {e}')
            logger.debug(f'request:{request_id}:An unexpected error occurred: {e}')

            raise Exception from e

        else:
            if response.status_code != 200:
                add_message(None,'WARN', True, f'An unexpected error occurred: {response.text}')
                logger.debug(f'request:{request_id}:An unexpected error occurred: {response}')

            else:
                return Api.safe_decode(response)

    return None
