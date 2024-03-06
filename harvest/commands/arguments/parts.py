from argparse import ArgumentParser

# PSTAR components
pstar_parser = ArgumentParser(add_help=False)
pstar_group = pstar_parser.add_argument_group('PSTAR')
pstar_group.add_argument('--platform', type=str,
                         help='Set the platform for the data.'
                              '\nExample: `aws`')
pstar_group.add_argument('--service', type=str,
                         help='Set the service name for the data.'
                              '\nExample: `rds`')
pstar_group.add_argument('--type', type=str,
                         help='Set the service subtype for the data.'
                              '\nExample: instance')
pstar_group.add_argument('--account', type=str,
                         help='Set the platform account name for the data.'
                              '\nExample: aws-business-development')
pstar_group.add_argument('--region', type=str,
                         help='The account geographical region.'
                              '\nExample: us-east-1')

# Matching -m
matching_parser = ArgumentParser(add_help=False)
matching_parser_group = matching_parser.add_argument_group('Matching')
matching_parser_group.add_argument('-m', '--match', action='append', nargs='+', default=[],
                                   help='\n'.join([
                                       'Provide matching statements. Matches are defined in the following ways:',
                                       'One match statement matches on just that field/value | `-m Field=Value`',
                                       'A single `-m` are AND statements                     | `-m Field=Value Field=Value`',
                                       'Additional `-m` is an OR statement                   | `-m Field=Value` `-m Field=Value`.'
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
