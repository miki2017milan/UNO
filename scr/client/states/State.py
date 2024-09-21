from __future__ import annotations

from abc import ABC, abstractmethod

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    import pygame as py
    from Main import Main

class State(ABC):
    current_state: State
    states = {"End": None}

    def __init__(self, main: Main):
        self.main = main

    @staticmethod
    def add_state(state_name: str, state: State) -> None:
        State.states[state_name] = state

    @staticmethod
    def switch_state(state_name: str) -> None:
        State.current_state = State.states[state_name]

    @staticmethod
    def get_state() -> State:
        return State.current_state

    @abstractmethod
    def tick(self) -> None:
        pass

    @abstractmethod
    def render(self, win: py.Surface) -> None:
        pass