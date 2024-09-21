import pygame as py
import sys

sys.path.append("..")

from standards import ASSETS_PATH

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

class Assets:
    UNO_CARDS: list[[py.Surface, ...], ...] = []
    CARD_WIDTH = 140
    CARD_HEIGHT = int(CARD_WIDTH * 1.4958677)

    CARD_TABEL = {
        "r": 0,
        "y": 1,
        "g": 2,
        "b": 3,
        
        "0": 0,
        "1": 1,
        "2": 2,
        "3": 3,
        "4": 4,
        "5": 5,
        "6": 6,
        "7": 7,
        "8": 8,
        "9": 9,
        "s": 10,
        "c": 11,
        "t": 12,

        "o": 4,
        "w": 0,
        "f": 1,
        "u": 2
    }

    @staticmethod
    def load_assets() -> None:
        IMAGE_CARD_WIDTH = 242
        IMAGE_CARD_HEIGHT = 362

        sheet = py.image.load(ASSETS_PATH + "UnoCards.png")

        for i in range(4):
            Assets.UNO_CARDS.append([])
            for j in range(13):
                card = sheet.subsurface((j * (IMAGE_CARD_WIDTH - 2), i * (IMAGE_CARD_HEIGHT - 2), IMAGE_CARD_WIDTH, IMAGE_CARD_HEIGHT))
                card = py.transform.scale(card, (Assets.CARD_WIDTH, Assets.CARD_HEIGHT))
                Assets.UNO_CARDS[i].append(card)

        Assets.UNO_CARDS.append([])

        special = [py.image.load(ASSETS_PATH + "Wish.png"), py.image.load(ASSETS_PATH + "Plus4.png"), py.image.load(ASSETS_PATH + "Back.png")]
        for card in special:
            card = py.transform.scale(card, (Assets.CARD_WIDTH, Assets.CARD_HEIGHT))
            Assets.UNO_CARDS[4].append(card)

    @staticmethod
    def card_into_image(card: str) -> py.Surface:
        if not card:
            return Assets.UNO_CARDS[4][2]
        return Assets.UNO_CARDS[Assets.CARD_TABEL[card[0]]][Assets.CARD_TABEL[card[1]]]
