# POKER PROJECT

<div align="center">
<img width = 75% src = "img/R.jpeg">
</div>

## About project

This repositorie is dedicated to 1DAW 3rd trimester project. We are going to simulate a game of Texas Hold'em poker between two players, the program will determine the best hand for each player (5 common cards and 2 self cards) and then will give a winner.

## Modules

We will work with this modules structure:

```
├── test_poker.py
├── helpers.py
├── game.py
│   └── Game
├── cards.py
│   ├── Card
│   └── Hand
└── roles.py
    └── Player
```

- Game.py: To make the test work, this module will act like a main.py. It will be a funciton on this module in charge of calling other modules and give the winning hand and player. In case of tie, it will return None and the hand of one player.
- Cards.py: It will be the module that is going to solve the game. There will be a class (Card) to define all the cards (objects) and a class (Hand) to evaluate the hads and give a rating to the hands.
- Player: Will be the class to save the player's name and the best hand of all the possible combinations.
- Helpers.py: This module has been given by the teacher to make easier some parts of the project.

### Implementation requirements

- You must be able to construct a `Player` object by just giving the player's name. **Example**: `Player('Player 1'), Player('Player 2')`
- You must be able to construct a `Card` object from a text string. **Example**: `Card('Q♠'), Card('7♣'), Card('A♠')`
- The `Hand` object must contain a `cat` attribute that identifies the category of the hand as well as a `cat_rank` attribute that stores the "ranking" of its category. In most cases this is the highest card, but not always. **Example**:

| `hand.cat`             | `hand.cat_rank` | Explicación                                                    |
| ---------------------- | --------------- | -------------------------------------------------------------- |
| `Hand.HIGH_CARD`       | `'J'`           | High card of the hand                                          |
| `Hand.ONE_PAIR`        | `'5'`           | High card of the hand                                          |
| `Hand.TWO_PAIR`        | `('10', '7')`   | Sorted tuple with the two values (major to minor)              |
| `Hand.THREE_OF_A_KIND` | `'K'`           | High card of the hand                                          |
| `Hand.STRAIGTH`        | `'9'`           | High card of the hand                                          |
| `Hand.FLUSH`           | `'Q'`           | High card of the hand                                          |
| `Hand.FULL_HOUSE`      | `('3', 'J')`    | Tuple with three of a kind and two pair values (in thar order) |
| `Hand.FOUR_OF_A_KIND`  | `'Q'`           | High card of the hand                                          |
| `Hand.STRAIGHT_FLUSH`  | `'7'`           | High card of the hand                                          |

## References

- [Anatomy of a poker card](https://bit.ly/45KP9jp)
- [List of possible winning hands](https://en.wikipedia.org/wiki/List_of_poker_hands)
- [Online Winning Hand Calculator](https://www.pokerlistings.com/which-hand-wins-calculator)
- [Teacher's repo](https://github.com/sdelquin/pro/tree/main/ut4/te2)
- [Project Partner](https://github.com/ElPayo)
