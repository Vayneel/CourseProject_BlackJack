"""
BlackJack module with classes of cards and deck
"""

from consts import CARD_SUITS, CARD_VALUES
from itertools import product
from random import shuffle


class Card:
    """
    Card class in BlackJack
    """
    def __init__(self, suit: str, picture: str, value: int) -> None:
        """
        Init method of Card class
        :param suit: suit of card
        :param picture: picture (name) of card
        :param value: value of card
        """
        self.suit = suit
        self.picture = picture
        self.value = value

    def __repr__(self) -> str:
        """
        Repr method of Card class
        :return: card suit and picture in one string
        """
        return f'{self.suit} {self.picture}'


class Deck:
    """
    Deck class in BlackJack
    """
    def __init__(self) -> None:
        """
        Init method of Deck class
        """
        self.deck_cards = []
        self.create_shuffled_deck()

    def create_shuffled_deck(self) -> list[Card]:
        """
        Creating deck with 4 sets of cards and shuffling it
        :return: list of Card class objects
        """
        for suit, picture in product(CARD_SUITS, CARD_VALUES):
            if picture == 'Ace':
                card = Card(suit, picture, 11)
            elif picture in ('Jack', 'Queen', 'King'):
                card = Card(suit, picture, 10)
            elif picture in ('2', '3', '4', '5', '6', '7', '8', '9', '10'):
                card = Card(suit, picture, int(picture))
            else:
                continue

            # this part is for creating 4 sets of cards (not only 1 set, but 4)
            # usually in BlackJack players use 4 sets of cards
            for _ in range(4):
                self.deck_cards.append(card)

        # shuffling deck
        shuffle(self.deck_cards)

        return self.deck_cards

    def take_card_from_deck(self) -> Card:
        """
        Take top (last) card from deck (list of Card class objects)
        :return: top (last) card
        """
        return self.deck_cards.pop()


# creating deck
current_deck = Deck()
