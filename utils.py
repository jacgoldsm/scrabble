import itertools


def fail_if_middle_not_included(word: str, row_idx: int, col_idx: int, axis: int) -> None:
    MIDDLE_IDX = row_column_idx_to_idx(7,7)
    word_range = range_from_word_quadruple(word, row_idx, col_idx, axis)
    assert MIDDLE_IDX in word_range

def letter_in_original_row_or_column(board_i: int, original_idx: int, axis: int) -> bool:
    original_axis_row_or_column = row_or_column_range_from_index(original_idx, axis)
    return board_i in original_axis_row_or_column

def row_or_column_range_from_index(idx: int, axis: int) -> range:
    row_idx, col_idx = idx_to_row_column_idx(idx)
    if axis == 0:
        return range(idx - col_idx, idx - col_idx + 15)
    else:
        return range(idx - (15*row_idx), idx - (15*row_idx) + 15*14, 15)

def range_from_word_quadruple(word: str, row_idx: int, col_idx: int, axis:int) -> range:
    idx = row_column_idx_to_idx(row_idx, col_idx)
    row_or_column = row_or_column_range_from_index(idx, axis)
    return itertools.islice((elem for elem in row_or_column if elem >= idx), len(word))


def row_column_idx_to_idx(row_idx: int, col_idx: int) -> int:
    return row_idx * 15 + col_idx

def idx_to_row_column_idx(idx: int) -> int:
    return (idx // 15, idx % 15)