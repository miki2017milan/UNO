import pygame as py

from states.State import State

class MenuState(State):
    def __init__(self, main):
        super().__init__(main)

        self.font = py.font.SysFont("Mononoki Nerd Font", 50)
        self.menu_text = self.font.render("Main Menu", True, (255, 255, 255))

    def render(self, win):
        win.fill((60, 60, 60))

        win.blit(self.menu_text, (100, 270))

    def tick(self):
        pass

    def recive(self):
        pass
        