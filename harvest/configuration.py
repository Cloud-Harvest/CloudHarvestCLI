class HarvestConfiguration:
    """
    Static class which includes the contents of the harvest.yaml.
    Although strictly not needed, it is helpful to put the top-level keys and their respective types below as pointers
    for IDEs when developing. The content of the harvest.yaml is dynamically applied.
    """
    api = {}
    banners = {}
    colors = {}

    @staticmethod
    def load(config: dict):
        for k, v in config.items():
            setattr(HarvestConfiguration, k, v)


def load() -> dict:
    # create user directory
    from pathlib import Path
    Path('~/.harvest/cli/').expanduser().mkdir(parents=True, exist_ok=True)

    # enable the debug log file
    _configure_logger()

    # load configuration files
    config = _load_configuration()

    # store the version information in the config
    config['version'] = _get_version()

    HarvestConfiguration.load(config=config)

    # set theme colors
    from text.styling import TextColors
    TextColors.set_colors(**HarvestConfiguration.colors)

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
                           '~/.harvest/cli/harvest.yaml',
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

    with Path('~/.harvest/cli/logs').expanduser() as p:
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

