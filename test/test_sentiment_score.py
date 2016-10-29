import unittest
import sentiment_score


class TestBase(unittest.TestCase):

    def setUp(self):
        pass

    def test_get_sentiment(self):
        text = "Twitter reviews are awesome"
        senti, score = sentiment_score.get_sentiment(text)
        self.assertEquals(senti, 'pos')
        self.assertIsNotNone(score)

    def test_find_product(self):
        
