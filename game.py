"""
BlackJack module with all game algorythm
"""

import players
from random import randint
from colorama import Fore


class Game:
    """
    Game class in BlackJack
    """

    def __init__(self) -> None:
        """
        Init method of Game class
        """
        self.list_of_players = []

    def _create_players(self) -> None:
        """
        Create list of Player class objects
        :return: Nothing
        """
        while 1:
            try:
                amount_of_bots = int(input(Fore.YELLOW + '\nEnter amount of bots (up to 4): ' + Fore.WHITE))
                if 4 >= amount_of_bots >= 0:
                    break
                else:
                    print(Fore.RED + 'Incorrect value. Try again.')
            except ValueError:
                print(Fore.RED + 'Try again.')

        for _ in range(amount_of_bots):
            self.list_of_players.append(players.Bot())

        self.list_of_players.insert(randint(0, amount_of_bots), players.Player())
        self.list_of_players.append(players.Dealer())

    def _hand_out_cards(self) -> None:
        """
        Hand out cards to each player and check for BlackJack
        :return: Nothing
        """
        print(Fore.MAGENTA + '\nDealer hands out cards' + Fore.WHITE)
        for player in self.list_of_players:
            player.take_card()
            player.take_card()
            print(player.show_first_cards())
            player.blackjack = True if player.check_points() == 21 else False

        if self.list_of_players[-1].my_cards[0].picture == 'Ace':
            players.AbstractPlayer.enable_insurance = True
        if self.list_of_players[-1].blackjack:
            players.AbstractPlayer.ins_work = True

    def _player_choice(self) -> None:
        """
        Making choice for each player and checking for split
        :return: Nothing
        """
        do_if_split = False
        card_of_second_hand = None

        for player in self.list_of_players:
            if not isinstance(player, players.Dealer):

                if not do_if_split:
                    player.make_choice()
                    if player.split:
                        if isinstance(player, players.Player):
                            self.list_of_players.insert(self.list_of_players.index(player) + 1,
                                                        players.Player(f'{player.name}\'s right hand'))
                        else:
                            self.list_of_players.insert(self.list_of_players.index(player) + 1,
                                                        players.Bot(f'{player.name}\'s right hand'))
                        player.name = f'{player.name}\'s left hand'
                        card_of_second_hand = player.my_cards.pop()
                        player.take_card()
                        do_if_split = True
                        player.enough_split = True
                        player.blackjack = True if player.check_points() == 21 else False
                        player.make_choice()
                else:
                    player.my_cards.append(card_of_second_hand)
                    player.take_card()
                    do_if_split = False
                    player.enough_split = True
                    player.blackjack = True if player.check_points() == 21 else False
                    player.make_choice()
            else:
                player.make_choice()

    def _left_game_check(self) -> None:
        """
        Few-time check of players, which left game
        :return: Nothing
        """
        stop = 1

        while stop != 0:
            stop = 0
            for player in self.list_of_players[:-1]:
                if player.left_game:
                    self.list_of_players.remove(player)
                    stop += 1

    def _show_cards(self) -> None:
        """
        Print all players cards and show if player's insurance bet was paid
        :return: Nothing
        """
        print(self.list_of_players[-1].show_cards())  # show cards of Dealer

        for player in self.list_of_players[:-1]:
            if isinstance(player, players.Player):
                if player.got_ins:
                    print(Fore.LIGHTMAGENTA_EX + f'+{3 * player.ins_bet}$ (insurance) - {player.name}'
                          + Fore.WHITE)
            print(player.show_cards())

    def _results(self) -> None:
        """
        Show who lose, won or drew
        :return: Nothing
        """
        for player in self.list_of_players:
            if not isinstance(player, players.Dealer):
                if player.check_points() > self.list_of_players[-1].check_points() or self.list_of_players[-1].busted:
                    print(f'Player {player.name} won.')
                    if isinstance(player, players.Player):
                        if player.blackjack:
                            player.bet *= 1.5
                        print(player.win())

                elif player.check_points() == self.list_of_players[-1].check_points():
                    print(f'Player {player.name} drew with the {self.list_of_players[-1].name}.')
                    if isinstance(player, players.Player):
                        print(player.draw())
                else:
                    print(f'Player {player.name} loses.')
            else:
                players.Dealer.my_cards.clear()  # Dealer drops cards

    def play(self) -> None:
        """
        Game algorythm
        :return: Nothing
        """
        self._create_players()
        self._hand_out_cards()
        self._player_choice()
        self._left_game_check()
        self._show_cards()
        self._results()
