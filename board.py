from typing import List
from termcolor import colored
import mapping
from bag import Bag
import utils
import copy

class LetterError(Exception):
    pass

class Tile:
    def __init__(self, letter: str = None):
        letter = letter.lower() if letter is not None else letter
        assert letter is None or letter.isalpha()
        self.letter = letter

    def __str__(self) -> str:
        letter = self.letter if self.letter is not None else '_'
        return f'|_{letter}|'


class Square:
    _possible_attributes = ['3w', '2w', '3l', '2l']
    _attribute_dict = {
        '3w':'red',
        '2w':'magenta',
        '3l':'blue',
        '2l':'cyan',
    }

    def __init__(self, attribute: str = None):
        assert attribute in self._possible_attributes or attribute is None
        self.attribute = attribute

    def color(self):
        return self._attribute_dict.get(self.attribute, 'white')

    def get_letter_value(self) -> int:
        return int(self.attribute[0]) if self.attribute[1] == 'l' else 1

    def get_word_value(self) -> int:
        return int(self.attribute[0]) if self.attribute[1] == 'w' else 1


class Board:
    squares: List[Square]
    tiles: List[Tile]

    def restore_board(self, old_board) -> None:
        self.tiles = old_board.tiles


    def _generate_word(self, starting_idx: int, axis: int) -> str:
        row_or_column = utils.row_or_column_range_from_index(starting_idx, axis)
        after_word_list = []
        after_range = (elem for elem in row_or_column if elem >= starting_idx)
        for i in after_range:
            if self.letters[i] is None:
                break
            after_word_list.append(self.tiles[i])

        before_word_list = []
        before_range = (elem for elem in row_or_column if elem < starting_idx)
        for i in reversed(before_range):
            if self.letters[i] is None:
                break
            before_word_list.append(self.tiles[i])
            # HE[L]LO will be stored as [E,H] and [L,L,O]
            word = "".join(reversed(before_word_list) + after_word_list)
            return word

        
    def _add_word_impl(self, word: str, starting_idx: int, axis: int, recursive: bool) -> int:
        """
        Add a word laid out horizontally. If this word is the original word played,
        check each column for vertical words and call `add_word_vertical` if needed.
        Otherwise, don't do that. Return the score from the original word and any child
        vertical words from the recursive call. Only check for '* word scores' or '* letter scores' for the
        original word.
        """
        _score = 0
        if word is None:
            word = self._generate_word(starting_idx, axis)
            
        _seen_3w_attr, _seen_2w_attr = False, False
        word_quadruple = word,utils.idx_to_row_column_idx(starting_idx),axis
        word_range = utils.range_from_word_quadruple(*word_quadruple)
        for word_i, board_i in zip(range(len(word)), word_range):
                current_letter = self.letters[board_i]
                assert current_letter is None
                pv = (
                    self.bag.get_point_value(word[word_i])
                    if utils.letter_in_original_row_or_column(board_i, self._original_idx, axis)
                    else 1
                )
                value = self.squares[board_i].get_letter_value() * pv
                if self.squares[board_i].attribute == '3w':
                    _seen_3w_attr = True
                elif self.squares[board_i].attribute == '2w':
                    _seen_2w_attr = True
                _score += value
                self.letters[board_i] = word[word_i]
                letter_above_or_left = self.tiles[board_i - 15] if axis == 0 else board_i - 1
                letter_below_or_right = self.tiles[board_i + 15] if axis == 0 else board_i + 1
                if recursive:
                    if letter_above_or_left is not None or letter_below_or_right is not None:
                        _score += self._add_word_impl(
                        word=None, 
                        starting_idx=board_i, 
                        axis = 1 if axis == 0 else 0,
                        recursive=False
                        )

        if utils.letter_in_original_row_or_column(board_i, self._original_idx, axis):
            if _seen_2w_attr:
                _score *= 2
            elif _seen_3w_attr:
                _score *= 3

        return _score



    def add_word(self, word: str, row_idx: int, col_idx: int, axis: int=0) -> int:
        """
        On success, add the word and all dependent words to the board and return the total
        score, inclusive of multiplers. On failure, do not mutate board and raise exception.
        """
        old_board = copy.deepcopy(self)
        starting_idx = row_idx * 15 + col_idx
        assert axis in [0,1]
        self._original_idx = starting_idx

        try:
            self._add_word_impl(word, starting_idx, axis, recursive=True)
        except Exception as e:
            self.restore_board(old_board)
            raise e
        

                

    def _get_default_letters(self) -> List[Tile]:
        return [Tile() for _ in range(15*15)]

    def _get_default_squares(self) -> List[Square]:
        squares = [Square() for _ in range(15*15)]
        for idx, square in enumerate(squares):
            if idx in mapping._3w_idx:
                square.attribute = '3w'
            elif idx in mapping._3l_idx:
                square.attribute = '3l'
            elif idx in mapping._2w_idx:
                square.attribute = '2w'
            elif idx in mapping._2l_idx:
                square.attribute = '2l'
        return squares

    def __init__(self, bag, squares: List[Square] = None, letters: List[Tile] = None):
        self.bag = bag
        self.squares = squares or self._get_default_squares()
        self.letters = letters or self._get_default_letters()

    def __str__(self) -> str:
        out_list = []
        out_list.extend('__')
        out_list.extend([f" {str(i).zfill(2)} " for i in range(15)])
        for i  in range(15*15):
            print(f"{i=}")
            if i % 15 == 0:
                out_list.extend('\n' + str(i // 15).zfill(2))
            out_list.extend(colored(str(self.letters[i]), color=self.squares[i].color()))

        return ''.join(out_list)
