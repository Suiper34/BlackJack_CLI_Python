import random
from typing import Sequence

from data_models.data_models import (GameAction, GameStats, Participant,
                                     RoundOutcome)
from exceptions.invalid_input import InvalidInputError
from exceptions.user_exit import UserExit
from utils.utils import (BLACKJACK, DEALER_STAND_THRESHOLD, MINIMUM_BET,
                         draw_card, format_hand, safe_input)


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


def prompt_player_action() -> GameAction:
    """Prompt the player to hit or stand."""

    while True:
        response = safe_input('Hit or Stand? (h/s): ').strip().lower()

        if response in {'h', 'hit'}:
            return GameAction.HIT

        if response in {'s', 'stand'}:
            return GameAction.STAND

        print('Please choose \'h\' to hit or \'s\' to stand.')


def player_turn(
    player: Participant,
    deck: Sequence[int],
    random_card: random.Random
) -> None:
    """Handle the player's turn, allowing hits until they stand or bust."""

    while player.total < BLACKJACK:
        print(f'\nYour hand: {format_hand(player)} (Total: {player.total})')
        action = prompt_player_action()

        if action is GameAction.STAND:
            print('You chose to stand.')
            break

        new_card = draw_card(deck, random_card)
        player.add_card(new_card)
        print(f'You drew a {new_card}.')

        if player.total > BLACKJACK:
            print(f'Bust! Your total is {player.total}.')
            break


def dealer_turn(
    dealer: Participant,
    deck: Sequence[int],
    random_card: random.Random
) -> None:
    """Handle the dealer's turn following standard Blackjack rules."""

    print(
        f'\nDealer reveals hand: {format_hand(dealer)} (Total: {dealer.total})'
    )
    while dealer.total < DEALER_STAND_THRESHOLD:
        new_card = draw_card(deck, random_card)
        dealer.add_card(new_card)
        print(
            f'Dealer draws a {new_card}. Dealer total is now {dealer.total}.')

    if dealer.total > BLACKJACK:
        print('Dealer busts!')


def evaluate_round(player: Participant, dealer: Participant) -> RoundOutcome:
    """Determine the outcome of the round."""

    player_total = player.total
    dealer_total = dealer.total

    if player_total == BLACKJACK and len(player.hand) == 2:
        return RoundOutcome.PLAYER_BLACKJACK

    if player_total > BLACKJACK:
        return RoundOutcome.PLAYER_BUST

    if dealer_total > BLACKJACK:
        return RoundOutcome.DEALER_BUST

    if player_total > dealer_total:
        return RoundOutcome.PLAYER_WIN

    if player_total < dealer_total:
        return RoundOutcome.DEALER_WIN

    return RoundOutcome.PUSH


def apply_outcome(outcome: RoundOutcome, balance: int, wager: int) -> int:
    """Update the player's balance based on the round outcome."""

    if outcome in {RoundOutcome.PLAYER_BLACKJACK,
                   RoundOutcome.PLAYER_WIN,
                   RoundOutcome.DEALER_BUST}:
        winnings = wager if outcome != RoundOutcome.PLAYER_BLACKJACK else int(
            wager * 1.5)
        print(f'You win {winnings} credits!')
        return balance + winnings

    if outcome in {RoundOutcome.DEALER_WIN, RoundOutcome.PLAYER_BUST}:
        print(f'You lose {wager} credits.')
        return balance - wager

    print('Push! Your wager is returned.')
    return balance


def describe_outcome(
    outcome: RoundOutcome,
    player: Participant,
    dealer: Participant
) -> None:
    """Print the round scores."""

    print('\n--- Round Score ---')
    print(f'Your hand:   {format_hand(player)} (Total: {player.total})')
    print(f'Dealer hand: {format_hand(dealer)} (Total: {dealer.total})')

    messages = {
        RoundOutcome.PLAYER_BLACKJACK: 'Blackjack! 🎉',
        RoundOutcome.PLAYER_WIN: 'You beat the dealer!',
        RoundOutcome.DEALER_BUST: 'Dealer busts. You win!',
        RoundOutcome.DEALER_WIN: 'Dealer wins this round.',
        RoundOutcome.PLAYER_BUST: 'You busted!...Better luck next time',
        RoundOutcome.PUSH: 'It\'s a push.',
    }
    print(messages[outcome])


def play_round(
    balance: int,
    player: Participant,
    dealer: Participant,
    stats: GameStats,
    deck: Sequence[int],
    random_card: random.Random,
) -> int:
    """Play a single round of Blackjack and return the updated balance."""

    player.clear_hand()
    dealer.clear_hand()

    wager = prompt_wager(balance)
    print(f'\nWager accepted: {wager} credits.\n')

    # Initial deal
    for _ in range(2):
        player.add_card(draw_card(deck, random_card))
        dealer.add_card(draw_card(deck, random_card))

    print(f'Dealer shows: {format_hand(dealer, concealed_second_card=True)}')
    print(f'Your hand:    {format_hand(player)} (Total: {player.total})')

    if player.total == BLACKJACK and len(player.hand) == 2:
        print('Natural Blackjack!')

    else:
        player_turn(player, deck, random_card)
        if player.total <= BLACKJACK:
            dealer_turn(dealer, deck, random_card)

    outcome = evaluate_round(player, dealer)
    stats.record(outcome)
    describe_outcome(outcome, player, dealer)
    new_balance = apply_outcome(outcome, balance, wager)

    print(f'New balance: {new_balance} credits.\n')
    print(stats.score_board())
    print('-' * 40)

    return new_balance
