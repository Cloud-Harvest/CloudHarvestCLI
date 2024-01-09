
def prepare() -> dict:
    _configure_logger()
    config = _load_configuration()

    config['version'] = _get_version()

    return config


def _get_first_path(*args) -> str:
    from os.path import expanduser, exists
    for a in args:
        if a:
            path = expanduser(a)
            if exists(path):
                return path


def _load_configuration() -> dict:
    from os import environ
    path = _get_first_path(environ.get('HARVEST_CONFIG'),
                           '~/.harvest/harvest.yaml',
                           './harvest.yaml')

    from yaml import load, FullLoader
    with open(path, 'r') as config_stream:
        config = load(config_stream, Loader=FullLoader)

    return config


def _configure_logger():
    from logging import getLogger, DEBUG
    from logging.handlers import RotatingFileHandler

    logger = getLogger('harvest')

    [logger.removeHandler(handler) for handler in logger.handlers]

    from pathlib import Path

    with Path('~/.harvest/logs').expanduser() as p:
        p.expanduser()
        p.mkdir(parents=True, exist_ok=True)

        rfh = RotatingFileHandler(filename=p.joinpath('harvest.log'),
                                  maxBytes=5000000,
                                  backupCount=10)

        rfh.setLevel(DEBUG)

    logger.addHandler(rfh)

    return getLogger('harvest')


def _get_version() -> str:
    with open('./version') as version_stream:
        return str(version_stream.read().strip())

