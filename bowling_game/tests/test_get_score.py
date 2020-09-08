import unittest
from bowling import GetScore


class MyFrameTest(unittest.TestCase):

    def setUp(self):
        result = "Х4/34-49/1245--8/X"
        self.get_score = GetScore(result)

    def test_normal(self):
        self.get_score.run()
        self.assertEqual(self.get_score.score, 108)

    def test_strike(self):
        self.get_score.strike("X")
        self.assertEqual(self.get_score.score, 20)

    def test_spare(self):
        self.get_score.spare("4/")
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


if __name__ == '__main__':
    unittest.main()
