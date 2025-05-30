from rich.prompt import Confirm, Prompt
from rich.text import Text
from CloudHarvestCLI.text.styling import TextColors
from typing import List


def input_pick_choices(prompt: str, data: List[dict], keys: list, selection_keys: list = None, record_index_identifier: str = 'i') -> str:
    """
    This function is used to display a list of choices to the user and return the user's selection.

    Parameters:
    prompt (str): The question that is displayed to the user.
    data (List[dict]): The data that is displayed to the user. Each dictionary in the list represents a record.
    keys (list): The keys that are used to display the data. Each key represents a column in the displayed table.
    selection_keys (list, optional): The keys that are used to populate the choices list. Default is None. When None,
                                     the function will use the keys parameter instead.
    record_index_identifier (str, optional): The key that is used to identify each record. Default is 'i'.

    Returns:
    str: The user's selection.
    """
    from CloudHarvestCLI.text.printing import print_data
    print_data(data=data, keys=keys, output_format='table', record_index_keyname=record_index_identifier)

    choices = [
        record.get(key)
        for key in selection_keys or keys
        for record in data
        if record.get(key) is not None
    ]

    # Add the record index to the choices list
    choices += [str(i) for i in range(len(data))]

    return Prompt().ask(prompt=Text(prompt, style=TextColors.PROMPT), choices=choices, show_choices=False)


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
