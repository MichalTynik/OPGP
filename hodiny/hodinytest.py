import unittest
import hodiny

class Test(unittest.TestCase):
    
    def test_13_00(self):
        c = hodiny.Cas(13,00)
        self.assertEqual(c.str(), "13:00")
        
if __name__ == "__main__":
    unittest.main()
    