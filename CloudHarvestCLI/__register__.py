"""
The `__register__.py` module is used to register objects that should be placed in the
`CloudHarvestCorePluginManager.registry.Registry`. Here, they are loaded via the `__main__.py` -> `app.py`
startup process. Note that even though these modules do not appear to be used, they are necessary to register
definitions and instances with the PluginManager Registry.

Furthermore, objects which are to be registered with the PluginManager Registry must be wrapped with one of the
following decorators available in the CloudHarvestCorePluginManager.decorators module:
- `register_definition`: Used to register objects, like classes, with the PluginManager Registry.
- `register_instance`: Used to register instances, such as instantiations of classes, with the PluginManager Registry.

cmd2.CommandSets are handled a little differently. They are registered with cmd2 simply by importing them at some point
in the application's execution. This is because cmd2.CommandSets are automatically registered with the cmd2.Cmd. For
that reason, is it not necessary to wrap cmd2.CommandSets with the `register_definition` decorator.
"""

# import commands
from commands import *
