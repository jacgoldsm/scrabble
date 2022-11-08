from board import Board
import copy


class WordNotInLettersError(Exception):
    pass


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
        self._fail_if_invalid_letters(letters)
        self.letters = [letter for letter in self.letters if letter not in letters]
        self.draw_n_letters_from_bag(len(letters))

    def _fail_if_invalid_letters(self, word: str) -> None:
        _self_letters = copy.copy(self.letters)
        for letter in word.upper():
            if letter not in _self_letters:
                if "" in _self_letters:
                    _letter = ""
                else:
                    raise WordNotInLettersError("Cannot form word with current letters")
            else:
                _letter = letter
                _self_letters.remove(_letter)

    def try_to_play_word(
        self, current_board: Board, word: str, row_idx: int, col_idx: int, axis: int = 0
    ) -> None:
        self._fail_if_invalid_letters(word)
        self.score += current_board.add_word(word, row_idx, col_idx, axis)
        for letter in word.upper():
            self.letters.remove(letter)
