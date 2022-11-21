import sys
import players
import board
import utils
from bag import Bag
import dictionary
import traceback


def main():
    player_list = []
    bag = Bag()
    current_board = board.Board(bag)

    args_list = sys.argv[1:]
    
    if not args_list:
        raise ValueError("Must be at least one player")

    for name in args_list:
        player_list.append(players.Player(current_board, name))

    print("Welcome to SCRABBLE!. Enter '__QUIT__' to quit at any time.")


    
    
    turn_one = True
    while sum(bag.letters.values()) > 0:
        for player in player_list:
            print("RED = triple word score, MAGENTA = double word score BLUE = ",
                  "triple letter score, CYAN = double letter score")
            print(current_board)
            print(f"Player {player.name}: Enter a word ('__pass__' to pass, '__letters__' to trade in letters)")
            print(f"Your letters are {player.letters}")
            response = input()

            incorrect_word_flag = True
            while incorrect_word_flag:
                if not dictionary.is_valid_word(response):
                    print("Not a valid word")
                else:
                    incorrect_word_flag = False

            if response == '__pass__':
                continue
            elif response == '__letters__':
                print("Enter the letters you would like to exchange.")
                letters = input()
                flag = True
                while flag:
                    try:
                        player.trade_in_letters(letters)
                        flag = False
                    except Exception:
                        print("Invalid letters.")
                        letters = input()
                    continue
            elif response == '__QUIT__':
                break


            print("""
            Enter 'row,column,orientation' to play the word. Orientation is 0 for across, 1 for down.
            row and column is the index of the leftmost/uppermost index.
            """)

            idx_triple = input().split(',')
            idx_triple = [int(i) for i in idx_triple]

            if idx_triple == '__QUIT__': 
                break

            flag = True
            while flag:
                try:
                    if turn_one:
                        utils.fail_if_middle_not_included(response, *idx_triple)
                    player.try_to_play_word(
                        current_board, response.lower(), *idx_triple
                        )
                    flag = False
                except Exception as e:
                    print(traceback.format_exc())
                    print(e)
                    response = input()

            print(current_board)
            turn_one = False

            
    players_sorted = sorted(player_list, key = lambda p: p.score, reverse=True)

    print(f"GAME OVER! Player {players_sorted[0].name} Wins! Scores:")

    for player in players_sorted:
        print(f"Player {player.name}: {player.score} points")

    print("Play Again? (Y/N)")
    resp = input()
    if resp.lower() == 'y':
        main()
    else:
        sys.exit(0)


if __name__ == '__main__':
    main()