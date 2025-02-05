from typing import Literal
from rich.text import Text, Style

VALID_TEXT_COLOR_NAMES = Literal['HEADER', 'PROMPT', 'INFO', 'WARN', 'ERROR']


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
    Return a colorized string designed for ascii output. This method should not be used in conjunction with rich.console
    as it will print the literal color values.
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
