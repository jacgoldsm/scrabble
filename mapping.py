import utils

_3w_idx = [
               1*15-1   , 8*15-1   , 15*15-1,
               1*15-1-7 ,            15*15-1-7,
               1*15-1-14, 8*15-1-14, 15*15-1-14
               ]

_2w_idx = [
               i 
               for i in range(15*15)
               if 
               (
               i % 16 == 0
               or i % 14 == 0
               )
               and
               (
               utils.idx_to_row_column_idx(i)[0] not in range(5,10) # row not in [5,9) except for center square
               or i == 112
               )

    ]

_3l_idx_rowcols_1h = [
            (1,5),
            (1,14-5),
            (5,1),
            (5,14-1),
            (5,5),
            (5,14-5),
    ]

_3l_idx_rowcols_2h = [
    (14 - i, j) for i, j in _3l_idx_rowcols_1h
]

_3l_idx_rowcols = _3l_idx_rowcols_1h + _3l_idx_rowcols_2h

_3l_idx = [utils.row_column_idx_to_idx(*i) for i in _3l_idx_rowcols]


_2l_idx_rowcols_1h = [
        (0,3),
        (0,14-3),
        (2,6),
        (2,14-6),
        (3,0),
        (3,14-0),
        (3,7),
    #   (3,14-7),
        (6,2),
        (6,14-2),
        (6,6),
        (6,14-6)
    ]

_2l_idx_rowcols_2h = [
    (14 - i, j) for i, j in _2l_idx_rowcols_1h
]

_2l_idx_rowcols = _2l_idx_rowcols_1h + _2l_idx_rowcols_2h

_2l_idx = [utils.row_column_idx_to_idx(*i) for i in _2l_idx_rowcols]