import mapping
import bag
import players
import utils
import board
import unittest


# bag.py

class TestBag(unittest.TestCase):
    def test_bag_letter_sum(self):
        current_bag = bag.Bag()
        self.assertEqual(sum(current_bag.letters.values()), 100)

    def test_bag_point_values(self):
        current_bag = bag.Bag()
        self.assertEqual(current_bag.get_point_value('Z'), 10)
        self.assertEqual(current_bag.get_point_value('a'), 1)



# players.py

class TestPlayer(unittest.TestCase):

    def test_bad_letters_fail(self):
        current_bag = bag.Bag()
        player = players.Player(board.Board(current_bag), "Jacob")
        with self.assertRaises(players.WordNotInLettersError):
            _ = player.trade_in_letters('abcdefgh')
        with self.assertRaises(AssertionError):
            _ = player.draw_n_letters_from_bag(8)

# utils.py

class TestUtils(unittest.TestCase):
    def test_middle_works(self):
        with self.assertRaises(AssertionError):
            utils.fail_if_middle_not_included('hello', 1,5,0)
            utils.fail_if_middle_not_included('hello', 10,5,1)
        self.assertEqual(utils.fail_if_middle_not_included('hello', 7,7,0), None)


if __name__ == '__main__':
    unittest.main()
