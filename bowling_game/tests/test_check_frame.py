import unittest
from bowling import GetFrame


class MyFrameTest(unittest.TestCase):

    def test_normal(self):
        frames = [x for x in GetFrame("Х4/34-49/1245--8/X")]
        self.assertEqual(len(frames), 10)
        self.assertEqual(frames[0], ["Х"])
        self.assertEqual(frames[1], ["4", "/"])
        self.assertEqual(frames[2], ["3", "4"])
        self.assertEqual(frames[3], ["-", "4"])
        self.assertEqual(frames[4], ["9", "/"])
        self.assertEqual(frames[5], ["1", "2"])
        self.assertEqual(frames[6], ["4", "5"])
        self.assertEqual(frames[7], ["-", "-"])
        self.assertEqual(frames[8], ["8", "/"])
        self.assertEqual(frames[9], ["X"])

    def test_symbol_in_frame(self):
        GetFrame("Хu/34-49/1245--8/X")
        self.assertRaises(ValueError)

    def test_result_frame_more10(self):
        GetFrame("Х4/84-49/1245--8/X")
        self.assertRaises(ValueError)

    def test_frame_start(self):
        GetFrame("Х4/34-49/1245--/8X")
        self.assertRaises(ValueError)

    def test_frame_end(self):
        GetFrame("Х4/3X-49/1245--8/X")
        self.assertRaises(ValueError)

    def test_len_frame_more10(self):
        GetFrame("Х4/34-49/1245--8/XX")
        self.assertRaises(IndexError)

    def test_len_frame_less10(self):
        GetFrame("Х4/34-4")
        self.assertRaises(IndexError)


if __name__ == '__main__':
    unittest.main()
