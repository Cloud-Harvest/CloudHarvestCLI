"""
Font credits:
    https://web.archive.org/web/20120819044459/http://www.roysac.com/thedrawfonts-tdf.asp
    FIGFont created with: http://patorjk.com/figfont-editor
"""
from rich.text import Text

_characters = {
    'a': ('█████╗  ',
          '██╔══██╗',
          '███████║',
          '██╔══██║',
          '██║  ██║',
          '╚═╝  ╚═╝'),

    'b': ('██████╗ ',
          '██╔══██╗',
          '██████╔╝',
          '██╔══██╗',
          '██████╔╝',
          '╚═════╝ '),

    'c': ('██████╗ ',
          '██╔════╝',
          '██║     ',
          '██║     ',
          '╚██████╗',
          '╚═════╝ '),

    'd': ('██████╗ ',
          '██╔══██╗',
          '██║  ██║',
          '██║  ██║',
          '██████╔╝',
          '╚═════╝ '),

    'e': ('███████╗',
          '██╔════╝',
          '█████╗  ',
          '██╔══╝  ',
          '███████╗',
          '╚══════╝'),

    'f': ('███████╗',
          '██╔════╝',
          '█████╗  ',
          '██╔══╝  ',
          '██║     ',
          '╚═╝     '),

    'g': ('██████╗  ',
          '██╔════╝ ',
          '██║  ███╗',
          '██║   ██║',
          '╚██████╔╝',
          '╚═════╝  '),

    'h': ('██╗  ██╗',
          '██║  ██║',
          '███████║',
          '██╔══██║',
          '██║  ██║',
          '╚═╝  ╚═╝'),

    'i': ('██╗',
          '██║',
          '██║',
          '██║',
          '██║',
          '╚═╝'),

    'j': ('██╗     ',
          '██║     ',
          '██║     ',
          '██   ██║',
          '╚█████╔╝',
          '╚════╝  '),

    'k': ('██╗  ██╗',
          '██║ ██╔╝',
          '█████╔╝ ',
          '██╔═██╗ ',
          '██║  ██╗',
          '╚═╝  ╚═╝'),

    'l': ('██╗     ',
          '██║     ',
          '██║     ',
          '██║     ',
          '███████╗',
          '╚══════╝'),

    'm': ('███╗   ███╗',
          '████╗ ████║',
          '██╔████╔██║',
          '██║╚██╔╝██║',
          '██║ ╚═╝ ██║',
          '╚═╝     ╚═╝'),

    'n': ('███╗   ██╗',
          '████╗  ██║',
          '██╔██╗ ██║',
          '██║╚██╗██║',
          '██║ ╚████║',
          '╚═╝  ╚═══╝'),

    'o': ('██████╗  ',
          '██╔═══██╗',
          '██║   ██║',
          '██║   ██║',
          '╚██████╔╝',
          '╚═════╝  '),

    'p': ('██████╗ ',
          '██╔══██╗',
          '██████╔╝',
          '██╔═══╝ ',
          '██║     ',
          '╚═╝     '),

    'q': ('██████╗  ',
          '██╔═══██╗',
          '██║   ██║',
          '██║▄▄ ██║',
          '╚██████╔╝',
          '╚══▀▀═╝  '),

    'r': ('██████╗ ',
          '██╔══██╗',
          '██████╔╝',
          '██╔══██╗',
          '██║  ██║',
          '╚═╝  ╚═╝'),

    's': ('███████╗',
          '██╔════╝',
          '███████╗',
          '╚════██║',
          '███████║',
          '╚══════╝'),

    't': ('████████╗',
          '╚══██╔══╝',
          '   ██║   ',
          '   ██║   ',
          '   ██║   ',
          '   ╚═╝   '),

    'u': ('██╗   ██╗',
          '██║   ██║',
          '██║   ██║',
          '██║   ██║',
          '╚██████╔╝',
          '╚═════╝  '),

    'v': ('██╗   ██╗',
          '██║   ██║',
          '██║   ██║',
          '╚██╗ ██╔╝',
          ' ╚████╔╝ ',
          '  ╚═══╝  '),

    'w': ('██╗    ██╗',
          '██║    ██║',
          '██║ █╗ ██║',
          '██║███╗██║',
          '╚███╔███╔╝',
          ' ╚══╝╚══╝ '),

    'x': ('██╗  ██╗',
          '╚██╗██╔╝',
          ' ╚███╔╝ ',
          ' ██╔██╗ ',
          '██╔╝ ██╗',
          '╚═╝  ╚═╝'),

    'y': ('██╗   ██╗',
          '╚██╗ ██╔╝',
          ' ╚████╔╝ ',
          '  ╚██╔╝  ',
          '   ██║   ',
          '   ╚═╝   '),

    'z': ('███████╗',
          '╚══███╔╝',
          '  ███╔╝ ',
          ' ███╔╝  ',
          '███████╗',
          '╚══════╝'),

    '1': (' ██╗',
          '███║',
          '╚██║',
          ' ██║',
          ' ██║',
          ' ╚═╝'),

    '2': ('██████╗ ',
          '╚════██╗',
          '█████╔╝ ',
          '██╔═══╝ ',
          '███████╗',
          '╚══════╝'),

    '3': ('██████╗ ',
          '╚════██╗',
          ' █████╔╝',
          ' ╚═══██╗',
          '██████╔╝',
          '╚═════╝ '),

    '4': ('██╗  ██╗',
          '██║  ██║',
          '███████║',
          '╚════██║',
          '     ██║',
          '     ╚═╝'),

    '5': ('███████╗',
          '██╔════╝',
          '███████╗',
          '╚════██║',
          '███████║',
          '╚══════╝'),

    '6': (' ██████╗',
          '██╔════╝',
          '███████╗',
          '██╔═══██╗',
          '╚██████╔╝',
          ' ╚═════╝'),

    '7': ('███████╗',
          '╚════██║',
          '   ██╔╝ ',
          '  ██╔╝  ',
          '  ██║   ',
          '  ╚═╝   '),

    '8': (' █████╗ ',
          '██╔══██╗',
          '╚█████╔╝',
          '██╔══██╗',
          '╚█████╔╝',
          ' ╚════╝ '),

    '9': (' █████╗ ',
          '██╔══██╗',
          '╚██████║',
          ' ╚═══██║',
          ' █████╔╝',
          ' ╚════╝'),

    '0': (' ██████╗',
          '██╔═████╗',
          '██║██╔██║',
          '████╔╝██║',
          '╚██████╔╝',
          ' ╚═════╝   '),

    ' ': ('  ',
          '  ',
          '  ',
          '  ',
          '  ',
          '  ')
}


def get_banner(banner_configuration: dict, name: str = None, text: str = 'HARVEST') -> Text:
    """
    Generates a banner based on the banner's name. The banner must be printed with rich.Console().print().
    :param banner_configuration: the Harvest Configuration's `banners` key
    :param name: The name of a banner key in the harvest.yaml, banners section.
    :param text: The text to convert to a banner.
    :return: rich.text.Text
    """

    if name:
        banner = banner_configuration.get(name)

    else:
        from random import randrange
        eligible_banners = _get_eligible_banners(banner_configuration=banner_configuration)
        banner = eligible_banners[randrange(0, len(eligible_banners))]

    banner_text = _text_to_banner(text)
    character_list = _banner_to_character_list(text=banner_text)
    assigned_colors = _assign_banner_colors(character_list=character_list, plan=banner['colors'])
    result = _colorize_banner_list(character_list=assigned_colors)

    return result


def _get_eligible_banners(banner_configuration: dict) -> list:
    """
    Generates a list of banners based on season, date, or other rules/
    :return: List
    """
    # we always provide a seasonal banner

    banners = [banner_configuration[_get_season()]]

    # date logic
    # specific date

    # date range

    return banners


def _get_season():
    from datetime import date, datetime

    now = datetime.now().date()
    seasons = [('winter', (date(now.year, 1, 1), date(now.year, 3, 20))),
               ('spring', (date(now.year, 3, 21), date(now.year, 6, 20))),
               ('summer', (date(now.year, 6, 21), date(now.year, 9, 22))),
               ('autumn', (date(now.year, 9, 23), date(now.year, 12, 20))),
               ('winter', (date(now.year, 12, 21), date(now.year, 12, 31)))]

    return next(season for season, (start, end) in seasons
                if start <= now <= end)


def _text_to_banner(text: str) -> str:
    """
    Converts a string into banner _characters. If the character is not present in _characters, it returns the ' ' value.
    :param text: any string
    :return:
    """

    chars = [_characters.get(str(t).lower()) or _characters[' '] for t in text]

    rows = []
    for i in range(len(_characters['a'])):
        row = ''
        for c in chars:
            row += c[i]

        rows.append(row)

    return '\n'.join(rows)


def _banner_to_character_list(text: str) -> list:
    result = []

    rows = text.split('\n')

    for x in range(len(rows)):
        for y in range(len(rows[x])):
            result.append([x, y, rows[x][y], '#ffffff'])  # assign the default color here

    sorted(result, key=lambda element: (element[1], element[2]))

    return result


def _assign_banner_colors(character_list: list, plan: dict) -> list:
    max_x, max_y = character_list[-1][0], character_list[-1][1]

    for c in character_list:
        x, y, char, color = c

        if plan.get(x):
            for plan_colors in plan.get(x):
                start = plan_colors.get('start') or 0
                end = plan_colors.get('end')
                planned_color = plan_colors.get('color')

                colorize_cell = False

                # when the range is a percentage of the row length
                if start < 1 and end:
                    from math import floor, ceil
                    perc_start = floor(start * max_y)
                    perc_end = ceil(end * max_y)

                    if perc_start <= y <= perc_end:
                        colorize_cell = True

                # if there is no 'end' and x is greater than or equal to 'start'
                if end is None and x >= start:
                    colorize_cell = True

                # exact cell start/end position
                elif start == y == end:
                    colorize_cell = True

                # if start and end are defined
                elif start <= y <= end:
                    colorize_cell = True

                if colorize_cell:
                    c[3] = planned_color

        else:
            continue

    return character_list


def _colorize_banner_list(character_list: list):
    from rich.text import Text, Style

    result = Text()

    last_x = None

    for char in character_list:
        x, y, character, color = char

        # new line after x position changes
        if last_x != x and last_x is not None:
            result += f'\n'

        result += Text(text=character, style=Style(color=color))

        last_x = x

    return result


if __name__ == '__main__':
    _a = _text_to_banner("HARVEST")
    print(_a)
    assert _a == '██╗  ██╗█████╗  ██████╗ ██╗   ██╗███████╗███████╗████████╗\n' \
                 '██║  ██║██╔══██╗██╔══██╗██║   ██║██╔════╝██╔════╝╚══██╔══╝\n' \
                 '███████║███████║██████╔╝██║   ██║█████╗  ███████╗   ██║   \n' \
                 '██╔══██║██╔══██║██╔══██╗╚██╗ ██╔╝██╔══╝  ╚════██║   ██║   \n' \
                 '██║  ██║██║  ██║██║  ██║ ╚████╔╝ ███████╗███████║   ██║   \n' \
                 '╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝  ╚═══╝  ╚══════╝╚══════╝   ╚═╝   '

    _b = _banner_to_character_list(text=_a)

    with open('../harvest.yaml', 'r') as harvest_stream:
        from yaml import load, FullLoader

        harvest_config = load(harvest_stream, Loader=FullLoader)

    _c = _assign_banner_colors(character_list=_b, plan=harvest_config['banners']['spring']['colors'])

    _d = _colorize_banner_list(character_list=_c)

    from rich.console import Console

    console = Console()
    console.print(_d)

    print('season: ' + _get_season())
