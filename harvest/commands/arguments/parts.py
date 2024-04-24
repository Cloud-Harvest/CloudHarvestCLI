"""
parts.py - Reusable argument components which show up in different areas.

* When adding to parts, use the standard ArgumentParser(add_help=False).
* Provide examples where practical, especially if this is a part which is infrequently used.
* The calling Command's arguments.py should import the specific parers in question as parents=[].
* When calling, use Cmd2ArgumentParser(formatter_class=RawTextRichHelpFormatter) for proper syntax highlighting.
"""

from argparse import ArgumentParser

# PSTAR components
pstar_parser = ArgumentParser(add_help=False)
pstar_group = pstar_parser.add_argument_group('PSTAR')
pstar_group.add_argument('--platform', type=str,
                         help='Set the platform for the data.'
                              ' Example: `aws`')
pstar_group.add_argument('--service', type=str,
                         help='Set the service name for the data.'
                              ' Example: `rds`')
pstar_group.add_argument('--type', type=str,
                         help='Set the service subtype for the data.'
                              ' Example: instance')
pstar_group.add_argument('--account', type=str,
                         help='Set the platform account name for the data.'
                              ' Example: aws-business-development')
pstar_group.add_argument('--region', type=str,
                         help='The account geographical region.'
                              ' Example: us-east-1')

# Matching -m
matching_parser = ArgumentParser(add_help=False)
matching_parser_group = matching_parser.add_argument_group('Matching')
matching_parser_group.add_argument('-m', '--matches', action='append', nargs='+', default=[],
                                   help='\n'.join([
                                       'Provide matching statements. Matches are defined in the following ways:',
                                       'Syntax                              | Description',
                                       '----------------------------------- | -------------------------------------------------',
                                       '`-m Field=Value`                    | Just match this field/value.',
                                       '`-m Field=Value Field=Value`        | One `-m` and multiple field/value pairs is an `AND`.',
                                       '`-m Field=Value` `-m Field=Value`   | Additional `-m` are an `OR`.',
                                       '',
                                       'Note: When using the `|`, `<`, and `>` characters, you must enclose the',
                                       '      entire -m statement in quotes: `-m "Field=Value|Value"` else the command',
                                       '      will be interpreted as a redirect to another command.'
                                   ]))

# Formatting --format
format_parser = ArgumentParser(add_help=False)
format_parser_group = format_parser.add_argument_group('Formatting')
format_parser_group.add_argument('--format', default='table', choices=['csv', 'json', 'pretty-json', 'table'],
                                 help='Sets the command output format. Users can route output to files using `> path`.')
format_parser_group.add_argument('--flatten', default=None, type=str,
                                 help='Converts a nested JSON object into a one with a single key/value pair with'
                                      ' fields separated by the character provided.')
format_parser_group.add_argument('--unflatten', default=None,
                                 help='Converts a flattened JSON object into a nested object based on the character'
                                      ' provided.')
format_parser_group.add_argument('--page', action='store_true',
                                 help='Output is halted when it fills the screen, similar to `less` or `more`')

# Add/Remove Keys and Headers
key_manipulation_parser = ArgumentParser(add_help=False)
key_manipulation_parser_group = key_manipulation_parser.add_argument_group('Key Manipulation')
key_manipulation_parser_group.add_argument('-a', '--add-keys', nargs='+', default=[],
                                           help='Append keys to the report output.')
key_manipulation_parser_group.add_argument('-e', '--exclude-keys', nargs='+', default=[],
                                           help='Removes keys from the report output.')
key_manipulation_parser_group.add_argument('-H', '--header-order', nargs='+', default=[],
                                           help='Changes the header order to the provided input. Fields not included are'
                                                ' hidden as if the user removed the them with `-e`.')

refresh_parser = ArgumentParser(add_help=False)
refresh_parser_group = refresh_parser.add_argument_group('Refresh')
refresh_parser_group.add_argument('--refresh', type=float, default=0, help='Refresh the output n seconds.')

# Thread Controls
thread_parser = ArgumentParser(add_help=False)
thread_parser_group = thread_parser.add_argument_group('Threading')
thread_parser_group.add_argument('--background', action='store_true',
                                 help='Sends a threaded process to the background instead of displaying the progress bar.')
thread_parser_group.add_argument('--max-workers', type=int, default=0,
                                 help='Sets the number of simultaneous tasks for this command.'
                                      ' When not provided, uses a value equal to thw number of cores, minus one.')

# Yes
yes_parser = ArgumentParser(add_help=False)
yes_parser.add_argument('-y', '--yes', action='store_true', help='Automatically answer yes to all prompts.')
