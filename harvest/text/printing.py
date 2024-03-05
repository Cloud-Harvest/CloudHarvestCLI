from rich.console import Console
from .formatting import to_csv, to_json, to_table
from .styling import DEFAULT_TEST_COLOR_NAMES

output_console = Console()
feedback_console = Console(stderr=True)


def print_data(data: (list or dict), keys: list = None, flatten: str = None, unflatten: str = None,
               output_format: str = 'table', page: bool = False):
    """
    Displays data in one of many formats.
    :param data: printable data
    :param keys: the dictionary keys which shall be displayed (others will be hidden)
    :param flatten: flatten a dictionary based on the provided character
    :param unflatten: unflatten a dictionary based on the provided character
    :param output_format: the desired output format
    :param page: when true, output will be paged like `less` or `more`
    :return:
    """

    match output_format:
        case 'csv':
            output = to_csv(data=data, keys=keys)

        case 'json':
            output = to_json(data=data, keys=keys, flatten=flatten, unflatten=unflatten)

        case 'pretty-json':
            output = to_json(data=data, keys=keys, flatten=flatten, unflatten=unflatten)

        case 'table':
            output = to_table(data=data, keys=keys)

        case _:
            print_feedback(f'Invalid output format provided: `{output_format}`.', 'ERROR')
            return

    if page:
        from os import environ
        environ['MANPAGER'] = 'less -R'

        with output_console.pager(styles=True, links=True):
            output_console.print(output)

    else:
        output_console.print(output)


def print_message(text: str, color: DEFAULT_TEST_COLOR_NAMES):
    """
    Prints a rich formatted string.
    :param text: Text to print
    :param color: Color code to use
    :return:
    """

    from rich.style import Style
    from .styling import TextColors

    output_console.print(text, style=Style(color=getattr(TextColors, color.upper())))


def print_feedback(text: str, color: DEFAULT_TEST_COLOR_NAMES):
    from text.styling import TextColors
    from rich.style import Style

    feedback_console.print(text, style=Style(color=getattr(TextColors, color)))
