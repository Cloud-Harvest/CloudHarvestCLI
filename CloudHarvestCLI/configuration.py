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
    plugins = {}
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
        if not exists('./app/harvest.json'):
            logger.error('Configuration file `./app/harvest.json` not found. '
                         'Please run the configuration tool ./config.py.')

            from sys import exit
            exit(1)

        with open('./app/harvest.json', 'r') as stream:
            import json
            config = json.load(stream)

        for key, value in config.items():
            setattr(HarvestConfiguration, key, value)

        from json import load
        with open('./meta.json', 'r') as meta_file_stream:
            meta = load(meta_file_stream)

        HarvestConfiguration.version = meta['version']

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

        return HarvestConfiguration
