import unittest
import gal_module

class TestGalModule(unittest.TestCase):

    def test_connect_by_synonyms(self):
        self.assertEqual(gal_module.connect_by_synonyms("small", "little"),  1 )
        self.assertEqual(gal_module.connect_by_synonyms("huge kid", "heavy child"),  2 )
