import sys
import players
import board
import utils
from bag import Bag



def main():
    player_list = []
    bag = Bag()
    current_board = board.Board(bag)

    args_list = sys.argv[1:]

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

            if response == '__QUIT__':
                break
            print("""
            Enter 'row,column,orientation' to play the word. Orientation is 0 for across, 1 for down.
            row and column is the index of the leftmost/uppermost index.
            """)

            idx_triple = input().split(',')

            if idx_triple == '__QUIT__': break
            flag = True
            while flag:
                try:
                    if turn_one:
                        utils.fail_if_middle_not_included(letters, *idx_triple)
                    current_board = player.try_to_play_word(
                        current_board, response.lower(), *idx_triple
                        )
                    flag = False
                except Exception:
                    print("Invalid Word, try again")
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