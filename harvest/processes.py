from threading import Thread

MESSAGE_QUEUE = []
ABORT_THREAD = False


def start_thread() -> Thread:
    from time import sleep

    def _message_queue_thread():
        while ABORT_THREAD is False:
            sleep(1)


def add(command):
    from datetime import datetime
    MESSAGE_QUEUE.append()