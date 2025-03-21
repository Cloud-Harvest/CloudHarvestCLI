from logging import getLogger

from CloudHarvestCLI.configuration import HarvestConfiguration

logger = getLogger('harvest')


def generate_plugins_file():
    """
    Populates the plugins.txt file with the plugins to install
    """

    with open('./app/plugins.txt', 'w') as plugins_file:
        for plugin in HarvestConfiguration.plugins or []:

            # Check if the plugin is a git repository or a URL
            from re import compile

            git_pattern = compile(r'^(git\+|)(http|https)://')
            if git_pattern.match(plugin['url_or_package_name']):
                # Get the package name from the URL
                package_name = plugin['url_or_package_name'].split('/')[-1].split('.')[0]

                if 'git+' not in plugin['url_or_package_name']:
                    url = f'git+{plugin["url_or_package_name"]}'

                else:
                    url = plugin["url_or_package_name"]

                branch_name = plugin.get('branch') or 'master'
                output_string = f'{package_name} @ {url}@{branch_name}\n'

            else:
                output_string = plugin['url_or_package_name']

            plugins_file.write(output_string)
            logger.debug(f'Plugin {output_string} written to plugins.txt')


def install_plugins(quiet: bool = False):
    """
    Installs the plugins in the plugins.txt file
    """

    from subprocess import run
    command = ['pip', 'install', '-r', './app/plugins.txt']

    if quiet:
        command.append('--quiet')

    execution = run(command)

    if execution.returncode == 0:
        logger.info('Plugins installed successfully')

    else:
        logger.error('Error installing plugins')

    from CloudHarvestCorePluginManager import register_all
    register_all()

def read_plugins_file():
    """
    Reads the plugins.txt file and returns the list of plugins
    """

    with open('./app/plugins.txt') as plugins_file:
        plugins = [
            line.strip()
            for line in plugins_file.readlines()
        ]

    result = []

    for plugin in plugins:
        if 'git+' in plugin:
            plugin_split = plugin.split('@')
            url = plugin_split[1].replace('git+', '').strip()

            if len(plugin_split) > 2:
                branch = plugin_split[2].strip()

            else:
                branch = 'main'

            result.append({
                'url_or_package_name': url,
                'branch': branch
            })

        else:
            result.append({
                'url_or_package_name': plugin.replace('\n', '')
            })

    return result
