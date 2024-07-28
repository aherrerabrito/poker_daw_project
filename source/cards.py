from __future__ import annotations


class Card:
    CLUBS = "♣"
    DIAMONDS = "◆"
    HEARTS = "❤"
    SPADES = "♠"
    SUITS = [CLUBS, DIAMONDS, HEARTS, SPADES]
    GLYPH = {
        CLUBS: "🃑🃒🃓🃔🃕🃖🃗🃘🃙🃚🃛🃝🃞",
        DIAMONDS: "🃁🃂🃃🃄🃅🃆🃇🃈🃉🃊🃋🃍🃎",
        HEARTS: "🂱🂲🂳🂴🂵🂶🂷🂸🂹🂺🂻🂽🂾",
        SPADES: "🂡🂢🂣🂤🂥🂦🂧🂨🂩🂪🂫🂭🂮",
    }
    SYMBOLS = ("A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K")
    A_VALUE = 1
    K_VALUE = 13

    def __init__(self, card_representation: str):
        self.suit = card_representation[-1]
        self.str_value = card_representation[:-1]
        self.value = Card.SYMBOLS.index(self.str_value) + 1

    @classmethod
    def get_symbol(cls, card_num):
        return Card.SYMBOLS[card_num - 1] if card_num != 14 else "A"

    @classmethod
    def get_value(cls, card_symbol):
        return (
            Card.SYMBOLS.index(card_symbol) + 1
            if card_symbol != "A"
            else Card.A_VALUE + Card.K_VALUE
        )

    @property
    def cmp_value(self):
        return Card.A_VALUE + Card.K_VALUE if self.value == Card.A_VALUE else self.value

    def __eq__(self, other):
        if isinstance(other, Card):
            return self.value == other.value and self.suit == other.suit
        return False

    def __gt__(self, other: Card):
        return self.cmp_value > other.cmp_value

    def __lt__(self, other: Card):
        return self.cmp_value < other.cmp_value

    def __str__(self):
        return Card.GLYPH[self.suit][self.value - 1]

    def __repr__(self) -> str:
        return f"{self.str_value}{self.suit}"


class Hand:
    HIGH_CARD = 1
    ONE_PAIR = 2
    TWO_PAIR = 3
    THREE_OF_A_KIND = 4
    STRAIGHT = 5
    FLUSH = 6
    FULL_HOUSE = 7
    FOUR_OF_A_KIND = 8
    STRAIGHT_FLUSH = 9
    LOWER_STAIR = [5, 4, 3, 2, 1]

    def __init__(self, cards: tuple):
        self.cards = cards
        self.pattern_values = {
            item: self.values.count(item) for item in set(self.values)
        }
        self.ranking = {
            "escalera_de_color": Hand.STRAIGHT_FLUSH,
            (4, 1): Hand.FOUR_OF_A_KIND,
            (3, 2): Hand.FULL_HOUSE,
            "color": Hand.FLUSH,
            "stair": Hand.STRAIGHT,
            (3, 1, 1): Hand.THREE_OF_A_KIND,
            (2, 2, 1): Hand.TWO_PAIR,
            (2, 1, 1, 1): Hand.ONE_PAIR,
            (1, 1, 1, 1, 1): Hand.HIGH_CARD,
        }

    @property
    def values(self) -> list:
        self.total_sum = sorted(list(i.value for i in self.cards), reverse=True)
        if self.total_sum == Hand.LOWER_STAIR:
            return self.total_sum
        return sorted(i.cmp_value for i in self.cards)

    @property
    def hand_values(self):
        """
        This function returns the numerical values of the cards involved in the move,
        followed by the remaining excess cards.
        Example of the output:
        [2,2,9,5,3] -> A pair with the leftover cards sorted.
        """
        other_values = []
        hand_values = []
        for key, value in self.pattern_values.items():
            if value != 1:
                hand_values.extend([key] * value)
            else:
                other_values.append(key)
        hand_values.sort(reverse=True)
        other_values.sort(reverse=True)
        hand_values.extend(other_values)
        return hand_values

    def same_suits(self) -> bool:
        return self.cards[0].suit * 5 == "".join(i.suit for i in self.cards)

    @property
    def is_stair(self) -> tuple:
        if self.same_suits() and self.consecutive:
            return True, "escalera_de_color"
        if self.consecutive:
            return True, "stair"
        return False, None

    @property
    def consecutive(self) -> bool:
        fcard = self.values[0]
        for card in self.values[1:]:
            if (card - 1) != fcard:
                return False
            fcard = card
        return True

    @property
    def cat(self) -> int:
        """
        Returns a number taken from a dictionary, whose fields are
        key: The *pattern of the hand
        value: The class attribute corresponding to the score of that hand.
        * By the pattern of a hand we mean the counts of each type of digit that may be in the hand.
        type of digit that may be in the hand.
        Example:
        Hand -> [A♣,2♣,3♣,4♣,5♣]
        Pattern -> (1,1,1,1,1,1,1) -> Straight.
        Example 2:
        Hand -> [A♣,2♣,2❤,3♣,4♣]
        Pattern -> (2,1,1,1,1) -> Pair.
        """
        is_stair, hand_value = self.is_stair
        if is_stair:
            return self.ranking[hand_value]
        if self.same_suits() and not self.consecutive:
            return self.ranking["color"]
        ranking = tuple(sorted(self.pattern_values.values(), reverse=True))
        return self.ranking[ranking]

    @property
    def cat_rank(self) -> str | tuple:
        """
        This function returns the best/best cards according to the obtained hand.
        In case of a double pair the highest pair is returned first:
            Hand -> [K❤, K◆, 3♣, 3❤, 5♣]
            Result -> (K, 3)
        In case of full house the value of the three of a kind and then pair is returned:
            Hand -> [Q❤, Q♠, Q◆, 4♣, 4◆]
            Result -> (Q, 4)
        In the remaining hands the highest card is returned.
        """
        if len(self.pattern_values) == len(self.values):
            return Card.get_symbol(max(self.pattern_values.keys()))
        better_card_values = []
        for key, value in self.pattern_values.items():
            if value in self.pattern_values.values() and value != 1:
                better_card_values.append(Card.get_symbol(key))
        if self.cat == Hand.TWO_PAIR:
            item1, item2 = better_card_values
            if Card.get_value(item1) > Card.get_value(item2):
                return item1, item2
            return item2, item1
        if self.cat == self.FULL_HOUSE:
            items = []
            for item, value in self.pattern_values.items():
                if value == 3:
                    items.insert(0, Card.get_symbol(item))
                elif value == 2:
                    items.append(Card.get_symbol(item))
            return tuple(items)
        return "".join(better_card_values)

    def __repr__(self) -> str:
        return f"{self.cards}"

    def __contains__(self, other: Card) -> bool:
        return other in self.cards

    def __gt__(self, other: Hand) -> bool:
        """
        Check which hand is higher between two possible hands.
        First check the category of the hand to rule out a lower category hand.
        that it is of a lower rank, then look at each of the cards involved in the play.
        involved in the play
        """
        if self.cat > other.cat:
            return True
        if self.cat < other.cat:
            return False
        for card_num1, card_num2 in zip(self.hand_values, other.hand_values):
            if card_num1 > card_num2:
                return True
            if card_num1 < card_num2:
                return False
        return False
