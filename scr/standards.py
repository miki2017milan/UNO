import sys

HEADER = 64
SERVER_IP = "192.168.178.77"
PORT = 5052
ADDR = (SERVER_IP, PORT)
FORMAT = "utf-8"
DISCONNECT_MSG = "!DISCONNECT"
GAMESTART_MSG = "!GAMESTART"
ASSETS_PATH = sys.path[0].replace("scr/client", "assets/")
