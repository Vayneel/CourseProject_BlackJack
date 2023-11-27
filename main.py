"""
BlackJack main module, in which you can start your game
"""

import game
from colorama import Fore


def start(n: int) -> None:
    """
    Play BlackJack n times
    :param n: Number of rounds to play
    :return: Nothing
    """
    if n > 0:
        while 1:
            match input(Fore.MAGENTA + 'Want to play?(y/n): '):
                case 'y':
                    game.Game().play()
                    start(n - 1)
                    break
                case 'n':
                    break
                case _:
                    print(Fore.RED + 'Try again.' + Fore.WHITE)
    else:
        print(Fore.MAGENTA + '\nIf you want to play more, restart me')


if __name__ == '__main__':
    # to set higher number without getting errors, u should add more bot-names (in consts.py module)
    start(5)
