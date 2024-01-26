# TODO: remote messages from the server
from text.styling import TextColors

class Messages:
    queue = []

    @staticmethod
    def add(*args, style: str):
        Messages.queue.append((' '.join([str(a) for a in args]), style))

        return Messages

    @staticmethod
    def read() -> list:
        # get the last message position
        last_message = len(Messages.queue)

        # copy the messages to be read out of the queue
        messages = Messages.queue[0: last_message]

        # remove the copied messages from the queue
        [Messages.queue.remove(message) for message in messages]

        return messages
