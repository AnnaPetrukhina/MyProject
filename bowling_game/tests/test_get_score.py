import unittest
from bowling import GetScore, InternalGetScore


class TestInternalGetScore(unittest.TestCase):

    def setUp(self):
        result = "Х4/34-49/1245--8/X"
        self.get_score = InternalGetScore(result)

    def test_normal(self):
        self.get_score.run()
        self.assertEqual(self.get_score.score, 108)

    def test_strike(self):
        self.get_score.strike("X", number=0)
        self.assertEqual(self.get_score.score, 20)

    def test_spare(self):
        self.get_score.spare("4/", number=0)
        self.assertEqual(self.get_score.score, 15)

    def test_emptiness_start(self):
        self.get_score.emptiness("-4")
        self.assertEqual(self.get_score.score, 4)

    def test_emptiness_end(self):
        self.get_score.emptiness("4-")
        self.assertEqual(self.get_score.score, 4)

    def test_emptiness(self):
        self.get_score.emptiness("--")
        self.assertEqual(self.get_score.score, 0)

    def test_sum(self):
        self.get_score.sum_frame("34")
        self.assertEqual(self.get_score.score, 7)


class TestGetScore(unittest.TestCase):

    def setUp(self):
        result = "Х4/34-49/1245--8/X"
        self.get_score = GetScore(result)

    def test_normal(self):
        self.get_score.run()
        self.assertEqual(self.get_score.score, 97)

    def test_last_strike(self):
        self.get_score.strike("X", number=9)
        self.assertEqual(self.get_score.score, 10)

    def test_strike_last_strike(self):
        self.get_score.strike("X", number=8)
        self.get_score.frames[9] = "X"
        self.assertEqual(self.get_score.score, 20)

    def test_strike_last_spare(self):
        self.get_score.strike("X", number=8)
        self.get_score.frames[9] = "6/"
        self.assertEqual(self.get_score.score, 20)

    def test_strike_next_strike_and_numeral(self):
        self.get_score.frames[1] = ["X"]
        self.get_score.frames[2] = ["1", "4"]
        self.get_score.strike("X", number=0)
        self.assertEqual(self.get_score.score, 21)

    def test_strike_next_strike_and_emptiness(self):
        self.get_score.frames[1] = ["X"]
        self.get_score.frames[2] = ["-", "4"]
        self.get_score.strike("X", number=0)
        self.assertEqual(self.get_score.score, 20)

    def test_strike_next_emptiness(self):
        self.get_score.frames[1] = ["-", "4"]
        self.get_score.strike("X", number=0)
        self.assertEqual(self.get_score.score, 14)

    def test_strike_next_numerals(self):
        self.get_score.frames[1] = ["4", "4"]
        self.get_score.strike("X", number=0)
        self.assertEqual(self.get_score.score, 18)

    def test_spare_next_numerals(self):
        self.get_score.frames[1] = ["4", "4"]
        self.get_score.spare("4/", number=0)
        self.assertEqual(self.get_score.score, 14)

    def test_last_spare(self):
        self.get_score.spare("4/", number=9)
        self.assertEqual(self.get_score.score, 10)

    def test_spare_next_emptiness(self):
        self.get_score.frames[1] = ["-", "4"]
        self.get_score.spare("4/", number=0)
        self.assertEqual(self.get_score.score, 10)

    def test_spare_next_strike(self):
        self.get_score.frames[1] = ["X"]
        self.get_score.spare("4/", number=0)
        self.assertEqual(self.get_score.score, 20)

    def test_emptiness_start(self):
        self.get_score.emptiness("-4")
        self.assertEqual(self.get_score.score, 4)

    def test_emptiness_end(self):
        self.get_score.emptiness("4-")
        self.assertEqual(self.get_score.score, 4)

    def test_emptiness(self):
        self.get_score.emptiness("--")
        self.assertEqual(self.get_score.score, 0)

    def test_sum(self):
        self.get_score.sum_frame("34")
        self.assertEqual(self.get_score.score, 7)


if __name__ == '__main__':
    unittest.main()
