import pygame as py
import threading

from states.State import State

import sys
sys.path.append("..")

from standards import GAMESTART_MSG, DISCONNECT_MSG

from Assets import Assets

class GameState(State):
    def __init__(self, main):
        super().__init__(main)

        self.game_started = False
        self.current_player = 0
        self.top_card = ""
        self.players = []

        self.cards = []
        self.id = None

        self.font = py.font.SysFont("Mononoki Nerd Font", 30)
        self.waiting_text = self.font.render("Waiting for the game to start...", True, (255, 255, 255))

        thread = threading.Thread(target=self.recive)
        thread.start()

    def render(self, win) -> None:
        win.fill((60, 60, 60))

        if not self.game_started:
            win.blit(self.waiting_text, (110, 270))
            return

        if self.id == self.current_player:
            win.fill((60, 80, 60))

        win.blit(self.font.render(f"ID: {self.id}", True, (255, 255, 255)), (10, 10))

        win.blit(Assets.card_into_image(self.top_card), (300, 100))

        for i, card in enumerate(self.cards):
            win.blit(Assets.card_into_image(card), (i * Assets.CARD_WIDTH + 10, 500))

    def tick(self) -> None:
        pass

    def draw_cards(self) -> None:
        pass
    
    """
    Sending Pattern: (the number indicates wich character is meant)
    0: what type of information is send('s': stating the game 'i': round info 'd': drawing a card)

    s)
    1: own id

    i)
    1: currentplayer
    2-3: current top card
    4-...: own cards and other players cards divieded by , and : for next player

    d)
    1-...: cards you get devied by ,
    """

    def recive(self) -> None:
        while True:
            msg = self.main.connection.recive()

            if not msg:
                break

            print(f"[SERVER] {msg}")

            if msg == GAMESTART_MSG:
                self.game_started = True

                print("[GAME STARTED]")
                continue

            if msg == DISCONNECT_MSG:
                self.main.connection.disconnect()
                self.main.connected = False
                break

            if msg[0] == 's': # Starting info message
                self.id = int(msg[1])
                print("ID: ", self.id)

            # Example: "i1r1,r4b5y2ys,5:2:"
            if msg[0] == "i": # Round info message
                data = msg.split(",")

                self.current_player = int(data[0][1])
                self.top_card = data[0][2:4]

                self.cards = []
                for c in range(0, len(data[1]), 2):
                    self.cards.append(data[1][c:c+2])

                print(self.cards)

                other_players_card_count = data[2].split(":")
                other_players_card_count.pop()
                for i in range(len(other_players_card_count)):
                    self.players.append(int(other_players_card_count[i]))

                # self.players.insert(self.id, self.cards)

                print(self.players)

        State.switch_state("End")
        