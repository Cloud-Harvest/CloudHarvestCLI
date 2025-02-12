from typing import Any, Literal
from logging import getLogger

from requests import JSONDecodeError

from messages import add_message

logger = getLogger('harvest')


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


def request(request_type: Literal['get', 'post', 'put', 'delete'], endpoint: str, data: dict = None, **requests_kwargs) -> Any:
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
    (Any) The response from the API.
    """

    from uuid import uuid4
    request_id = str(uuid4())

    response = None

    try:
        # Disable SSL warnings which are raised when using self-signed certificates
        import urllib3
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        from requests.api import request
        logger.debug(f'request:{request_id}: {Api.host}:{Api.port}/{endpoint}')

        response = request(method=request_type,
                           url=f'https://{Api.host}:{Api.port}/{endpoint}',
                           cert=Api.pem,
                           headers={
                               'Authorization': f'Bearer {Api.token}'
                           },
                           json=data,
                           verify=Api.verify,
                           **requests_kwargs)

    except Exception as e:
        add_message(None,'ERROR', True, f'An unexpected error occurred: {e}')
        logger.debug(f'request:{request_id}:An unexpected error occurred: {e}')

    else:
        if response.status_code != 200:
            add_message(None,'ERROR', True, f'An unexpected error occurred: {response.text}')
            logger.debug(f'request:{request_id}:An unexpected error occurred: {response}')

        else:
            return Api.safe_decode(response)
