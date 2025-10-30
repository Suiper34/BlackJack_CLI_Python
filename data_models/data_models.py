from dataclasses import dataclass, field
from enum import Enum, auto
from typing import List

from utils.utils import best_total


class GameAction(Enum):
    HIT = auto()
    STAND = auto()


class RoundOutcome(Enum):
    PLAYER_BLACKJACK = auto()
    PLAYER_WIN = auto()
    DEALER_WIN = auto()
    PUSH = auto()
    PLAYER_BUST = auto()
    DEALER_BUST = auto()


@dataclass
class Participant:
    name: str
    hand: List[int] = field(default_factory=list)

    @property
    def total(self) -> int:
        return best_total(self.hand)

    def add_card(self, card: int) -> None:
        self.hand.append(card)

    def clear_hand(self) -> None:
        self.hand.clear()


@dataclass
class GameStats:
    rounds_played: int = 0
    wins: int = 0
    losses: int = 0
    pushes: int = 0

    def record(self, outcome: RoundOutcome) -> None:
        self.rounds_played += 1
        if outcome in {RoundOutcome.PLAYER_BLACKJACK,
                       RoundOutcome.PLAYER_WIN,
                       RoundOutcome.DEALER_BUST}:
            self.wins += 1

        elif outcome in {RoundOutcome.DEALER_WIN, RoundOutcome.PLAYER_BUST}:
            self.losses += 1

        else:
            self.pushes += 1

    def score_board(self) -> str:
        if self.rounds_played == 0:
            return 'No rounds played yet!'

        return (
            f'Rounds: {self.rounds_played} | '
            f'Wins: {self.wins} | '
            f'Losses: {self.losses} | '
            f'Pushes: {self.pushes} | '
            f'Win Rate: {self.wins / self.rounds_played:.1%}'
        )
