import socket as s
import sys

sys.path.append("..")
from standards import DISCONNECT_MSG, HEADER, FORMAT

class Connection:
    def __init__(self, ip: str, port: int):
        self.IP = ip
        self.PORT = port

        self.ADDR = (ip, port)

        self.client = None

    def connect(self) -> None:
        self.client = s.socket(s.AF_INET, s.SOCK_STREAM)
        self.client.connect(self.ADDR)

        print(f"[CONNECTED] Connected to the Server ({self.ADDR})")

    def disconnect(self) -> None:
        self.send(DISCONNECT_MSG)
        print(f"[DISCONNECTED] Disconected from the Server ({self.ADDR})")

    def recive(self) -> str:
        msg_len = self.client.recv(HEADER).decode(FORMAT)

        if not msg_len:
            return

        msg_len = int(msg_len)

        msg = self.client.recv(msg_len).decode(FORMAT)

        return msg

    def send(self, msg: str) -> None:
        message = msg.encode(FORMAT)

        msg_len = len(msg)
        send_len = str(msg_len).encode(FORMAT)
        send_len += b' ' * (HEADER - len(send_len))

        self.client.send(send_len)
        self.client.send(message)

if __name__ == "__main__":
    ...