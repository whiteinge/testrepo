import unittest

class TestAllTheThings(unittest.TestCase):
    def test_foo(self):
        self.assertTrue(True)

    def test_bar(self):
        self.assertFalse(False)

    def test_baz(self):
        self.assertEqual(None, None)

if __name__ == '__main__':
    unittest.main()
