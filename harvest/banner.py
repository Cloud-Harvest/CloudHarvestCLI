"""
Font credits:
    https://web.archive.org/web/20120819044459/http://www.roysac.com/thedrawfonts-tdf.asp
    FIGFont created with: http://patorjk.com/figfont-editor
"""

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


def _get_eligible_banners():
    # we always provide a seasonal banner
    season = _get_season()



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
    for c in character_list:
        x, y, char, color = c

        for plan_colors in plan[x]:
            start = plan_colors.get('start') or 0
            end = plan_colors.get('end')
            planned_color = plan_colors.get('color')

            # if there is no 'end' and x is greater than or equal to 'start'
            if end is None and x >= start:
                c[3] = planned_color
                break

            # if start and end are defined
            elif start <= x <= end:
                c[3] = planned_color
                break

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

    _c = _assign_banner_colors(character_list=_b, plan=harvest_config['banners']['winter']['colors'])

    _d = _colorize_banner_list(character_list=_c)

    from rich.console import Console

    console = Console()
    console.print(_d)

    print('season: ' + _get_season())
