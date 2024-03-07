# TODO: remote messages from the server
from typing import Any, List


class Messages:
    queue = []


def add_message(parent: Any, style: str, *args):
    new_message = (parent, style, ' '.join([str(a) for a in args]))

    # prevent spamming of the same message
    if new_message not in Messages.queue:
        Messages.queue.append(new_message)

    return Messages


def read_messages() -> List[tuple]:
    """
    :return: (parent, style, message)
    """

    # get the last message position
    last_message = len(Messages.queue)

    # copy the messages to be read out of the queue
    messages = Messages.queue[0: last_message]

    # remove the copied messages from the queue
    del Messages.queue[0: last_message]

    return messages


if __name__ == '__main__':
    default_color_names = ['HEADER', 'PROMPT', 'INFO', 'WARN', 'ERROR']
    [
        Messages.add(__name__, color, f'test message {color}')
        for color in default_color_names
    ]

    expected_queue = [(__name__, color, f'test message {color}') for color in default_color_names]

    assert Messages.queue == expected_queue

    read_result = Messages.read()
    assert read_result == expected_queue and Messages.queue == []

    from text.printing import print_message
    [print_message(text=message[2], color=message[1]) for message in read_result]
