# TODO: remote messages from the server
from typing import Any, Generator, Tuple


class Messages:
    queue = []


def add_message(parent: Any, style: str, *args):
    new_message = (parent, style, ' '.join([str(a) for a in args]))

    # prevent spamming of the same message
    if new_message not in Messages.queue:
        Messages.queue.append(new_message)

    return Messages


def read_messages() -> Generator[Tuple[Any, str, str], None, None]:
    """
    Reads messages from the queue, removing them in the process.
    :return: Generator yielding tuples of (parent, style, message)
    """

    while Messages.queue:
        yield Messages.queue.pop(0)


if __name__ == '__main__':
    default_color_names = ['HEADER', 'PROMPT', 'INFO', 'WARN', 'ERROR']
    [
        add_message(__name__, color, f'test message {color}')
        for color in default_color_names
    ]

    expected_queue = [(__name__, color, f'test message {color}') for color in default_color_names]

    assert Messages.queue == expected_queue

    read_result = read_messages()
    assert read_result == expected_queue and Messages.queue == []

    from text.printing import print_text
    [print_text(text=message[2], color=message[1]) for message in read_result]
