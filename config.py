#!/bin/env python3

from typing import Any


def main(reset: bool = False):
    from rich.console import Console

    console = Console()

    defaults = {
        'api': {
            'host': 'localhost',
            'port': 8000,
            'protocol': 'https'
        },
        'logging': {
            'level': 'warn',
            'location': './app/logs/'
        },
        'plugins': {

        },
        'theme': 'default'
    }

    console.print('\n'.join(['',
                             'Welcome to the Cloud Harvest CLI Configuration Tool!',
                             '',
                             'This tool will assist you in setting up your Cloud Harvest CLI.',
                             '* You can escape this process at any time with CTRL+C.',
                             '* You may also edit the file manually once it is created in ./app/harvest.json',
                             '* You can skip this process by copying an existing harvest.json to ./app/harvest.json',
                             '']))

    from os.path import exists

    if exists('../app/harvest.json') and reset is False:
        console.print('Loading existing configuration at `./app/harvest.json`', style='bold yellow')

        with open('../app/harvest.json', 'r') as existing_config_file_stream:
            from json import load
            existing_config = load(existing_config_file_stream)
            defaults.update(existing_config)

    try:
        defaults['api']['host'] = ask('Please enter the API host IP address, hostname, or domain name of the API service.',
                                      default=defaults['api']['host'], )
        defaults['api']['port'] = int(ask('Please enter the API port',
                                          default=defaults['api']['port']))
        defaults['api']['protocol'] = ask('Please enter the API protocol',
                                          choices=['http', 'https'],
                                          default=defaults['api']['protocol'])
        defaults['logging']['level'] = ask('Please enter the logging level',
                                           choices=['debug', 'info', 'warning', 'error', 'critical'],
                                           default=defaults['logging']['level'])
        defaults['logging']['location'] = ask('Please enter the logging location',
                                              default=defaults['logging']['location'])

        # Themes
        with open('CloudHarvestCLI/config/themes.yaml') as theme_stream:
            from yaml import load, FullLoader
            themes = load(theme_stream, Loader=FullLoader)

        if len(themes.keys()) > 1:
            from rich.table import Table, Row
            from rich.box import SIMPLE
            from rich.text import Text

            console.print()
            table = Table(title='Available Themes', box=SIMPLE)
            table.add_column('Name', overflow='fold')

            [table.add_column(col) for col in list(themes['default'].keys())]

            [
                table.add_row(*[Text(theme_name)] + [Text('SAMPLE', style=color) for output_type, color in color_pallet.items()])
                for theme_name, color_pallet in themes.items()
            ]

            console.print(table)

            defaults['theme'] = ask('Please select a theme',
                                    choices=themes.keys(),
                                    show_choices=False,
                                    default=defaults['theme'])

        else:
            console.print('Only one theme available. Skipping theme selection.', style='blue')

        if defaults.get('plugins'):
            from rich.table import Table
            from rich.box import SIMPLE
            table = Table(title='Existing Plugins', box=SIMPLE)
            table.add_column('Plugin URL', overflow='fold')
            table.add_column('Branch', overflow='fold')

            for plugin_url, plugin_branch in defaults['plugins'].items():
                table.add_row(plugin_url, plugin_branch)

            console.print()
            console.print(table)

            keep_existing_plugins = ask('Would you like to keep the existing plugins?', default='y')
            if keep_existing_plugins.lower() == 'n':
                defaults['plugins'] = {}
                console.print('\nExisting plugins will not be carried over.', style='yellow')

        add_plugins = ask('Would you like to add a plugin at this time? (y/n)', default='n')

        if add_plugins.lower() == 'y':
            while True:
                plugin_url = ask('Please enter the plugin URL or leave empty to stop adding plugins: ',
                                 default=None)

                if plugin_url is None:
                    break

                elif not plugin_url.endswith('.git'):
                    console.print('Invalid plugin URL provided. Plugin URL must end with .git. Please try again',
                                  style='bold red')
                    continue

                plugin_branch = ask('Please enter the plugin branch', default='main')

                defaults['plugins'][plugin_url] = plugin_branch

        install_binary = ask('Would you like to install the Cloud Harvest CLI binary?', default='y')
        if install_binary.lower() == 'y':
            with open('launch.sh', 'r') as harvest_stream:
                harvest_shell = harvest_stream.read()

            import os
            cur_dir = os.path.dirname(os.path.abspath(''))
            harvest_shell = harvest_shell.replace('install_path=$(realpath ".")',
                                                  f'install_path="{cur_dir}"')

            ulb = '/usr/local/bin'
            if os.access(ulb, os.W_OK):
                install_path = ulb

            else:
                install_path = os.path.abspath('')
                console.print(f'You do not have write access to {ulb}.\n'
                              f'Either copy the output file or add {install_path} to your $PATH\n', style='yellow')

            # write the file locally
            with open('harvest', 'w') as harvest_stream:
                harvest_stream.write(harvest_shell)

            from shutil import copy
            copy('harvest', os.path.join(install_path, 'harvest'))
            os.chmod(os.path.join(install_path, 'harvest'), 0o755)

            console.print(f'Binary installed to {os.path.join(install_path, "harvest")}', style='blue')

        else:
            console.print('Skipping binary installation.', style='blue')

    except KeyboardInterrupt:
        console.print('\nExiting...', style='bold red')
        exit(1)

    else:
        if not exists('app'):
            from os import mkdir
            mkdir('app')

        with open('./app/harvest.json', 'w') as config_file_stream:
            from json import dump
            dump(defaults, config_file_stream, indent=4, default=str)

        console.print()
        console.print('Configuration saved to ./app/harvest.json',
                      style='blue')
        from rich.text import Text
        console.print(Text('You may now start the Harvest CLI using the following command:', style='green') +
                      Text('./launch\n', style='blue'))


def ask(prompt: str, default: str = None, style: str = 'white', **kwargs) -> Any:
    from rich.prompt import Prompt
    from rich.text import Text

    result = Prompt.ask(prompt=Text('\n' + prompt, style=style),
                        default=None if default is None else str(default),
                        **kwargs)

    if default is None and result is None:
        result = None

    elif default is not None and result is None:
        result = default

    elif default is None and result is not None:
        result = result

    else:
        result = type(default)(result)

    return result


if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser(description='Cloud Harvest CLI Configuration Tool')
    parser.add_argument('--reset', action='store_true', help='Reset the configuration file to defaults')

    args = parser.parse_args()

    main(reset=args.reset)
