import unittest
import sentiment_analyzer


class TestBase(unittest.TestCase):

    def setUp(self):
        self.test_tweet = "Who made you an @ATT fan? Share with #MadeMeAFanContest for a chance to win. Rules https://t.co/hU3I3wFn5V https://t.co/seJBJK"

    def test_get_sentiment_textblob(self):
        senti, score = sentiment_analyzer.get_sentiment_textblob(self.test_tweet)
        self.assertEquals(senti, 'neg')
        self.assertIsNotNone(score)

    def test_get_sentiment_vivekn(self):
        senti, score = sentiment_analyzer.get_sentiment_vivekn(self.test_tweet)
        self.assertEquals(senti, 'Positive')
        self.assertIsNotNone(score)

    def test_find_product_general(self):
        product = sentiment_analyzer.find_product(self.test_tweet)
        self.assertEquals("general", product)

    def test_find_product_specific(self):
        test_sample = self.test_tweet + " uverse"
        product = sentiment_analyzer.find_product(test_sample)
        self.assertEquals("uverse", product)

    def test_find_service_general(self):
        service = sentiment_analyzer.find_service(self.test_tweet)
        self.assertEquals("general", service)

    def test_find_service_specific(self):
        test_sample = self.test_tweet + " technician"
        service = sentiment_analyzer.find_service(test_sample)
        self.assertEquals("technician dispatch", service)

    def test_preprocess_text(self):
        cleaned_text = sentiment_analyzer.preprocess_text(self.test_tweet)
        self.assertIsNotNone(cleaned_text)
        self.assertTrue("att" in cleaned_text)
        self.assertTrue("mademeafancontest" in cleaned_text)
