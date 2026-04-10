import unittest
from functions import text_node_to_html_node
from textnode import TextNode, TextType
from htmlnode import HTMLNode, ParentNode, LeafNode
case = [item for item in TextType]


class TestTextToHTML(unittest.TestCase):
    def test_text_to_html(self):
        check = []
        for item in case:
            with self.subTest(item=item):
            
                node = TextNode(f"text node {item}", item, "http://dummy.com")
                result = text_node_to_html_node(node)
                check.append(result)
                self.assertIsInstance(result, LeafNode)
                if item == TextType.TEXT:
                    self.assertEqual(result.tag, None)
                if item == TextType.LINK:
                    self.assertEqual(result.tag, "a")
                    self.assertEqual(result.value, node.text)
                    self.assertEqual(result.props["href"], node.url)
                    self.assertIsNotNone(node.url)
                    self.assertIsInstance(result.props, dict)
                if item == TextType.IMAGE:
                    self.assertEqual(result.tag, "img")
                    self.assertEqual(result.value, "")
                    self.assertEqual(result.props["src"], node.url)
                    self.assertEqual(result.props["alt"], node.text)
                    self.assertGreater(len(result.props), 1)

    def test_failure(self):
        with self.assertRaises(Exception):
            text_node_to_html_node("not a node")
# use with assertRaises(Exception) to check for raises

            
                
            
        
        
        
        