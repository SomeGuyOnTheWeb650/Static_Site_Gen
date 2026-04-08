import unittest
from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_eq_tag(self):
        node = HTMLNode("a",
                         "This is text, inside a p, could be anything",
                         None, {"href": "http://www.dummy.com",
                                "target": "boogity"}
                        )
        
        
        self.assertEqual(node.tag, "a")
    
    def test_props_to_html(self):
        node = HTMLNode("a",
                        "Value Text",
                        None,
                        {"key": "dummy",
                         "key2": "dummy2"}
                         )
        check = f" key=dummy key2=dummy2"
        self.assertEqual(node.props_to_html(), check)

    def test_value(self):
        node = HTMLNode(None, "Something")
        self.assertEqual(node.value, "Something")