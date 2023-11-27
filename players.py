"""
BlackJack module with classes of players
"""

from abc import ABC, abstractmethod
from deck import current_deck
from random import randint
from consts import BOT_NAMES
from colorama import Fore


class MembersOfBlackJack(ABC):
    """
    Abstract class for all types of players (Player, Bot, Dealer) in BlackJack
    """
    name = ''
    my_cards = []
    blackjack = False

    def __repr__(self) -> str:
        """
        Represent method of all players in BlackJack
        :return: string with name of player
        """
        return self.name

    def check_points(self) -> int:
        """
        Method of all players in BlackJack to count player's card points
        :return: sum of card points of player
        """
        points = 0
        for card in self.my_cards:
            points += card.value
        return points

    def get_card_values(self) -> list[int]:
        """
        Method of all players in BlackJack to make list of player's card points
        :return: list with values of player's cards
        """
        card_values = []
        for card in self.my_cards:
            card_values.append(card.value)
        return card_values

    def bust_check(self) -> bool:
        """
        Method of all players in BlackJack to check player for bust. If you have more than 21 point and
        have Ace, method will replace it value with 1
        :return: True or False (Are you busted or no)
        """
        cv = self.get_card_values()
        if self.check_points() > 21:
            if 11 not in cv:
                print(f'{self.name} have too much points ({self.check_points()}p.) - ' +
                      Fore.RED + 'busted' + Fore.WHITE)
                return True
            else:
                self.my_cards[cv.index(11)].value = 1
                return self.bust_check()
        else:
            return False

    def show_cards(self) -> str:
        """
        Method of all players in BlackJack to show player's cards in string
        :return: str with cards of player
        """
        string_with_cards = f'\n{self.name}\'s cards:\n'
        for card in self.my_cards:
            string_with_cards += card.__repr__() + '\n'
        return string_with_cards

    def take_card(self) -> None:
        """
        Method of all players in BlackJack to append list of player's cards with top card of deck
        :return: Nothing
        """
        self.my_cards.append(current_deck.take_card_from_deck())

    @abstractmethod
    def show_first_cards(self):
        pass

    @abstractmethod
    def make_choice(self):
        pass


class AbstractPlayer(MembersOfBlackJack):
    """
    Abstract class for Player and Bot players in BlackJack
    """
    enable_insurance = False
    left_game = False
    split = False
    enough_split = False

    def show_first_cards(self) -> str:
        """
        Method of Player and Bot players in BlackJack to show player's first cards
        :return: Player's cards
        """
        return f'\n{self.name} has these cards:\n{self.my_cards[0]}, {self.my_cards[1]}'

    def exit_game(self) -> str:
        """
        Method of Player and Bot players in BlackJack to set left_game to True
        :return: Player {player's name} left the session
        """
        self.left_game = True
        return f'Player {self.name} left the session.'

    @abstractmethod
    def card_take_cycle(self):
        pass


# ------------------------------------------------------------------------------------------------ #

class Player(AbstractPlayer):
    """
    Player class in BlackJack
    """
    bet = 0
    ins_bet = 0
    ins_work = False
    got_ins = False

    def __init__(self, name=input('Enter your name: ')) -> None:
        """
        Init method of Player class
        :param name: name of player
        """
        self.name = Fore.YELLOW + name + Fore.WHITE
        self.make_bet('bet')
        self.my_cards = []

    def make_bet(self, mode: str) -> None:
        """
        Method of Player in BlackJack to set player's bet
        :return: Nothing
        """
        while 1:
            try:
                bet = int(input('Enter your bet (50, 100, 200): '))
                if bet in (50, 100, 200):
                    break
                else:
                    print('Incorrect bet. Try again.\n')
            except ValueError:
                print('Try again.\n')

        print(Fore.LIGHTMAGENTA_EX + f'-{bet}$' + Fore.WHITE)
        if mode == 'bet':
            self.bet = bet
        elif mode == 'ins':
            self.ins_bet = bet

    def insurance(self) -> None:
        """
        Method of Player in BlackJack to make insurance
        :return: Nothing
        """
        if self.ins_work:
            self.got_ins = True

    def double(self) -> None:
        """
        Method of Player in BlackJack to double player's bet and take 1 card
        :return: Nothing
        """
        print(Fore.LIGHTMAGENTA_EX + f'-{self.bet}$ (double)' + Fore.WHITE)
        self.bet *= 2
        self.take_card()

    def surrender(self) -> None:
        """
        Method of Player in BlackJack to surrender and got pay-back (half of player's bet)
        :return: Nothing
        """
        print(self.name + Fore.RED + ' surrendered' + Fore.WHITE)
        print(Fore.LIGHTMAGENTA_EX + f'+{self.bet / 2}$ (surrender)' + Fore.WHITE)
        print(self.exit_game())

    def get_reward_instantly(self) -> None:
        """
        Method of Player in BlackJack to instantly win if player has blackjack
        :return: Nothing
        """
        print(Fore.LIGHTMAGENTA_EX + f'+{2 * self.bet}$' + Fore.WHITE)
        print(self.exit_game())

    def card_take_cycle(self) -> None:
        """
        Method of Player in BlackJack to take cards or stop doing it
        :return: Nothing
        """
        while 1:
            match input(Fore.MAGENTA + '\nWhat should I do now?' + Fore.WHITE +
                        '\n\t1.Hit (take card)\n\t2.Stand (stop)\n(Enter number of action)> '):
                case '1':
                    if self.check_points() < 21:
                        self.take_card()
                        print(Fore.LIGHTBLUE_EX + 'Your card -  ' + self.my_cards[-1].__repr__()
                              + Fore.WHITE)
                        print(self.show_cards())
                        if self.bust_check():
                            print(self.exit_game())
                            break
                    else:
                        print(Fore.RED + 'You have too much points to take more cards.' + Fore.WHITE)
                        break
                case '2':
                    break
                case _:
                    print(Fore.RED + '\nYou entered wrong value. Try again.' + Fore.WHITE)

    def make_choice(self) -> None:
        """
        Method of Player in BlackJack to make choice what player will do
        :return: Nothing
        """
        while 1:
            match input(Fore.MAGENTA + '\nWhat should I do? ' + Fore.WHITE + f'(Make choice as {self.name})' +
                        Fore.WHITE + '\n\t1.Take card (Hit)\n\t2.Stand\n\t3.Surrender\n\t4.Double' +
                        '\n\t5.Split hand\n\t6.Make insurance\n\t' +
                        '7.Get reward instantly (If BlackJack)\n\t8.Check my cards\n(Enter number of action)> '):

                case '1':
                    if not self.blackjack:
                        self.card_take_cycle()
                        break
                    else:
                        print(Fore.RED + '\nYou can\'t do this action.' + Fore.WHITE)
                    break
                case '2':
                    break
                case '3':
                    self.surrender()
                    break
                case '4':
                    self.double()
                    print(Fore.LIGHTBLUE_EX + 'Your card -  ' + self.my_cards[-1].__repr__()
                          + Fore.WHITE)
                    if self.bust_check():
                        print(self.exit_game())
                    break
                case '5':
                    if self.my_cards[0].value == self.my_cards[1].value and not self.enough_split:
                        self.split = True
                        print(self.name + Fore.MAGENTA + ' split his hand' + Fore.WHITE)
                        break
                    else:
                        print(Fore.RED + '\nYou can\'t do this action.' + Fore.WHITE)
                case '6':
                    if self.enable_insurance:
                        self.make_bet('ins')
                        self.insurance()
                        self.enable_insurance = False
                        print(self.name + Fore.MAGENTA + ' insured' + Fore.WHITE)
                        self.make_choice()
                        break

                    else:
                        print(Fore.RED + '\nYou can\'t do this action.' + Fore.WHITE)
                case '7':
                    if self.blackjack:
                        self.get_reward_instantly()
                        break
                    else:
                        print(Fore.RED + '\nYou can\'t do this action.' + Fore.WHITE)
                case '8':
                    print(self.show_cards())
                case _:
                    print(Fore.RED + '\nYou entered wrong value. Try again.' + Fore.WHITE)

    def win(self) -> str:
        """
        Method of Player in BlackJack to print player's gain if player won
        :return: String with gain in $
        """
        return Fore.LIGHTMAGENTA_EX + f'+{2 * self.bet}$' + Fore.WHITE

    def draw(self) -> str:
        """
        Method of Player in BlackJack to print player's gain if player drew with Dealer
        :return: String with gain in $
        """
        return Fore.LIGHTMAGENTA_EX + f'+{self.bet}$' + Fore.WHITE


# ------------------------------------------------------------------------------------------------ #

class Bot(AbstractPlayer):
    """
    Bot class in BlackJack
    """
    def __init__(self, name: str = '') -> None:
        """
        Init method of Bot class
        :param name: Name of Bot
        """
        self.max_value = randint(18, 20)
        self.surrender_value = (range(14, 18))
        self.my_cards = []
        if not name == '':
            self.name = name
        else:
            self.name = Fore.GREEN + BOT_NAMES.pop(BOT_NAMES.index(BOT_NAMES[randint(0, len(BOT_NAMES) - 1)])) \
                        + Fore.WHITE

    def card_take_cycle(self) -> None:
        """
        Method of Bot in BlackJack to take cards
        :return: Nothing
        """
        while self.check_points() < self.max_value:
            self.take_card()
            print(self.name + Fore.LIGHTGREEN_EX + ' took card -  ' + self.my_cards[-1].__repr__() + Fore.WHITE)
            if self.bust_check():
                print(self.exit_game())

    def make_choice(self) -> None:
        """
        Method of Bot in BlackJack to make random choice what bot will do
        :return: Nothing
        """
        while 1:
            match randint(1, 5):
                case 1:
                    self.card_take_cycle()
                    break
                case 2:
                    if self.check_points() >= self.max_value:
                        break
                case 3:
                    if self.check_points() in self.surrender_value:
                        print(self.name + Fore.RED + ' surrendered' + Fore.WHITE)
                        print(self.exit_game())
                        break
                case 4:
                    if self.my_cards[0].value == self.my_cards[1].value and not self.enough_split:
                        self.split = True
                        print(self.name + Fore.MAGENTA + ' split his hand' + Fore.WHITE)
                        break
                case 5:
                    if self.enable_insurance:
                        self.enable_insurance = False
                        print(self.name + Fore.MAGENTA + ' insured' + Fore.WHITE)
                        self.make_choice()
                        break


# ------------------------------------------------------------------------------------------------ #

class Dealer(MembersOfBlackJack):
    """
    Dealer class in BlackJack
    """
    def __init__(self) -> None:
        """
        Init method of Dealer class
        """
        self.name = Fore.RED + 'Dealer' + Fore.WHITE
        self.busted = False

    def show_first_cards(self) -> str:
        """
        Method of Dealer in BlackJack to show Dealer's first cards
        :return: Dealer's card and some secret card
        """
        return f'\n{self.name} has these cards:\n{self.my_cards[0]}, ##### (second card will be revealed later)\n'

    def make_choice(self) -> None:
        """
        Method of Dealer in BlackJack to make Dealer take cards while he won't get more than 16 points
        :return: Nothing
        """
        while self.check_points() < 17:
            self.take_card()
            print(self.name + Fore.LIGHTRED_EX + ' took card -  ' + self.my_cards[-1].__repr__() + Fore.WHITE)
            self.busted = self.bust_check()

# ------------------------------------------------------------------------------------------------ #
