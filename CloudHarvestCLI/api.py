from CloudHarvestCLI.messages import add_message

from logging import getLogger
from requests import JSONDecodeError, Response
from requests.exceptions import (
    ChunkedEncodingError,
    ConnectionError,
    ConnectTimeout,
    HTTPError,
    ProxyError,
    ReadTimeout,
    SSLError,
    TooManyRedirects
)
from typing import Any, Literal

from messages import print_message

HTTP_REQUEST_TYPES = Literal['get', 'post', 'put', 'delete']
logger = getLogger('harvest')


RETRYABLE_EXCEPTIONS = (
    ChunkedEncodingError,
    ConnectionError,
    ConnectTimeout,
    ReadTimeout,
    SSLError,
    TooManyRedirects
)

RETRYABLE_HTTP_STATUS_CODES = (
    408,  # Request Timeout
    409,  # Conflict
    429,  # Too Many Requests
    500,  # Internal Server Error
    502,  # Bad Gateway
    503,  # Service Unavailable
    504,  # Gateway Timeout
    507  # Insufficient Storage
)

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
    response = None

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
            logger.debug(f'request:{request_id}: User interrupted the request.')
            return {}

        except Exception as ex:
            if _retry_request(ex, response):
                if attempt < retries:
                    from time import sleep

                    logger.debug(f'request:{request_id}: Got {_format_exception(ex)}. Retrying ({attempt + 1}/{retries})...')
                    sleep(1)
                    continue

                else:
                    print_message(f'[{request_id}] Too many retries ({retries}) for request. {_format_exception(ex)}', 'ERROR', True)
                    break

            else:
                print_message(f'[{request_id}] An unexpected error occurred: {_format_exception(ex)}', 'ERROR', True)

                from traceback import format_exc
                logger.debug(f'request:{request_id}:An unexpected error occurred:\n{format_exc()}')

        else:
            return Api.safe_decode(response)

def _retry_request(exception: Exception, response: Response) -> bool:
    """
    Determines if a request should be retried based on the exception type.

    Arguments
    exception: (Exception) The exception that occurred.
    response: (Response) The response object from the request.

    Returns
    (bool) True if the request should be retried, False otherwise.
    """
    if isinstance(exception, HTTPError):
        if response:
            if response.status_code in RETRYABLE_HTTP_STATUS_CODES:
                return True

    elif isinstance(exception, RETRYABLE_EXCEPTIONS):
        return True

    return False

def _format_exception(exception: Exception) -> str:
    """
    Formats an exception into a string.

    Arguments
    exception: (Exception) The exception to format.

    Returns
    (str) The formatted exception.
    """
    exception_message = ''

    if isinstance(exception.args, tuple):
        exception_message = ", ".join(map(str, exception.args))

    elif isinstance(exception.args, str):
        exception_message = exception.args

    else:
        exception_message = str(exception)

    return f'{exception.__class__.__name__}: {exception_message}'
