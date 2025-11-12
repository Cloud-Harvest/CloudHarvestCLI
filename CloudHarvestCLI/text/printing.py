from argparse import Namespace
from rich.console import Console
from typing import List

from CloudHarvestCLI.text.formatting import to_csv, to_json, to_table

output_console = Console()
feedback_console = Console(stderr=True)


def print_data(data: (dict, List[dict]), keys: (list, tuple) = None, flatten: str = None, unflatten: str = None,
               list_separator:str = '\n', output_format: str = 'table', page: bool = False, as_feedback: bool = False,
               record_index_keyname: str = None, sort_by_keys: list = None, title: str = None,
               with_freshness: bool = False, with_record_count: bool = False):
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
    :param with_freshness: Include a column indicating how recent the records are
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
        # _keys.sort()

    else:
        _keys = keys

    if record_index_keyname and isinstance(data, list):
        data = [{**{record_index_keyname: index}, **record} for index, record in enumerate(data)]

        if record_index_keyname not in _keys:
            _keys += [record_index_keyname]

    if with_freshness:
        _keys.insert(0, 'f')

        data = _add_freshness(
            data=data,
            include_fresh_color=True if output_format == 'table' else False,
            include_row_formatting=True if output_format == 'table' else False
        )

    # if sort_by_keys:
    #     from natsort import natsorted
    #     data = natsorted(data, key=lambda d: [d.get(k) for k in _keys])

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


def print_task_response(report_response: List[dict] or dict, args: Namespace, **kwargs):
    from CloudHarvestCLI.messages import print_message

    if isinstance(report_response, list):
        # Recursively print each report in the list
        [
            print_task_response(report_response=report, args=args, **kwargs)
            for report in report_response
        ]

    elif isinstance(report_response, dict):
        data = report_response.get('data') or {}
        meta = report_response.get('meta') or {}
        metrics = report_response.get('metrics') or []

        has_task_errors = any(bool(task.get('Errors')) for task in metrics or [])

        if data:
            print_data(data=report_response['data'],
                       keys=meta.get('headers'),
                       title=meta.get('title'),
                       output_format='pretty-json' if args.describe else (args.format or 'table'),
                       flatten=args.flatten,
                       unflatten=args.unflatten,
                       page=args.page,
                       with_record_count=False,
                       with_freshness=not args.suppress_freshness,
                       **kwargs)

        if args.performance or has_task_errors:
            print_data(data=metrics,
                       keys=['Position', 'Name', 'Class', 'Records', 'Status', 'Duration', 'Attempts', 'DataBytes', 'Errors'],
                       output_format='table',
                       page=args.page,
                       title='Error Report' if has_task_errors else 'Performance Report',
                       with_record_count=False)

        if metrics and metrics[-1].get('Duration'):
                print_message('INFO', True, f'{len(data)} records in {metrics[-1]["Duration"] * 1000:.2f} ms')


def _add_freshness(data: (list or dict), include_row_formatting: bool = False, include_fresh_color: bool = False) -> list:
    class FreshnessCode:
        def __init__(self, code: str, description: str, color: str, max_second_age: float = None,
                     row_format: dict = None):
            """
            A FreshnessCode provides quick visible context for records displayed in a table.
            """

            self.code = code
            self.color = color
            self.description = description
            self.max_second_age = max_second_age

            from rich.style import Style
            self.fresh_format = Style(color=self.color)
            self.row_format = Style(**row_format) if row_format else None

    # Ensure the data is a DataSet
    from CloudHarvestCoreTasks.dataset import DataSet
    data = DataSet(data if isinstance(data, list) else [data])

    # We define these on each report in case the theme changes. TODO: implement an event handler for theme changes.
    from CloudHarvestCLI.text.styling import TextColors
    fresh = FreshnessCode('F', 'fresh', TextColors.INFO, max_second_age=3600)
    aging = FreshnessCode('A', 'aging', TextColors.WARN, max_second_age=7200)
    old = FreshnessCode('O', 'old', TextColors.ERROR)
    inactive = FreshnessCode('I', 'inactive', TextColors.HEADER)  # , row_format={'italic': True}
    unknown = FreshnessCode('U', 'unknown', TextColors.PROMPT)

    for record in data:
        is_active = record.walk('Harvest.Active')
        last_seen = record.walk('Harvest.Dates.LastSeen')

        if str(last_seen):
            from datetime import datetime
            last_seen = datetime.fromisoformat(last_seen)

        # Default freshness code
        fresh_code = unknown

        if is_active is False:
            fresh_code = inactive

        elif is_active:
            if last_seen:
                from datetime import datetime, timezone
                record_age = (datetime.now(tz=timezone.utc) - last_seen).total_seconds()

                if record_age < fresh.max_second_age:
                    fresh_code = fresh

                elif record_age < aging.max_second_age:
                    fresh_code = aging

                else:
                    fresh_code = old

        # Apply Text Style encoding to the record
        from rich.text import Text
        if include_row_formatting and fresh_code.row_format:
            # Apply row-wide formatting to values
            for key, value in record.items():
                record[key] = Text(str(value), style=fresh_code.row_format)

        # Add the freshness column
        if include_fresh_color:
            record['f'] = Text(fresh_code.code, style=fresh_code.fresh_format)

        else:
            record['f'] = fresh_code.code

    return data
