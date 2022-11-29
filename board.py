from typing import List, Tuple
from termcolor import colored
import mapping
from bag import Bag
import utils
import dictionary


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


class Squares:
    data: List[Square]

    def __getitem__(self, tuple_or_idx):
        if isinstance(tuple_or_idx, int):
            return self.data[tuple_or_idx]
        row, col = tuple_or_idx
        return self.data[row * 15 + col]

    def get(self, tuple_or_idx, default):
        try:
            return self.__getitem__(tuple_or_idx)
        except Exception:
            return default

    def __init__(self):
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
        self.data = squares


class Tiles:
    data: List[Tile]

    def __getitem__(self, tuple_or_idx):
        if isinstance(tuple_or_idx, int):
            return self.data[tuple_or_idx]
        row, col = tuple_or_idx
        return self.data[row * 15 + col]

    def get(self, tuple_or_idx, default):
        try:
            return self.__getitem__(tuple_or_idx)
        except Exception:
            return default

    def __setitem__(self, tuple_or_idx, new):
        if isinstance(tuple_or_idx, int):
            self.data[tuple_or_idx] = new
        row, col = tuple_or_idx
        self.data[row * 15 + col] = new

    def __init__(self):
        self.data = [Tile() for _ in range(15 * 15)]


class Board:
    squares: Squares
    letters: Tiles

    def restore_board(self, old_board) -> None:
        self.bag = old_board.bag
        self.squares = old_board.squares
        self.letters = old_board.letters

    def _generate_word(self, row_idx: int, col_idx: int, axis: int) -> str:
        """
        Given an index and an orientation, find the word that contains that index in that orientation.
        Example:
        0  1  2  3  4  5  ...
        H  E  L^ L  O  '' ...

        Would return HELLO
        """
        starting_idx = utils.row_column_idx_to_idx(row_idx, col_idx)
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
        if not dictionary.is_valid_word(word) and word is not None and word != '':
            print(word)
            raise Exception(f"Move resulted in invalid word: {word}")
        return word

    def _add_letters_to_board(
        self,
        new_letters: str,
        new_letters_starting_row: int,
        new_letters_starting_col: int,
        axis: int,
    ) -> None:
        """
        Takes a string of new letters and a range of board indices and adds the new letters at the new indices.
        """
        if new_letters is None:
            return
        if axis == 0:
            for idx in range(len(new_letters)):
                self.letters[
                    new_letters_starting_row, new_letters_starting_col + idx
                ] = Tile(new_letters[idx])
        else:
            for idx in range(len(new_letters)):
                self.letters[
                    new_letters_starting_row + idx, new_letters_starting_col
                ] = Tile(new_letters[idx])

    def _add_words_impl(
        self,
        new_letters,
        new_letters_starting_row,
        new_letters_starting_col,
        row_idx,
        col_idx,
        axis,
    ) -> int:
        """
        Add new letters to the board and count up the score from the principal word (in the original orientation)
        and separately, all the other words in the opposite orientation that are formed. Return the cumulative score.
        """

        self._add_letters_to_board(
            new_letters=new_letters,
            new_letters_starting_row=new_letters_starting_row,
            new_letters_starting_col=new_letters_starting_col,
            axis=axis,
        )

        if axis == 0:
            new_letters_index_tuples = [
                (new_letters_starting_row, new_letters_starting_col + i)
                for i in range(len(new_letters))
            ]
        else:
            new_letters_index_tuples = [
                (new_letters_starting_row + i, new_letters_starting_col)
                for i in range(len(new_letters))
            ]

        current_score = 0
        for idx in range(len(new_letters)):
            if axis == 0:
                letter_above_or_left, letter_below_or_right = (
                    self.letters.get(
                        (new_letters_starting_row - 1, new_letters_starting_col + idx),
                        None,
                    ),
                    self.letters.get(
                        (new_letters_starting_row + 1, new_letters_starting_col + idx),
                        None,
                    ),
                )
            else:
                letter_above_or_left, letter_below_or_right = (
                    self.letters.get(
                        (new_letters_starting_row + idx, new_letters_starting_col - 1),
                        None,
                    ),
                    self.letters.get(
                        (new_letters_starting_row + idx, new_letters_starting_col + 1),
                        None,
                    ),
                )

            starting_row = new_letters_starting_row if axis == 0 else idx
            starting_col = new_letters_starting_col if axis == 1 else idx

            if letter_above_or_left is not None or letter_below_or_right is not None:
                word_tmp = self._generate_word(
                    row_idx=starting_row, col_idx=starting_col, axis=axis
                )

                current_score += self._add_word_impl(
                    word=word_tmp,
                    row_idx=row_idx,
                    col_idx=col_idx,
                    new_letters_index_tuples=new_letters_index_tuples,
                    axis=axis,
                )

        # entire word, including letters that are already on the board
        word = self._generate_word(row_idx, col_idx, axis)
        current_score += self._add_word_impl(
            word=word,
            row_idx=row_idx,
            col_idx=col_idx,
            new_letters_index_tuples=new_letters_index_tuples,
            axis=axis,
        )

        return current_score

    def _add_word_impl(
        self,
        word: str,
        row_idx: int,
        col_idx: int,
        new_letters_index_tuples: List[Tuple[int]],
        axis: int,
    ) -> int:

        if axis == 0:
            total_letters_index_tuples = [
                (row_idx, col_idx + i) for i in range(len(word))
            ]
        else:
            total_letters_index_tuples = [
                (row_idx + i, col_idx) for i in range(len(word))
            ]

        seen_2w_attr, seen_3w_attr = False, False

        word_score = 0
        for (row, col), letter in zip(total_letters_index_tuples, word):
            pv = (
                self.bag.get_point_value(letter)
                if (row, col)
                in new_letters_index_tuples  # only apply letter multiplier if it's a new letter
                else 1
            )

            word_score += self.squares[row, col].get_letter_value() * pv
            # only apply word multiplier if some letter in word both has attribute and is a new letter
            if (row, col) in new_letters_index_tuples:
                if self.squares[row, col].attribute == "3w":
                    seen_3w_attr = True
                elif self.squares[row, col].attribute == "2w":
                    seen_2w_attr = True

        if seen_2w_attr:
            word_score *= 2
        if seen_3w_attr:
            word_score *= 3

        return word_score

    def add_word(
        self,
        player_letters: str,
        new_word: str,
        row_idx: int,
        col_idx: int,
        axis: int = 0,
    ) -> int:
        """
        On success, add the word and all dependent words to the board and return the total
        score, inclusive of multiplers. On failure, do not mutate board and raise exception.
        """
        old_board = Board(self.bag, self.squares, self.letters)

        if axis == 0:
            new_letters = [
                letter
                for i, letter in enumerate(new_word)
                if self.letters[row_idx, col_idx + i].letter is None
            ]
            new_letters_starting_row = row_idx
            new_letters_starting_col = col_idx + (len(new_word) - len(new_letters))
        elif axis == 1:
            new_letters = [
                letter
                for i, letter in enumerate(new_word)
                if self.letters[row_idx + i, col_idx].letter is None
            ]
            new_letters_starting_row = row_idx + (len(new_word) - len(new_letters))
            new_letters_starting_col = col_idx
        else:
            raise ValueError("`axis` argument must be `0` or `1`")

        new_letters = "".join(new_letters)
        utils.fail_if_invalid_letters(player_letters, new_letters)

        try:
            score = self._add_words_impl(
                new_letters,
                new_letters_starting_row,
                new_letters_starting_col,
                row_idx,
                col_idx,
                axis,
            )
        except Exception as e:
            self.restore_board(old_board)
            raise e
        return score, new_letters

    def __init__(self, bag: Bag, squares: Squares = None, letters: Tiles = None):
        self.bag = bag
        self.squares = squares or Squares()
        self.letters = letters or Tiles()

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
