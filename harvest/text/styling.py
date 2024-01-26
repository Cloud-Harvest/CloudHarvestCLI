from rich.text import Text, Style


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
