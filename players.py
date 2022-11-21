from board import Board
import utils

class Player:
    def __init__(self, board, name):
        self.board = board
        self.name = name
        self.score = 0
        self.letters = []
        self.draw_n_letters_from_bag(7)

    def draw_n_letters_from_bag(self, n: int) -> None:
        assert n < 8
        n = (
            sum(self.board.bag.letters.values())
            if n >= sum(self.board.bag.letters.values())
            else n
        )
        letters = [self.board.bag.choose_letter_at_random() for _ in range(n)]
        self.letters.extend(letters)

    def trade_in_letters(self, letters: str) -> None:
        utils.fail_if_invalid_letters(self.letters, letters)
        self.letters = [letter for letter in self.letters if letter not in letters]
        self.draw_n_letters_from_bag(len(letters))


    def try_to_play_word(
        self, current_board: Board, word: str, row_idx: int, col_idx: int, axis: int = 0
    ) -> None:
        _self_letters = self.letters
        self.score += current_board.add_word(_self_letters, word, row_idx, col_idx, axis)
        for letter in word.upper():
            # the only case where `letter` won't be in `self.letters` is if it's a blank tile
            self.letters.remove(letter if letter in self.letters else '')
        self.draw_n_letters_from_bag(len(word))
