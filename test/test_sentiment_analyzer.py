# pylint: skip-file
import unittest
import pandas as pd
from HTMLTestRunner import HTMLTestRunner
import sentiment_analyzer as sa
import inspect


class TestMenu(unittest.TestCase):
    def test_file_exists(self):
        current_filename = inspect.getfile(inspect.currentframe())
        self.assertTrue(sa.file_exists(current_filename))

    def test_stop_between_steps(self):
        self.assertEqual(sa.stop_between_steps(1, 2), 3)
        self.assertEqual(sa.stop_between_steps(3, 2), 3)


class TestUtils(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls._text_in = "If you’d like to give back, please pull request at https://github.com/rstudio-education/hopr"
        cls._text_out1 = "if youd like to give back please pull request at"
        cls._text_out2 = "youd like give back please pull request"
        cls._dicts_raw = [{"sentiment": 0,
                          "text": "@switchfoot http://twitpic.com/2y1zl - Awww, that's a bummer. You shoulda got David Carr of Third Day to do it. ;D"},
                          {"sentiment": 4,
                           "text": "If you can, please support us on a monthly basis from just €2"}]
        cls._dicts_cleaned = [{"sentiment": 0,
                               "text": "switchfoot awww thats bummer shoulda got david carr third day d"},
                              {"sentiment": 4,
                               "text": "please support us monthly basis 2"}]
        cls._bows = [{"switchfoot": 1, "awww": 1, "thats": 1, "bummer": 1, "shoulda": 1, "got": 1,
                      "david": 1, "carr": 1, "third": 1, "day": 1, "d": 1},
                     {"please": 1, "support": 1, "us": 1, "monthly": 1, "basis": 1, "2": 1}]
        cls._vocab = ["switchfoot", "awww", "thats", "bummer", "shoulda", "got", "david", "carr",
                      "third", "day", "d", "please", "support", "us", "monthly", "basis", "2"]
        cls._df_joined = pd.DataFrame.from_dict(
            [{"sentiment": 0, "text": "switchfoot awww thats bummer shoulda got david carr third day d",
              "bow": {"switchfoot": 1, "awww": 1, "thats": 1, "bummer": 1, "shoulda": 1, "got": 1,
                     "david": 1, "carr": 1, "third": 1, "day": 1, "d": 1}},
                {"sentiment": 4, "text": "please support us monthly basis 2",
             "bow": {"please": 1, "support": 1, "us": 1, "monthly": 1, "basis": 1, "2": 1}}]
             )

    def test_preprocess_text(self):
        self.assertEqual(sa.preprocess_text(self._text_in), self._text_out1)

    def test_remove_stop_words(self):
        self.assertEqual(sa.remove_stopwords(self._text_out1), self._text_out2)

    def test_preprocess_data(self):
        self.assertEqual(sa.preprocess_data(self._dicts_raw), self._dicts_cleaned)

    def test_create_bows_vocab(self):
        bows, vocab = sa.create_bows_vocab(self._dicts_cleaned)
        self.assertEqual(set(vocab), set(self._vocab))
        self.assertEqual(bows, self._bows)

    def test_join_dicts_bows(self):
        df_joined = sa.join_dicts_bows(self._dicts_cleaned, self._bows)
        self.assertTrue(df_joined.equals(self._df_joined))

    def test_create_cluster_bow(self):
        self.assertTrue(sa.create_cluster_bow(self._df_joined, 0).equals(pd.Series(self._bows[0])))
        self.assertTrue(sa.create_cluster_bow(self._df_joined, 4).equals(pd.Series(self._bows[1])))


if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestMenu))
    suite.addTest(unittest.makeSuite(TestUtils))
    runner = HTMLTestRunner(log=True, verbosity=2, output='reports',
                            title='PAC4_AnaBlanco',
                            description='PAC4 Ana Blanco - Sentiment Analyzer tests',
                            report_name='Sentiment Analyzer tests')
    runner.run(suite)
