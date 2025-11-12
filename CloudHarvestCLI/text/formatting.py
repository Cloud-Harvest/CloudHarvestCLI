from typing import Literal, List
from rich.table import Table
from io import StringIO


def get_formatter(method: Literal['from', 'to'], extension: str):
    from importlib import import_module
    self = import_module(__name__)

    f = f'{method}_{extension}'

    if hasattr(self, f):
        return getattr(self, f)

    else:
        return None


def from_csv(filename: str or StringIO, **kwargs) -> list:
    from csv import DictReader

    if isinstance(filename, StringIO):
        _stream = filename

    else:
        from os.path import expanduser
        _stream = open(expanduser(filename), 'r')

    _dict_reader = list(DictReader(_stream, **kwargs))

    return _dict_reader


def to_csv(data: (list or dict), keys: list = None) -> str:
    """
    Convert a flattened dictionary to CSV.
    :param data:
    :param keys:
    :return:
    """
    from csv import DictWriter
    from io import StringIO

    _keys = keys or _identify_keys(data)

    # We remove keys which are not defined in _keys and add missing keys as unexpected or missing keys raise errors
    # in the DictWriter.writerows() method.
    _data = [
        {
            k: record.get(k)
            for k in _keys
        }
        for record in data
    ]

    _stream = StringIO()
    dict_writer = DictWriter(_stream, fieldnames=_keys)
    dict_writer.writeheader()
    dict_writer.writerows(_data)

    return _stream.getvalue()


def to_json(data, keys: list = None, flatten: str = None, unflatten: str = None):
    """
    Converts data into a JSON object
    :param data: the data to format
    :param keys: list of keys to display
    :param flatten: the separator character to use when flattening data
    :param unflatten: the separator character ot use when unflattening data
    :return: Any
    """

    # skip if the data is not an appropriate type
    if not isinstance(data, (dict, list)):
        return data

    if flatten:
        result = _flatten(data=data, separator=flatten)

    elif unflatten:
        result = _unflatten(data=data, separator=unflatten)

    else:
        result = data

    if keys:
        if isinstance(data, list):
            result = [_strip_keys(record=r) for r in result]

        elif isinstance(data, dict):
            result = _strip_keys(record=data)

    return result


def to_table(data: (list or dict),
             flatten_data: str = False,
             keys: list = None,
             sort_keys: List[str] = None,
             list_separator: str = '\n',
             title: str = None) -> Table or str:

    from rich.table import Table
    from rich.box import SIMPLE
    from rich.text import Text

    table = Table(box=SIMPLE, title=title)

    from CloudHarvestCoreTasks.dataset import DataSet
    data = DataSet(data if isinstance(data, list) else [data])

    # add headers to the table
    [
        table.add_column(key, overflow='fold')
        for key in keys or data.keys
    ]

    if flatten_data:
        data.flatten()

    if sort_keys:
        data.sort_records(keys=sort_keys)

    # add data to table
    for row in data:
        r = []
        for k in keys or data.keys:
            v = row.walk(k)

            if v is None:
                r.append('')

            elif isinstance(v, dict):
                from json import dumps
                r.append(dumps(v))

            elif isinstance(v, list):
                r.append(list_separator.join([str(s) for s in v]))

            # If the text was previously formatted, preserve it as-is
            elif isinstance(v, Text):
                r.append(v)

            else:
                r.append(str(v))

        table.add_row(*r)

    return table


def _identify_keys(data: (list or dict)) -> list:
    flat_data = _flatten(data)

    # dictionaries are easy: they're just the already-existing keys
    if isinstance(flat_data, dict):
        _result = list(flat_data.keys())

    # lists of dict are more complicated: that involves looping over each record
    elif isinstance(flat_data, list):
        _keys = []
        [
            _keys.extend(list(r.keys()))
            if isinstance(r, dict) else r
            for r in flat_data
        ]

        _result = list(set(_keys))

    else:
        return []

    del flat_data

    return _result


def _flatten(data, separator: str = '.'):
    from flatten_json import flatten

    if isinstance(data, list):
        result = [
            flatten(d, separator=separator)
            if isinstance(d, dict) else d
            for d in data
        ]

    elif isinstance(data, dict):
        result = flatten(data, separator=separator)

    else:
        result = data

    return result


def _unflatten(data: list or dict, separator: str = '.') -> list or dict:
    from flatten_json import unflatten_list

    result = data

    if isinstance(data, dict):
        result = unflatten_list(data, separator=separator)

    elif isinstance(data, list):
        result = [unflatten_list(d, separator=separator) for d in data]

    return result


def _strip_keys(record: dict, keys: list = None) -> dict:
    if keys:
        return {k: v for k, v in record.items() if k in keys}

    else:
        return record
