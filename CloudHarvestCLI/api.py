from CloudHarvestCLI.messages import print_message

from logging import getLogger
from requests.adapters import HTTPAdapter
from requests import JSONDecodeError, Session
from typing import Any, Literal
from urllib3.util.retry import Retry


HTTP_REQUEST_TYPES = Literal['get', 'post', 'put', 'delete']
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
    session: Session | None = None

    previous_token = None

    @staticmethod
    def config(host: str, port: int, token: str = None, pem: str = None, verify: (bool | str) = False):
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
    def init_session(pool_connections: int = 3, pool_maxsize: int = 5, backoff_factor: float = 0.3, total: int = 10,
                     connect: int = 10, other: int = 10, status:int = 10, read: int = 10, redirect: int = 10) -> Session:
        """
        Initializes a session for making requests to the API.

        Arguments
        pool_connections: (int) The number of connections to keep in the pool.
        pool_maxsize: (int) The maximum number of connections to keep in the pool.
        backoff_factor: (float) The backoff factor to use for retries.
        total: (int) The total number of retries to allow.
        connect: (int) The number of retries to allow on connection errors.
        other: (int) The number of retries to allow on other errors.
        status: (int) The number of retries to allow on status errors.
        read: (int) The number of retries to allow on read errors.
        redirect: (int) The number of retries to allow on redirect errors.

        Returns
        (Session) The initialized session.
        """

        # Return the existing session if it exists and the token has not changed
        if Api.session is not None:
            # If the token has changed, close the existing session and create a new one
            if Api.token == Api.previous_token:
                try:
                    Api.session.close()

                except Exception as e:
                    pass

            # If the token has not changed, return the existing session
            else:
                return Api.session

        session = Session()
        # Update the previous token so we can detect changes
        Api.previous_token = Api.token
        session.headers.update({'Authorization': f'Bearer {Api.token}' if Api.token else ''})

        # Create the Retry object which will be used to configure the HTTPAdapter.
        retry = Retry(
            total=total,
            connect=connect,
            other=other,
            read=read,
            redirect=redirect,
            status=status,
            backoff_factor=backoff_factor,
        )
        adapter = HTTPAdapter(pool_connections=pool_connections, pool_maxsize=pool_maxsize, max_retries=retry)
        session.mount('https://', adapter)
        session.mount('http://', adapter)
        Api.session = session

        return session

    @staticmethod
    def safe_decode(response) -> Any:
        """
        Safely decodes a response from the API.

        Arguments
        response: (dict) The response to decode.

        Returns
        (dict) The decoded response.
        """

        try:
            result = response.json()

        except JSONDecodeError as e:
            result = f'Failed to decode response JSON: {e}'

        return result


def request(request_type: HTTP_REQUEST_TYPES, endpoint: str, data: dict = None, session_kwargs: dict = None, **requests_kwargs) -> Any:
    """
    Makes an API request to the CloudHarvest API.

    Arguments
    host: (str) The host of the API.
    port: (int) The port of the API.
    token: (str) The token to authenticate with the API.
    request_type: (str) The type of request to make (GET, POST, PUT, DELETE).
    endpoint: (str) The endpoint to make the request to.
    data: (dict) The data to send with the request.
    session_kwargs: (dict, optional) Additional keyword arguments to pass to the session initializer.
    **requests_kwargs: Additional keyword arguments to pass to the requests library.

    """

    # Initialize the session
    Api.init_session(**(session_kwargs or {}))

    # Disable SSL warnings which are raised when using self-signed certificates
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    try:
        response = Api.session.request(
            method=request_type,
            url=f'https://{Api.host}:{Api.port}/{endpoint}',
            cert=Api.pem,
            json=data or {},
            verify=Api.verify,
            **requests_kwargs
        )

        return response.json()

    except KeyboardInterrupt:
        print_message('INFO', True, 'Acknowledged user interrupt.')

    except Exception as e:
        print_message('ERROR', True, f'An error occurred while making the request: {e}')
