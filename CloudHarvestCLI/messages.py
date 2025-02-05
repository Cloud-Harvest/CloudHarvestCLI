# TODO: remote messages from the server
from typing import Any, Generator, Tuple
from text.styling import VALID_TEXT_COLOR_NAMES

class Messages:
    queue = []


def add_message(parent: Any, style: VALID_TEXT_COLOR_NAMES, as_feedback: bool, *args):
    """
    Adds a message to the message queue.

    Arguments
    parent (Any): The parent object of the message.
    style (VALID_TEXT_COLOR_NAMES): The style of the message.
    as_feedback (bool): Whether the message should be displayed as feedback.
    args: The message arguments.

    Returns
    (Messages) The Messages object.
    """

    new_message = (parent, style, as_feedback, ' '.join([str(a) for a in args]))

    # prevent spamming of the same message
    if new_message not in Messages.queue:
        Messages.queue.append(new_message)

    return Messages


def read_messages() -> Generator[Tuple[Any, VALID_TEXT_COLOR_NAMES, bool, str], None, None]:
    """
    Reads messages from the queue, removing them in the process.
    :return: Generator yielding tuples of (parent, style, message)
    """

    while Messages.queue:
        yield Messages.queue.pop(0)


def print_all_messages():
    """
    Prints all messages in the queue.
    :return: None
    """

    for message in read_messages():
        source, color, as_feedback, text = message

        print_message(text=text, color=color, as_feedback=as_feedback)


def print_message(text: str, color: VALID_TEXT_COLOR_NAMES, as_feedback: bool = False):
    """
    Prints a rich formatted string.
    :param text: Text to print
    :param color: Color code to use
    :param as_feedback: When True, output will use the feedback_console which writes information to stderr.
    This distinction is important when deciding if information should be capture by terminal routing operators such as >
    :return: None (prints information to feedback_ or output_console)
    """

    from rich.style import Style
    from text.styling import TextColors
    from text.printing import feedback_console, output_console

    if as_feedback:
        console = feedback_console

    else:
        console = output_console

    console.print(text, style=Style(color=getattr(TextColors, color.upper())))
