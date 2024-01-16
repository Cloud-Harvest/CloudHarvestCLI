from rich.text import Text, Style
from rich.table import Table


class TextColors:
    # default colors
    HEADER = '#4AF626'      # terminal green
    PROMPT = '#00FFFF'      # cyan
    INFO = '#75BFEC'        # light blue
    WARN = '#EED202'        # warning yellow
    ERROR = '#FF0F0F'       # bright red

    @staticmethod
    def set_colors(**kwargs):
        for k, v in kwargs.items():
            setattr(TextColors, k, v)

        return TextColors


def _hex_to_rgb(color_hex: str) -> tuple:
    """
    Convert a hex color code to RGB.
    :param color_hex: Hex code starting with or without '#'
    :return: tuple(r, g, b)
    """

    # modified from https://stackoverflow.com/a/29643643
    return tuple(int(color_hex.lstrip('#')[i:i + 2], 16) for i in (0, 2, 4))


def colorize(text: str, color: str) -> str:
    """
    Return a colorized string.
    :param text: String to colorize.
    :param color: Color hex code.
    :return: str
    """
    from cmd2 import RgbFg, style
    result = style(text, fg=RgbFg(*_hex_to_rgb(color)))

    return result


def stylize(text: str, **style) -> Text:
    """
    Style a rich.Text object and return the Text result. rich.Style is more robust, allowing formatting with italics,
    bold, paragraphs, and wraps. Use rich.print() or rich.console.print() to display the output of this function.
    :param text: String to stylize.
    :param style: rich.Style kwargs
    :return: rich.Text
    """

    result = Text(text=text,
                  style=Style(**style))

    return result


class FormattedOutput:
    def __init__(self, data, keys: list = None):
        self.data = data
        self.keys = keys or []

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        del self.data
        return None

    def to_csv(self):
        from csv import DictWriter
        from io import StringIO
        stream = StringIO()
        dict_writer = DictWriter(stream, fieldnames=self.keys)
        dict_writer.writeheader()
        dict_writer.writerows(self.data)

        return stream.getvalue()

    def to_json(self, flatten: str = None, unflatten: str = None):
        # skip if the data is not an appropriate type
        if not isinstance(self.data, (dict, list)):
            return self.data

        if flatten:
            data = self._flatten(separator=flatten)

        elif unflatten:
            data = self._unflatten(separator=unflatten)

        else:
            data = self.data

        from json import dumps
        result = dumps(data, default=str)

        return result

    def to_table(self) -> Table:
        from rich.table import Table
        from rich.box import SIMPLE

        table = Table(box=SIMPLE)
        [table.add_column(c) for c in self.keys]

        [table.add_row(*[r.get(k) for k in self.keys]) for r in self.data]

        return table

    def _flatten(self, separator: str):
        from flatten_json import flatten

        if isinstance(self.data, list):
            result = [flatten(d, separator=separator) for d in self.data]

        elif isinstance(self.data, dict):
            result = flatten(self.data, separator=separator)

        else:
            result = self.data

        return result

    def _unflatten(self, separator: str):
        from flatten_json import unflatten_list
        result = unflatten_list({'result': self.data}, separator=separator)

        return result


if __name__ == '__main__':
    import rich

    print('rich print (stylize)-----------')
    rich.print(stylize('A lovely header', color=TextColors.HEADER))
    rich.print(stylize('[prompt]', color=TextColors.PROMPT))
    rich.print(stylize('Just some info', color=TextColors.INFO))
    rich.print(stylize('Be warned!', color=TextColors.WARN))
    rich.print(stylize('Straight up error!', color=TextColors.ERROR))

    print('colorize print-----------')
    print(colorize('A lovely header', color=TextColors.HEADER))
    print(colorize('[prompt]', color=TextColors.PROMPT))
    print(colorize('Just some info', color=TextColors.INFO))
    print(colorize('Be warned!', color=TextColors.WARN))
    print(colorize('Straight up error!', color=TextColors.ERROR))

    test_data = [
        {"A": "a1", "B": "b1"},
        {"A": "a2", "B": "b2"},
        {"A": "a3", "B": "b3"},
    ]

    with FormattedOutput(data=test_data, keys=["A", "B"]) as formatter:
        print('csv-------------')
        print(formatter.to_csv())

        print('json-------------')
        print(formatter.to_json())

        print('pretty-json-------------')
        rich.print_json(formatter.to_json())

        print('table-------------')
        rich.print(formatter.to_table())
