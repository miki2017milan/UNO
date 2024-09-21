import random
import sys

from Player import Player

sys.path.append("..")
from standards import GAMESTART_MSG

import socket

"""
Card Codes
r - red
g - green
b - blue
y - yellow

c - cycle card
s - skip card
t - plus 2

ow - wish card
of - 4 plus
ou - up side down
"""

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

class Game:
    def __init__(self):
        self.STARTING_CARDS = 7
        self.players = []
        self.current_player = 0
        self.play_cycle = 1 # Direction to play (clockwise +1 counter clockwise -1)

        self.deck = self.generate_deck()
        self.discarded_deck = [self.deck.pop()]

    def start(self) -> None:
        for i, p in enumerate(self.players):
            p.send(GAMESTART_MSG)
            p.send("s" + str(i))
            p.send(self.get_round_info(i))

    def get_round_info(self, player: int) -> str:
        msg = f"i{self.current_player}{self.discarded_deck[-1]},"

        for card in self.players[player].cards:
            msg += card

        msg += ","

        for i, player in enumerate(self.players):
            if i == self.current_player:
                continue

            msg += str(len(player.cards)) + ":"

        return msg

    def add_player(self, conn: socket.socket) -> None:
        self.players.append(Player(conn, self.give_hand()))

    def recive(self, msg: str, sender: socket.socket) -> None:
        pass

    def give_hand(self) -> str:
        return [self.deck.pop() for i in range(self.STARTING_CARDS)]

    def generate_deck(self) -> list[str]:
        deck = []

        for color in ["r", "g", "b", "y"]:
            for card in [str(i) for i in range(10)] + ["c", "s", "t"]:
                if not card == "0":
                    deck.append(color + card)
                deck.append(color + card)

        for i in range(4): 
            deck.append("ow")
            deck.append("of")

        random.shuffle(deck)

        return deck

    def end_connection(self, sender: socket.socket) -> None:
        for i in range(len(self.players) - 1, -1, -1):
            if not self.players[i].client == sender: # Exclude sender (first client who disconnected)
                self.players[i].disconnect()
            self.players.pop(i)

if __name__ == "__main__":
    pass
