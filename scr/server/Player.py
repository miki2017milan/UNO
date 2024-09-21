import socket
import sys

sys.path.append("..")
from standards import DISCONNECT_MSG, FORMAT, HEADER



class Player:
    def __init__(self, client: socket.socket, cards: list[str]):
        self.client = client
        self.cards = cards

    def disconnect(self) -> None:
        self.send(DISCONNECT_MSG)

    def send(self, msg) -> None:
        message = msg.encode(FORMAT)

        msg_len = len(msg)
        send_len = str(msg_len).encode(FORMAT)
        send_len += b' ' * (HEADER - len(send_len))

        self.client.send(send_len)
        self.client.send(message)