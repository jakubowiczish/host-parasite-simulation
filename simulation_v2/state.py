from abc import ABC, abstractmethod
from typing import Callable


class State(ABC):

    @abstractmethod
    def is_finished(self) -> bool:
        pass

    @abstractmethod
    def initialize(self) -> None:
        pass

    @abstractmethod
    def update(self, switch_state: Callable) -> None:
        pass

    @abstractmethod
    def draw(self) -> None:
        pass
