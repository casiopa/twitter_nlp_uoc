# pylint: skip-file
import unittest
from HTMLTestRunner import HTMLTestRunner
import sentiment_analyzer as sa


class TestMenu(unittest.TestCase):
    def test_stop_between_steps(self):
        self.assertEqual(sa.stop_between_steps(1, 2), 3)
        self.assertEqual(sa.stop_between_steps(3, 2), 3)


if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestMenu))
    # suite.addTest(unittest.makeSuite())
    # suite.addTest(unittest.makeSuite())
    # suite.addTest(unittest.makeSuite())
    # suite.addTest(unittest.makeSuite())
    runner = HTMLTestRunner(log=True, verbosity=2, output='reports',
                            title='PAC4_AnaBlanco',
                            description='PAC4 Ana Blanco - Sentiment Analyzer tests',
                            report_name='Sentiment Analyzer tests')
    runner.run(suite)
