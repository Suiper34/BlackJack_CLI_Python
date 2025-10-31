import random

from config.game_config import play_round, prompt_yes_no
from utils.utils import CARD_VALUES, DEFAULT_BANKROLL, MINIMUM_BET
from exceptions.user_exit import UserExit
from data_models.data_models import GameStats, Participant


def main() -> None:
    """Entry point for the Blackjack CLI game."""

    rng = random.Random()
    player = Participant(name='Player')
    dealer = Participant(name='Dealer')
    stats = GameStats()
    balance = DEFAULT_BANKROLL

    print('--- Welcome to Blackjack (21) ---')
    print(f'Starting bankroll: {balance} credits.')

    try:
        while balance >= MINIMUM_BET:
            if not prompt_yes_no('\nWould you like to play a round? (y/n): '):
                print('Thanks for playing!...Come back soon.')
                break

            balance = play_round(balance, player, dealer,
                                 stats, CARD_VALUES, rng)

        if balance < MINIMUM_BET:
            print('\nInsufficient balance for the minimum bet...Game over!!!')

    except UserExit as ue:
        print(ue)

    finally:
        print('\nFinal statistics:')
        print(stats.score_board())
        print('Goodbye...')
