import pygame as py
import sys

sys.path.append("..")
from standards import SERVER_IP, PORT

from Connection import Connection
from Assets import Assets

from states.State import State
from states.GameState import GameState
from states.MenuState import MenuState

py.init()

class Main:
    def __init__(self):
        self.running = True
        
        self.WINDOW_WIDTH = 1280
        self.WINDOW_HEIGHT = 720

        self.win = py.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        py.display.set_caption("UNO")
        self.clock = py.time.Clock()

        self.connection = Connection(SERVER_IP, PORT)
        self.connection.connect()
        self.connected = True

        Assets.load_assets()

        State.add_state("GameState", GameState(self))
        State.add_state("MenuState", MenuState(self))
        State.switch_state("GameState")

    def render(self) -> None:
        if not State.get_state():
            self.running = False
            return

        self.win.fill((0, 0, 0))

        State.get_state().render(self.win)

        py.display.flip()

    def tick(self) -> None:
        if not State.get_state():
            self.running = False
            return

        for event in py.event.get():
            if event.type == py.QUIT:
                self.running = False
                if self.connected:
                    self.connection.disconnect()

        State.get_state().tick()

        self.clock.tick(60)
        
    def run(self) -> None:
        while self.running:
            self.render()
            self.tick()

if __name__ == "__main__":
    main = Main()
    main.run()

    py.quit()
