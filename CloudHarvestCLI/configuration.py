from logging import getLogger, Logger
logger = getLogger('harvest')


class HarvestConfiguration:
    """
    Static class which includes the contents of the harvest configuration directory.
    Although strictly not needed, it is helpful to put the top-level keys and their respective types below as pointers
    for IDEs when developing. The content of the configuration directory is dynamically applied.
    """
    api = {}
    banners = {}
    logging = {}
    plugins = []
    shortcuts = {}
    theme: str = 'default'
    themes = {}
    version: str = '0.0.0'

    @staticmethod
    def load():
        """
        Load the configuration from the configuration directory.
        """
        from os.path import exists, join

        # get the user config
        if not exists('./app/harvest.yaml'):
            from shutil import copyfile
            logger.info('No configuration file found. Using default configuration file.')
            copyfile('./harvest.yaml', './app/harvest.yaml')

        with open('./app/harvest.yaml', 'r') as stream:
            from yaml import load, FullLoader
            config = load(stream, Loader=FullLoader)

        for key, value in config.items():
            setattr(HarvestConfiguration, key, value)

        from tomli import load
        with open('./pyproject.toml', 'br') as meta_file_stream:
            meta = load(meta_file_stream)

        HarvestConfiguration.version = meta['project']['version']

        # get the YAML files in CloudHarvestCLI/config/
        from os import listdir
        from yaml import load, FullLoader
        for file in listdir('./CloudHarvestCLI/config/'):
            if file.endswith('.yaml'):
                with open(join('./CloudHarvestCLI/config/', file), 'r') as stream:
                    config = load(stream, Loader=FullLoader)
                    setattr(HarvestConfiguration, file.split('.')[0], config)

        from CloudHarvestCLI.text.styling import TextColors
        TextColors.set_colors(**HarvestConfiguration.themes.get(HarvestConfiguration.theme))

        HarvestConfiguration.configure_logger(
            log_destination=HarvestConfiguration.logging.get('location') or './app/logs/',
            log_level=HarvestConfiguration.logging.get('level') or 'DEBUG',
            quiet=HarvestConfiguration.logging.get('quiet') or False
        )

        return HarvestConfiguration

    @staticmethod
    def configure_logger(log_destination: str = './app/logs/', log_level: str = 'info', quiet: bool = False, **kwargs) -> Logger:
        """
        This method configures logging for the api.

        Arguments
        log_destination (str, optional): The destination directory for the log file. Defaults to './app/logs/'.
        log_level (str, optional): The logging level. Defaults to 'info'.
        quiet (bool, optional): Whether to suppress console output. Defaults to False.
        """
        level = log_level

        from logging import getLogger, Formatter, StreamHandler, DEBUG
        from logging.handlers import RotatingFileHandler

        # startup
        new_logger = getLogger(name='harvest')

        # If the logger exists, remove all of its existing handlers
        if new_logger.hasHandlers():
            [
                new_logger.removeHandler(handler)
                for handler in new_logger.handlers
            ]

        from importlib import import_module
        lm = import_module('logging')
        log_level_attribute = getattr(lm, level.upper())

        # formatting
        log_format = Formatter(fmt='[%(asctime)s][%(levelname)s][%(filename)s] %(message)s')

        # file handler
        from pathlib import Path
        from os.path import abspath, expanduser
        _location = abspath(expanduser(log_destination))

        # make the destination log directory if it does not already exist
        Path(_location).mkdir(parents=True, exist_ok=True)

        # configure the file handler
        from os.path import join
        fh = RotatingFileHandler(join(_location, 'cli.log'), maxBytes=10000000, backupCount=5)
        fh.setFormatter(fmt=log_format)
        fh.setLevel(DEBUG)

        new_logger.addHandler(fh)

        if not quiet:
            # stream handler
            sh = StreamHandler()
            sh.setFormatter(fmt=log_format)
            sh.setLevel(log_level_attribute)
            new_logger.addHandler(sh)

        new_logger.setLevel(log_level_attribute)

        new_logger.debug(f'Logging enabled successfully. Log location: {log_destination}')

        return new_logger

    @staticmethod
    def update_config(key: str, value: any):
        """
        Updates the local configuration and the configuration file with the provided key and value.
        """

        # update the local configuration
        setattr(HarvestConfiguration, key, value)

        # update the configuration file
        from yaml import load, dump, FullLoader
        with open('./app/harvest.yaml', 'r') as stream:
            current_config = load(stream, Loader=FullLoader)

        with open('./app/harvest.yaml', 'w') as stream:
            current_config[key] = getattr(HarvestConfiguration, key)
            dump(current_config, stream)

        logger.debug(f'Updated configuration: {key} with value: {str(value)}')
