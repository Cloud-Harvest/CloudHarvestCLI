from rich.prompt import Confirm, Prompt
from rich.text import Text
from .styling import TextColors
from typing import List


def input_pick_choices(prompt: str, data: List[dict], keys: list) -> str:
    """
    This function is used to display a list of choices to the user and return the user's selection.

    Parameters:
    prompt (str): The question that is displayed to the user.
    data (List[dict]): The data that is displayed to the user. Each dictionary in the list represents a record.
    keys (list): The keys that are used to display the data. Each key represents a column in the displayed table.

    Returns:
    str: The user's selection.
    """
    from .printing import print_data
    print_data(data=data, keys=keys, output_format='table', record_index_keyname='i')

    return Prompt().ask(prompt=Text(prompt, style=TextColors.PROMPT), choices=keys)


def input_boolean(prompt: str, yes_argument: bool = False) -> bool:
    """
    This function is used to ask the user a yes/no question and return the user's response as a boolean.

    Parameters:
    prompt (str): The question that is displayed to the user.
    yes_argument (bool, optional): If set to True, the function will automatically return True without asking the user. Default is False.

    Returns:
    bool: The user's response. Returns True if the user answers 'yes', and False if the user answers 'no'.
    """

    if yes_argument:
        return True

    else:
        return Confirm().ask(prompt=Text(prompt, style=TextColors.PROMPT))
