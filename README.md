# Modern Blackjack CLI

## Overview

This repository contains a modernized command-line Blackjack (21) game implemented in Python. The project emphasizes robustness, maintainability, and player experience. It incorporates type hints, dataclasses, extensive input validation, and a statistics tracker. The design is modular and extensible, enabling further experimentation such as AI-driven strategies or analytics.

## 🚀 Features

- **Authentic Blackjack Rules**: Supports Ace soft/hard totals and dealer soft-17 behavior.
- **Resilient Input Handling**: Catches invalid responses, EOF, and keyboard interrupts cleanly.
- **Type Hints & Dataclasses**: Improves readability, tooling support, and extensibility.
- **Configurable Wagers**: Validates bets against bankroll with adjustable defaults.
- **Real-time Statistics**: Tracks wins, losses, pushes, and win rate across rounds.
- **Structured Architecture**: Separates concerns for easy modification (e.g., replacing RNG, adding shoe decks, or integrating bots).

## 📦 Requirements

- Python 3.8+
- No third-party dependencies (uses only the Python standard library)

## 🛠️ Getting Started

- **Clone or Download the Repository**

    ```bash
    git clone https://github.com/your_username/BlackJack_CLI_Python.git
    cd blackjack_cli_python

- **Run the Game**

    ```bash
    python __init__.py
    


- **Follow the on-screen prompts to place wagers and choose actions:**

    1. Enter quit/q or decline the invitation to play when you wish to stop.
    Gameplay Notes
    2. Minimum Bet: `50` credits by default.
    3. Starting Bankroll:  `1,000`credits by default.
    4. Dealer Behavior: Dealer stands on all totals ≥ `17 (including soft 17)`.
    5. Player Actions: Supports hit or stand. (Splits/doubles can be added.)
    6. Exiting: Type quit during wager prompt or press `Ctrl+C`; the game exits gracefully and prints your stats.

## Architecture Overview

**Participant dataclass** *represents the player and dealer hands.*
**GameStats dataclass** *aggregates outcomes across rounds.*
A suite of helper functions handles `input validation`, `card drawing`, `scoring`, and `round orchestration`.
**main()** *loops through rounds until the player quits or runs out of funds.*

## 🙌 Customization Ideas

- **Change Deck Composition**: *modify `CARD_VALUES` or implement multi-deck shoes.*
- **Add Rule Variants**: *splits, doubles, insurance, or surrender options.*
- **Player/Dealer**: *replace `prompt_player_action` with strategy algorithms.*
- **Logging/Analytics**: *pipe `GameStats` into external dashboards or files.*

## 🛠️ Troubleshooting

**Insufficient Balance**: reduce your bet or restart the game to reset your bankroll.
**Unexpected Termination**: ensure Python 3.8+ is installed. Interrupts `(Ctrl+C)` intentionally exit the game.
**Unit Testing**: The modular structure makes it straightforward to unit-test individual helper functions.

## 📄 License

This project is released under the MIT License. See [`LICENSE`][def] for details.

Enjoy refining and extending your Blackjack experience!

[def]: ./LICENSE
