import collections

class Bag:
    letters = collections.Counter(
    {
        'A':9, 
        'B':2, 
        'C':2, 
        'D':4, 
        'E':12, 
        'F':2, 
        'G':3, 
        'H':2, 
        'I':9, 
        'J':1, 
        'K':1, 
        'L':4, 
        'M':2, 
        'N':6, 
        'O':8, 
        'P':2, 
        'Q':1, 
        'R':6, 
        'S':4, 
        'T':6, 
        'U':4, 
        'V':2, 
        'W':2, 
        'X':1, 
        'Y':2, 
        'Z':1,
        '': 2,
    })

    point_values = [
    (),
    ('A', 'E', 'I', 'O', 'U', 'L', 'N', 'S', 'T', 'R'),
    ('D', 'G'),
    ('B', 'C', 'M', 'P'),
    ('F', 'H', 'V', 'W', 'Y'),
    ('K'),
    (),
    (),
    ('J', 'X'),
    (),
    ('Q', 'Z'),
]

    def choose_letter_at_random(self) -> str:
        import random
        choice = random.choices(list(self.letters.keys()), list(self.letters.values()))
        self.letters.subtract(choice)
        return choice[0]

    def get_point_value(self, letter: str) -> int:
        return [i for i in range(len(self.point_values)) if letter.upper() in self.point_values[i]][0]

