import unittest
from extraction_function import extract_title

class TestExtractFunction(unittest.TestCase):

    def test_extract_title_functional(self):
        result = extract_title("# Hello")
        
        self.assertEqual(result, "Hello")

    def test_extract_title_not_functional(self):
        with self.assertRaises(Exception):

            result = extract_title("### Hello")

    def test_extract_title_functional_space(self):
        result = extract_title("# Hello   ")
        
        self.assertEqual(result, "Hello")
        