from CloudHarvestCLI.commands.settings.plugin.arguments import plugin_parser
from CloudHarvestCLI.configuration import HarvestConfiguration

def do_plugin(args):
    from CloudHarvestCLI.messages import print_message
    from CloudHarvestCLI.plugins import generate_plugins_file, install_plugins, read_plugins_file

    if args.plugins_subcommand == 'add':
        from re import fullmatch
        package = args.url_or_package_name

        if fullmatch('^(http|https)://', package):
            package = f'git+{package}'

        new_plugin = {
            'url_or_package_name': package,
            'branch': args.branch
        }

        # Check if the plugin is already configured
        if any(plugin['url_or_package_name'] == package for plugin in HarvestConfiguration.plugins or []):
            print_message('WARN', False,f'Plugin `{package}` already configured')
            return

        else:
            plugins = HarvestConfiguration.plugins or [] + [new_plugin]

        # Update the local configuration
        HarvestConfiguration.update_config('plugins', plugins)

        # Store the plugins in the plugins.txt file
        from CloudHarvestCLI.plugins import generate_plugins_file
        generate_plugins_file()

        # Regenerate local configuration from file
        HarvestConfiguration.update_config('plugins', read_plugins_file())

        print_message('INFO', False, f'Added plugin {package}')

    elif args.plugins_subcommand == 'list':
        from CloudHarvestCLI.text.printing import print_data
        plugins = HarvestConfiguration().plugins

        if not plugins:
            print_message('WARN', False, 'No plugins configured')
            return

        else:
            print_data(data=plugins,
                       keys=['index', 'url_or_package_name', 'branch'],
                       record_index_keyname='index')

    elif args.plugins_subcommand == 'install':
        generate_plugins_file()
        install_plugins()

    elif args.plugins_subcommand == 'remove':
        from CloudHarvestCLI.text.inputs import input_pick_choices

        if not HarvestConfiguration.plugins:
            print_message('WARN', False, 'No plugins configured')
            return

        # Let the user select the plugin to remove
        index_or_package = input_pick_choices(
            prompt='Select the plugin to remove',
            data=HarvestConfiguration.plugins,
            keys=['index', 'url_or_package_name'],
            record_index_identifier='index'
        )

        # Identify the index of the plugin to remove
        if index_or_package.isdigit() and int(index_or_package) in range(len(HarvestConfiguration.plugins)):
            index = int(index_or_package)

        else:
            for plugin in HarvestConfiguration.plugins:
                if plugin['url_or_package_name'] == index_or_package:
                    index = HarvestConfiguration.plugins.index(plugin)
                    break

            else:
                print_message('ERROR', False, 'Invalid selection')
                return

        # If the index is valid, remove the plugin
        if index in range(len(HarvestConfiguration.plugins)):
            plugins = HarvestConfiguration.plugins
            old_plugin = plugins.pop(index)

            # Update the local configuration
            HarvestConfiguration.update_config('plugins', plugins)

            # Store the plugins in the plugins.txt file
            generate_plugins_file()

            print_message('INFO',False, f'Removed plugin {old_plugin["url_or_package_name"]}',)

        else:
            print_message('ERROR', False, 'Invalid selection')

    else:
        print_message('ERROR', False, 'Invalid subcommand')
        plugin_parser.print_help()
