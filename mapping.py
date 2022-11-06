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
               i not in range(15*5, 15*9)
               or i == 15 * 6 + 7
               )

    ]

_3l_idx = [
               i 
               for i in range(15*15)
               if i % 8 == 0
               and i not in _3w_idx
               and i not in _2w_idx
    ]

_2l_idx = [
            i
            for i in range(15*15)
            if i % 3 == 0
            and i not in _3l_idx
            and i not in _2w_idx
            and i not in _3w_idx
    ]