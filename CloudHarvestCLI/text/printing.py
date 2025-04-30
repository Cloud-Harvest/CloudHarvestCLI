from rich.console import Console
from typing import List

from CloudHarvestCLI.text.formatting import to_csv, to_json, to_table

output_console = Console()
feedback_console = Console(stderr=True)


def print_data(data: (dict, List[dict]), keys: (list, tuple) = None, flatten: str = None, unflatten: str = None,
               list_separator:str = '\n', output_format: str = 'table', page: bool = False, as_feedback: bool = False,
               record_index_keyname: str = None, sort_by_keys: list = None, title: str = None,
               with_record_count: bool = False):
    """
    Displays data in one of many formats.
    :param data: printable data
    :param keys: the dictionary keys which shall be displayed (others will be hidden).
    :param flatten: flatten a dictionary based on the provided character
    :param unflatten: unflatten a dictionary based on the provided character
    :param list_separator: the separator character to use when displaying lists
    :param output_format: the desired output format
    :param page: when true, output will be paged like `less` or `more`
    :param as_feedback: When True, output will use the feedback_console which writes information to stderr.
    This distinction is important when deciding if information should be capture by terminal routing operators such as >
    :param record_index_keyname: Include a column with the record index
    :param sort_by_keys: A list of keys used to sort the data by
    :param with_record_count: Include a line with the total number of records as defined by data
    :param title: A title to display above the data

    :return: None (prints information to feedback_ or output_console)
    """

    from CloudHarvestCLI.messages import add_message

    if as_feedback:
        console = feedback_console

    else:
        console = output_console

    if not keys:
        _keys = []
        [
            _keys.extend(list(record.keys()))
            for record in data if isinstance(record, dict)
        ]

        _keys = list(set(_keys))
        _keys.sort()

    else:
        _keys = keys

    if record_index_keyname and isinstance(data, list):
        data = [{**{record_index_keyname: index}, **record} for index, record in enumerate(data)]

        if record_index_keyname not in _keys:
            _keys += [record_index_keyname]

    if sort_by_keys:
        from natsort import natsorted
        data = natsorted(data, key=lambda d: [d.get(k) for k in _keys])

    match output_format:
        case 'csv':
            output = to_csv(data=data, keys=_keys)

        case 'json' | 'pretty-json':
            from json import dumps
            output = dumps(to_json(data=data, keys=_keys, flatten=flatten, unflatten=unflatten), default=str)

        case 'table':
            output = to_table(data=data, keys=_keys, flatten_data=flatten, list_separator=list_separator, sort_keys=sort_by_keys, title=title)

        case _:
            add_message(None,'ERROR',True, f'Invalid output format provided: `{output_format}`.')
            return

    if page:
        from os import environ
        environ['MANPAGER'] = 'less -R'

        with console.pager(styles=True, links=True):
            console.print_json(output, indent=2, highlight=True) if 'json' in output_format else console.print(output)

    else:
        console.print_json(output, indent=2, highlight=True) if 'json' in output_format else console.print(output)

    if with_record_count and isinstance(data, list):
        add_message(None,'INFO', True, f'records: {len(data)}')
