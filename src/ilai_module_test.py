import unittest
import ilai_module


class TestIlaiModule(unittest.TestCase):
    def test_sentence_char_count(self):
        self.assertEqual(ilai_module.sentence_char_count('sds 2j3'), 7)

    def test_sentence_word_count(self):
        self.assertEqual(ilai_module.sentence_word_count('sds 2j3'), 2)

    def test_sentence_stopwords_count(self):
        self.assertEqual(ilai_module.sentence_stopwords_count('I am not a stopword'), 4)

    def test_sentence_without_stopwords_count(self):
        self.assertEqual(ilai_module.sentence_without_stopwords_count('I am not a stopword'), 1)
