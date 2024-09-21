import socket
import threading
import traceback
import sys

from Game import Game

sys.path.append("..")
from standards import PORT, HEADER, FORMAT, DISCONNECT_MSG

class Server:
    def __init__(self):
        self.SERVER_IP = socket.gethostbyname(socket.gethostname())
        self.ADDR = (self.SERVER_IP, PORT)

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(self.ADDR)

        self.MAX_PLAYERS = 2
        self.game = Game()

    def handle_client(self, conn: socket.socket, addr: tuple[str, int]) -> None:
        print(f"[NEW CONNECTION] {addr} connected")

        self.game.add_player(conn)

        try:
            while True:
                # Reciving length
                msg_len = conn.recv(HEADER).decode(FORMAT)

                if not msg_len:
                    return

                msg_len = int(msg_len)

                # Reciving message with given length
                msg = conn.recv(msg_len).decode(FORMAT)

                print(f"[{addr}] {msg}")

                self.game.recive(msg, conn)

                if msg == DISCONNECT_MSG:
                    self.game.end_connection(conn)
                    print(f"[CLIENT DISCONNECT] {addr} disconnected")
                    break

        except Exception:
            print(f"Error handling client {addr}")
            traceback.print_exc()

        conn.close()

    def start(self) -> None:
        self.server.listen()
        print(f"[LISTENING] Listening on {self.SERVER_IP}")

        while True:
            conn, addr = self.server.accept()

            thread = threading.Thread(target=self.handle_client, args=(conn, addr))
            thread.start()

            active = threading.active_count() - 1
            print(f"[ACTIVE CONNECTIONS] {active}")

            if active >= self.MAX_PLAYERS:
                print(f"[STARTING GAME] All {self.MAX_PLAYERS} have connected. Stopped listeing and starting the game")
                self.game.start()

if __name__ == "__main__":
    server = Server()
    server.start()

    if threading.active_count() == 1:
        server.server.close()
