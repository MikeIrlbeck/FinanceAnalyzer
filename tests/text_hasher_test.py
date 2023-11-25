import unittest
import src.text_hasher as txtHash

class testSuite(unittest.TestCase):

    def setUp(self):
        pass

    def testHashingWords(self):
        s1 = "string"
        s2 = "stringg"
        
        myHash = txtHash.Hasher()

        self.assertEqual(1, myHash.hash(s1, s2))

        