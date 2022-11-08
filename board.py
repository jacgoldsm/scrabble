from typing import List, Iterable
from termcolor import colored
import mapping
from bag import Bag
import utils


class LetterError(Exception):
    pass


class Tile:
    def __init__(self, letter: str = None):
        letter = letter.lower() if letter is not None else letter
        assert letter is None or letter.isalpha()
        self.letter = letter

    def __str__(self) -> str:
        letter = self.letter if self.letter is not None else "_"
        return f"|_{letter}|"


class Square:
    _possible_attributes = ["3w", "2w", "3l", "2l"]
    _attribute_dict = {
        "3w": "red",
        "2w": "magenta",
        "3l": "blue",
        "2l": "cyan",
    }

    def __init__(self, attribute: str = None):
        self.attribute = attribute

    def color(self):
        return self._attribute_dict.get(self.attribute, "white")

    def get_letter_value(self) -> int:
        if self.attribute is None:
            return 1
        return int(self.attribute[0]) if self.attribute[1] == "l" else 1

    def get_word_value(self) -> int:
        return int(self.attribute[0]) if self.attribute[1] == "w" else 1


class Board:
    squares: List[Square]
    letters: List[Tile]

    def restore_board(self, old_board) -> None:
        self.bag = old_board.bag
        self.squares = old_board.squares
        self.letters = old_board.letters

    def _generate_word(self, starting_idx: int, axis: int) -> str:
        """
        Given an index and an orientation, find the word that contains that index in that orientation.
        Example:
        0  1  2  3  4  5  ...
        H  E  L^ L  O  '' ...

        Would return HELLO
        """
        row_or_column = utils.row_or_column_range_from_index(starting_idx, axis)
        after_word_list = []
        after_range = [elem for elem in row_or_column if elem >= starting_idx]
        for i in after_range:
            if self.letters[i].letter is None:
                break
            after_word_list.append(self.letters[i].letter)

        before_word_list = []
        before_range = [elem for elem in row_or_column if elem < starting_idx]
        for i in reversed(before_range):
            if self.letters[i].letter is None:
                break
            before_word_list.append(self.letters[i].letter)
            # HE[L]LO will be stored as [E,H] and [L,L,O]
        word = "".join(list(reversed(before_word_list)) + after_word_list)
        return word

    def _add_letters_to_board(
        self, new_letters: str, new_letters_index_range: Iterable
    ) -> None:
        """
        Takes a string of new letters and a range of board indices and adds the new letters at the new indices.
        """
        if new_letters is None:
            return
        for word_idx, board_idx in zip(
            range(len(new_letters)), new_letters_index_range
        ):
            self.letters[board_idx] = Tile(new_letters[word_idx])

    def _add_words_impl(
        self,
        new_letters: str,
        new_letters_index_range: range,
        starting_idx: int,
        axis: int,
    ) -> int:
        """
        Add new letters to the board and count up the score from the principal word (in the original orientation)
        and separately, all the other words in the opposite orientation that are formed. Return the cumulative score.
        """

        self._add_letters_to_board(
            new_letters=new_letters, new_letters_index_range=new_letters_index_range
        )
        current_score = 0

        for board_i in new_letters_index_range:
            letter_above_or_left = self.letters[
                (board_i - 15) if axis == 0 else (board_i - 1)
            ].letter
            letter_below_or_right = self.letters[
                (board_i + 15) if axis == 0 else (board_i + 1)
            ].letter

            if letter_above_or_left is not None or letter_below_or_right is not None:
                word_tmp = self._generate_word(starting_idx=board_i)
                word_tmp_quadruple = (
                    word,
                    *utils.idx_to_row_column_idx(starting_idx=board_i),
                    axis,
                )
                word_tmp_range = utils.range_from_word_quadruple(*word_tmp_quadruple)

                current_score += self._add_word_impl(
                    word=word_tmp,
                    word_index_range=word_tmp_range,
                    new_letters_index_range=new_letters_index_range,
                )

        # entire word, including letters that are already on the board
        word = self._generate_word(starting_idx, axis)
        word_quadruple = word, *utils.idx_to_row_column_idx(starting_idx), axis
        word_range = utils.range_from_word_quadruple(*word_quadruple)

        current_score += self._add_word_impl(
            word=word,
            word_index_range=word_range,
            new_letters_index_range=new_letters_index_range,
        )

        return current_score

    def _add_word_impl(
        self,
        word: str,
        word_index_range: range,
        new_letters_index_range: range,
    ) -> int:

        word_score = 0
        for word_i, board_i in zip(range(len(word)), word_index_range):
            pv = (
                self.bag.get_point_value(word[word_i])
                if board_i
                in new_letters_index_range  # only apply letter multiplier if it's a new letter
                else 1
            )

            word_score += self.squares[board_i].get_letter_value() * pv
            # only apply word multiplier if some letter in word both has attribute and is a new letter
            if board_i in new_letters_index_range:
                if self.squares[board_i].attribute == "3w":
                    seen_3w_attr = True
                elif self.squares[board_i].attribute == "2w":
                    seen_2w_attr = True

        if seen_2w_attr:
            word_score *= 2
        if seen_3w_attr:
            word_score *= 3

        return word_score

    def add_word(
        self, new_letters: str, row_idx: int, col_idx: int, axis: int = 0
    ) -> int:
        """
        On success, add the word and all dependent words to the board and return the total
        score, inclusive of multiplers. On failure, do not mutate board and raise exception.
        """
        old_board = Board(self.bag, self.squares, self.letters)
        starting_idx = utils.row_column_idx_to_idx(row_idx, col_idx)
        new_letters_index_range = utils.range_from_word_quadruple(
            new_letters, row_idx, col_idx, axis
        )
        if axis not in range(2):
            raise ValueError("`axis` argument must be `0` or `1`")
        self._original_idx = starting_idx

        try:
            score = self._add_words_impl(
                new_letters, new_letters_index_range, starting_idx, axis, recursive=True
            )
        except Exception as e:
            self.restore_board(old_board)
            raise e
        return score

    def _get_default_letters(self) -> List[Tile]:
        return [Tile() for _ in range(15 * 15)]

    def _get_default_squares(self) -> List[Square]:
        squares = [Square() for _ in range(15 * 15)]
        for idx, square in enumerate(squares):
            if idx in mapping._3w_idx:
                square.attribute = "3w"
            elif idx in mapping._3l_idx:
                square.attribute = "3l"
            elif idx in mapping._2w_idx:
                square.attribute = "2w"
            elif idx in mapping._2l_idx:
                square.attribute = "2l"
        return squares

    def __init__(
        self, bag: Bag, squares: List[Square] = None, letters: List[Tile] = None
    ):
        self.bag = bag
        self.squares = squares or self._get_default_squares()
        self.letters = letters or self._get_default_letters()

    def __str__(self) -> str:
        out_list = []
        out_list.extend("__")
        out_list.extend([f" {str(i).zfill(2)} " for i in range(15)])
        for i in range(15 * 15):
            if i % 15 == 0:
                out_list.extend("\n" + str(i // 15).zfill(2))
            out_list.extend(
                colored(str(self.letters[i]), color=self.squares[i].color())
            )

        return "".join(out_list)
