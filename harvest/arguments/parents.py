from argparse import ArgumentParser

# Matching -m
matching_parser = ArgumentParser(add_help=False)
matching_parser_group = matching_parser.add_argument_group('Matching')
matching_parser_group.add_argument('-m', '--match', action='append', nargs='+', default=[],
                                   help='Provide matching statements. Matches are defined in the following ways:\n'
                                        'One match statement                : `-m Field=Value`\n'
                                        'A single `-m` are AND statements   : `-m Field=Value Field=Value`\n'
                                        'Additional `-m` is an OR statement : `-m Field=Value` `-m Field=Value`.')

# Formatting --format
format_parser = ArgumentParser(add_help=False)
format_parser_group = format_parser.add_argument_group('Formatting')
format_parser_group.add_argument('--format', default='tabular', choices=['csv', 'json', 'pretty-json', 'tabular'],
                                 help='Sets the command output format. Users can route output to files using `> path`.')
format_parser_group.add_argument('--flatten', default=None, type=str,
                                 help='Converts a nested JSON object into a one with a single key/value pair with'
                                      ' fields separated by the character provided.')
format_parser_group.add_argument('--unflatten', default=None,
                                 help='Converts a flattened JSON object into a nested object based on the character'
                                      ' provided.')

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
