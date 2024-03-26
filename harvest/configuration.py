import datetime
from logging import getLogger
logger = getLogger('harvest')


class HarvestConfiguration:
    """
    Static class which includes the contents of the harvest configuration directory.
    Although strictly not needed, it is helpful to put the top-level keys and their respective types below as pointers
    for IDEs when developing. The content of the configuration directory is dynamically applied.
    """
    api = {}
    banners = {}
    themes = {}
    version: str = '0.0.0'

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
    config = _load_configuration_files()

    HarvestConfiguration.load(config=config)

    # set theme colors
    from text.styling import TextColors
    TextColors.set_colors(**HarvestConfiguration.themes['themes'].get(HarvestConfiguration.themes.get('active_theme') or 'default'))

    return config


def _get_first_path(*args) -> str:
    from os.path import expanduser, exists
    for a in args:
        if a:
            path = expanduser(a)
            if exists(path):
                return path


def _load_configuration_files() -> dict:
    from os import environ
    from os import listdir
    from os.path import abspath, basename, exists, isfile, join

    source_path = abspath('./harvest/config')
    target_path = abspath(_get_first_path(environ.get('HARVEST_CONFIG'), '~/.harvest/cli/'))

    version = _get_version()

    config = {
        'version': version
    }

    for file in listdir(source_path):
        source_file = join(source_path, file)
        target_file = join(target_path, file)

        if isfile(source_file) and file.endswith('.yaml'):
            if exists(target_file):
                source_version = load_yaml_file(source_file, safe_loader=False)['.schema']['version']
                target_version = load_yaml_file(target_file, safe_loader=False)['.schema']['version']
                source_date = convert_version_to_date(source_version)
                target_date = convert_version_to_date(target_version)

                if source_date > target_date:
                    from messages import add_message
                    add_message(__name__, 'WARN', f'The configuration file {target_file}',
                                f'({target_version}) is older than the source version ({source_version}).')

            else:
                from shutil import copyfile
                copyfile(source_file, target_file)

            configuration_part = basename(file)[0:-5]

            from yaml import load, FullLoader
            with open(join(target_path, file), 'r') as config_stream:
                config[configuration_part] = load(config_stream, Loader=FullLoader)

    return config


def convert_version_to_date(version: str) -> datetime.date:
    return datetime.date(*[int(part) for part in version.split('.')])


def load_yaml_file(path: str, safe_loader: bool = True) -> (list or dict):
    from yaml import load, SafeLoader, FullLoader
    with open(path, 'r') as file:
        result = load(file, Loader=SafeLoader if safe_loader else FullLoader)

    return result


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
