import unittest
from textnode import TextNode, TextType

@unittest.skip("elsewhere atm")
class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_dif(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_none(self):
        node = TextNode("This is a text node", TextType.LINK,)
        self.assertIsNone(node.url)
        
    def test_notNone(self):
        node = TextNode("This is a text node", TextType.TEXT, "http://dummy.com")
        self.assertIsNotNone(node.url)

    def test_doesnt_exist(self):
        with self.assertRaises(KeyError):
            _ = TextType["GRAPHIC"]


if __name__ == "__main__":
    unittest.main()
