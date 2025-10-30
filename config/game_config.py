from exceptions.invalid_input import InvalidInputError
from exceptions.user_exit import UserExit
from utils.utils import MINIMUM_BET, safe_input


def prompt_yes_no(prompt: str) -> bool:
    """Prompt the player for a yes/no response."""

    while True:
        response = safe_input(prompt).strip().lower()
        if response in {'y', 'yes'}:
            return True

        if response in {'n', 'no'}:
            return False

        print('Please respond with \'y\' or \'n\'.')


def prompt_wager(balance: int) -> int:
    """Prompt the player to enter a wager within the allowed range."""

    if balance < MINIMUM_BET:
        raise InvalidInputError('Insufficient balance for the minimum bet.')

    while True:
        response = safe_input(
            f'Place your wager (minimum {MINIMUM_BET}, \
                maximum {balance}) or type \'quit\' to exit: '
        ).strip().lower()

        if response in {'quit', 'q', 'exit'}:
            raise UserExit('Player chose to exit the game.')

        try:
            wager = int(response)

        except ValueError:
            print('Invalid amount...Please enter a whole number!')
            continue

        if wager < MINIMUM_BET:
            print(f'Minimum wager is {MINIMUM_BET}.')
            continue

        if wager > balance:
            print('You cannot wager more than your current balance!')
            continue

        return wager
