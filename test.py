import mapping
import bag
import players
import utils
import board
import unittest
import dictionary


# bag.py


class TestBag(unittest.TestCase):
    def test_bag_letter_sum(self):
        current_bag = bag.Bag()
        self.assertEqual(sum(current_bag.letters.values()), 100)

    def test_bag_point_values(self):
        current_bag = bag.Bag()
        self.assertEqual(current_bag.get_point_value("Z"), 10)
        self.assertEqual(current_bag.get_point_value("a"), 1)


# players.py


class TestPlayer(unittest.TestCase):
    def test_bad_letters_fail(self):
        current_bag = bag.Bag()
        player = players.Player(board.Board(current_bag), "Jacob")
        with self.assertRaises(players.WordNotInLettersError):
            player.trade_in_letters("abcdefgh")
        with self.assertRaises(AssertionError):
            player.draw_n_letters_from_bag(8)


# utils.py


class TestUtils(unittest.TestCase):
    def test_middle_works(self):
        with self.assertRaises(AssertionError):
            utils.fail_if_middle_not_included("hello", 1, 5, 0)
            utils.fail_if_middle_not_included("hello", 10, 5, 1)
        self.assertEqual(utils.fail_if_middle_not_included("hello", 7, 7, 0), None)

    def test_letter_in_original_works(self):
        self.assertTrue(utils.letter_in_original_row_or_column(20, 25, 0))
        self.assertTrue(utils.letter_in_original_row_or_column(20, 50, 1))
        self.assertFalse(utils.letter_in_original_row_or_column(20, 25, 1))
        self.assertFalse(utils.letter_in_original_row_or_column(20, 50, 0))

    def test_range_from_word_quadruple_works(self):
        self.assertEqual(
            list(utils.range_from_word_quadruple("hello", 3, 4, 0)), list(range(49, 54))
        )
        self.assertEqual(
            list(utils.range_from_word_quadruple("hello", 3, 4, 1)),
            list(range(49, 124, 15)),
        )

    def test_row_column_idx_to_idx(self):
        self.assertEqual(utils.row_column_idx_to_idx(0, 0), 0)
        self.assertEqual(utils.row_column_idx_to_idx(12, 3), 183)

    def test_idx_to_row_column_idx(self):
        self.assertEqual(utils.idx_to_row_column_idx(0), (0, 0))
        self.assertEqual(utils.idx_to_row_column_idx(183), (12, 3))

    def test_row_or_column_range_from_index(self):
        self.assertEqual(
            list(utils.row_or_column_range_from_index(6, 0)), list(range(0, 15))
        )
        self.assertEqual(
            list(utils.row_or_column_range_from_index(6, 1)), list(range(6, 216, 15))
        )

    def test_dictionary_works(self):
        self.assertTrue(dictionary.is_valid_word("pea"))
        self.assertTrue(dictionary.is_valid_word("pEa"))
        self.assertTrue(dictionary.is_valid_word("anonymous"))
        self.assertFalse(dictionary.is_valid_word("kdlfjalkdfii"))


if __name__ == "__main__":
    unittest.main()
