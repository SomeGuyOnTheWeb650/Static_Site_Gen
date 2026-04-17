import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

test_case = [["a", "tag and value only", None, None],
             ["b", "tag, value, and leafchildren", [HTMLNode("c", "NodeChild")], {"sometag": "blagh", "someothertag": "blagh2"}]
             ]







@unittest.skip("elsewhere atm")
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

    
        
        
    
    
    def test_leaf_node(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_node_a(self):
        node = LeafNode("a", 
                        "This is a link", 
                            {
                            "href": "http://dummy.com", 
                            "target": "boogity"
                            }
                        )
        self.assertEqual(node.to_html(), f"<a href=http://dummy.com target=boogity>This is a link</a>")
        
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")
    
    def test_to_html_with_grandchildren(self):
        
        
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_lots_of_children(self):
        child = []
        for i in range(0, 5):
            child.append(LeafNode(str(i), "child"))
        parent = ParentNode("div", child)
        self.assertIsInstance(parent.children, list)

    def test_include_props(self):
        child = LeafNode("a", "child", {"key": "value", "test": "run"})
        parent = ParentNode("tag", [child], {"inner": "peace", "rock": "roll"})
        self.assertEqual(parent.to_html(), 
                         f"<tag inner=peace rock=roll><a key=value test=run>child</a></tag>")