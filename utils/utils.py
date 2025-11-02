import random
from typing import TYPE_CHECKING, Callable, Sequence

from exceptions.user_exit import UserExit

if TYPE_CHECKING:
    from data_models.data_models import Participant

CARD_VALUES: Sequence[int] = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10)
BLACKJACK: int = 21
DEALER_STAND_THRESHOLD: int = 17
MINIMUM_BET: int = 50
DEFAULT_BANKROLL: int = 1_000


def safe_input(prompt: str, input_fn: Callable[[str], str] = input) -> str:
    """
    Wrapper for input() that handles EOF and keyboard interrupts gracefully.
    """

    try:
        return input_fn(prompt)

    except EOFError as eof:
        raise UserExit('EOF received. Exiting game.') from eof

    except KeyboardInterrupt as ki:
        raise UserExit('\nGame interrupted by player.') from ki


def draw_card(deck: Sequence[int], random_card: random.Random) -> int:
    """Draw a random card from the deck."""
    return random_card.choice(deck)


def best_total(hand: Sequence[int]) -> int:
    """
    Calculates the best Blackjack total for a hand.
    Aces (1) can count as 11 if it doesn't cause a bust.
    """

    total = sum(11 if card == 1 else card for card in hand)
    aces = hand.count(1)

    while total > BLACKJACK and aces:
        total -= 10
        aces -= 1

    return total


def format_hand(
    participant: 'Participant',
    concealed_second_card: bool = False
) -> str:

    """Return a printable representation of a participant's hand."""

    if concealed_second_card and participant.hand:
        return f'[{participant.hand[0]}, ?]'

    return '[' + ', '.join(str(card) for card in participant.hand) + ']'
