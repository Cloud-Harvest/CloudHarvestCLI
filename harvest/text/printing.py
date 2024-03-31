from rich.console import Console
from .formatting import to_csv, to_json, to_table
from .styling import DEFAULT_TEST_COLOR_NAMES

output_console = Console()
feedback_console = Console(stderr=True)


def print_data(data: (list or dict), keys: list = None, flatten: str = None, unflatten: str = None,
               output_format: str = 'table', page: bool = False, as_feedback: bool = False,
               record_index_keyname: str = None, sort_by_keys: list = None, with_record_count: bool = False):
    """
    Displays data in one of many formats.
    :param data: printable data
    :param keys: the dictionary keys which shall be displayed (others will be hidden)
    :param flatten: flatten a dictionary based on the provided character
    :param unflatten: unflatten a dictionary based on the provided character
    :param output_format: the desired output format
    :param page: when true, output will be paged like `less` or `more`
    :param as_feedback: When True, output will use the feedback_console which writes information to stderr.
    This distinction is important when deciding if information should be capture by terminal routing operators such as >
    :param record_index_keyname: Include a column with the record index
    :param sort_by_keys: A list of keys used to sort the data by
    :param with_record_count: Include a line with the total number of records as defined by data
    :return: None (prints information to feedback_ or output_console)
    """

    if as_feedback:
        console = feedback_console

    else:
        console = output_console

    if record_index_keyname and isinstance(data, list):
        data = [{**{record_index_keyname: index}, **record} for index, record in enumerate(data)]
        keys += [record_index_keyname]

    if sort_by_keys:
        from natsort import natsorted
        data = natsorted(data, key=lambda d: [d.get(k) for k in keys])

    match output_format:
        case 'csv':
            output = to_csv(data=data, keys=keys)

        case 'json' | 'pretty-json':
            output = to_json(data=data, keys=keys, flatten=flatten, unflatten=unflatten)

        case 'table':
            output = to_table(data=data, keys=keys)

        case _:
            print_message(f'Invalid output format provided: `{output_format}`.', 'ERROR', as_feedback=True)
            return

    if page:
        from os import environ
        environ['MANPAGER'] = 'less -R'

        with console.pager(styles=True, links=True):
            console.print(output)

    else:
        console.print(output)

    if with_record_count and isinstance(data, list):
        print_message(f'records: {len(data)}', color='INFO', as_feedback=True)


def print_message(text: str, color: DEFAULT_TEST_COLOR_NAMES, as_feedback: bool = False):
    """
    Prints a rich formatted string.
    :param text: Text to print
    :param color: Color code to use
    :param as_feedback: When True, output will use the feedback_console which writes information to stderr.
    This distinction is important when deciding if information should be capture by terminal routing operators such as >
    :return: None (prints information to feedback_ or output_console)
    """

    from rich.style import Style
    from .styling import TextColors

    if as_feedback:
        console = feedback_console

    else:
        console = output_console

    console.print(text, style=Style(color=getattr(TextColors, color.upper())))
