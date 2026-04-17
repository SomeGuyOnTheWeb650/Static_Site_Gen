import unittest
from inline_markdown import text_node_to_html_node, split_nodes_delimiter, extract_markdown_images
from inline_markdown import text_to_textnodes, extract_markdown_links, split_nodes_image, split_nodes_link

from textnode import TextNode, TextType
from htmlnode import HTMLNode, ParentNode, LeafNode
case = [item for item in TextType]

@unittest.skip("elsewhere atm")
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

@unittest.skip("elsewwhere atm")
class TestSplitNodesDelimiter(unittest.TestCase):
    def test_split_nodes_delimiter(self):
        old_nodes = [TextNode("this is plain text, no mods needed has a url, shouldn't do anything", TextType.TEXT, "https:dummy.com"),
                    TextNode("this is a node, with a `code block` word", TextType.TEXT),
                    TextNode("this is a node, it has a **bold section of text** blagh", TextType.TEXT),
                    TextNode("this is a node, it has an _italic section of text_ blagh", TextType.TEXT)
                    ]
        delimiter_text_type = [("", TextType.TEXT), ("`", TextType.CODE), ("**", TextType.BOLD), ("_", TextType.ITALIC)]
        result = []
        result.extend(split_nodes_delimiter(old_nodes, delimiter_text_type[0][0], delimiter_text_type[0][1]))
        self.assertEqual("this is plain text, no mods needed has a url, shouldn't do anything", result[0].text)
        
    def test_split_nodes_code(self):
        old_nodes = [TextNode("this is a node, with a `code block` word", TextType.TEXT)]
        result = split_nodes_delimiter(old_nodes, "`", TextType.CODE)
        self.assertEqual((result[0].text, result[0].text_type), ("this is a node, with a ", TextType.TEXT))
        self.assertEqual((result[1].text, result[1].text_type), ("code block", TextType.CODE))
        self.assertEqual((result[2].text, result[2].text_type), (" word", TextType.TEXT))
        
    def test_split_nodes_bold(self):
        old_nodes = [TextNode("this is a node, with a **bolded word** word", TextType.TEXT)]
        result = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
        self.assertEqual((result[0].text, result[0].text_type), ("this is a node, with a ", TextType.TEXT))
        self.assertEqual((result[1].text, result[1].text_type), ("bolded word", TextType.BOLD))
        self.assertEqual((result[2].text, result[2].text_type), (" word", TextType.TEXT))
        
         
    def test_split_nodes_italics(self):
        old_nodes = [TextNode("this is a node, with a _italic block_ word", TextType.TEXT)]
        result = split_nodes_delimiter(old_nodes, "_", TextType.ITALIC)
        self.assertEqual((result[0].text, result[0].text_type), ("this is a node, with a ", TextType.TEXT))
        self.assertEqual((result[1].text, result[1].text_type), ("italic block", TextType.ITALIC))
        self.assertEqual((result[2].text, result[2].text_type), (" word", TextType.TEXT))

    def test_split_nodes_edge_case(self):
        old_nodes = [TextNode("this is a node, with a `code block`", TextType.TEXT)]
        result = split_nodes_delimiter(old_nodes, "`", TextType.CODE)
        self.assertEqual((result[0].text, result[0].text_type), ("this is a node, with a ", TextType.TEXT))
        self.assertEqual((result[1].text, result[1].text_type), ("code block", TextType.CODE))
        
    def test_syntax_error(self):
        old_nodes = [TextNode("this is a node, with a **code block", TextType.TEXT)]
        
        with self.assertRaises(SyntaxError):
            split_nodes_delimiter(old_nodes, "**", TextType.BOLD)

    def test_multiple_splits(self):
        old_nodes = [TextNode("**this is a bold** sentence **multiple splits**", TextType.TEXT)]
        result = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
        self.assertEqual((result[0].text, result[0].text_type), ("this is a bold", TextType.BOLD))
        self.assertEqual((result[1].text, result[1].text_type), (" sentence ", TextType.TEXT))
        self.assertEqual((result[2].text, result[2].text_type), ("multiple splits", TextType.BOLD))
    
    
    def test_skippable(self):
        old_nodes = [TextNode("already bold", TextType.BOLD)]
        result = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
        self.assertIs(old_nodes[0], result[0])
            
class TestExtractImage(unittest.TestCase):  
    def test_extract_image(self):
        text = "hello darkness ![my old friend](http://iwillseeyou.com)"
        result = extract_markdown_images(text)
        self.assertEqual([("my old friend", "http://iwillseeyou.com")], result)
        
    def test_e_i(self):
        #testing multiple images in one line
        text = "![my old friend](please come home) and ![I will keep the lights on](hurry up)"
        result = extract_markdown_images(text)
        self.assertEqual(result, [("my old friend", "please come home"), ("I will keep the lights on", "hurry up")])
        
    def test_ei_none(self):
        text = None
        result = extract_markdown_images(text)
        self.assertIs(result, None)
    
    def test_ei_no_matches(self):
        text = "ladydahdeedah"
        result = extract_markdown_images(text)
        self.assertEqual(result, [])
    
    def test_ei_raise(self):
        text = 51
        with self.assertRaises(TypeError):
            extract_markdown_images(text)

    def test_ei_image_link(self):
        text = "[hulu](hoops) something like ![wacka](mole)"
        result = extract_markdown_images(text)
        self.assertEqual(result, [("wacka", "mole")])
        
    
    
    
class TestExtractLink(unittest.TestCase):
    def test_extract_link(self):
        text = "hello darkness [my old friend](http://iwillseeyou.com)"
        result = extract_markdown_links(text)
        self.assertEqual([("my old friend", "http://iwillseeyou.com")], result)
        
    def test_e_l(self):
        #testing multiple images in one line
        text = "[my old friend](please come home) and [I will keep the lights on](hurry up)"
        result = extract_markdown_links(text)
        self.assertEqual(result, [("my old friend", "please come home"), ("I will keep the lights on", "hurry up")])
        
    def test_el_none(self):
        text = None
        result = extract_markdown_links(text)
        self.assertIs(result, None)
    
    def test_el_no_matches(self):
        text = "ladydahdeedah"
        result = extract_markdown_links(text)
        self.assertEqual(result, [])
    def test_el_raise(self):
        text = 51
        with self.assertRaises(TypeError):
            extract_markdown_links(text)

    def test_nest(self):
        text = "[![something](witty)](entertainment)"
        result = extract_markdown_links(text)
        self.assertEqual(result, [("![something](witty)", "entertainment")])
    
    def test_near(self):
        text = "[![something](witty)](entertainment)[blaghity](spot)"
        result = extract_markdown_links(text)
        self.assertEqual(result, [("![something](witty)", "entertainment"), ("blaghity", "spot")])

class TestSplitNodeImage(unittest.TestCase):
    def test_split_nodes_image(self):
        text = TextNode("something ![checkovs](gun) fires away ![away](again) alleyoop", TextType.TEXT)
        result = split_nodes_image([text])
        self.assertEqual(result, [TextNode("something ", TextType.TEXT), TextNode("checkovs", TextType.IMAGE, "gun"), TextNode(" fires away ", TextType.TEXT), TextNode("away", TextType.IMAGE, "again"), TextNode(" alleyoop", TextType.TEXT)])

    def test_split_nodes_image_with_a_link(self):
        node = TextNode("![check](ov) has a gun [in](hand)", TextType.TEXT)
        result = split_nodes_image([node])
        self.assertEqual(result, [TextNode("check", TextType.IMAGE, "ov"), TextNode(" has a gun [in](hand)", TextType.TEXT)])

    def test_split_nodes_image_with_url_syntax(self):
        node = TextNode("![google](/user/documents/bin/temp) is where I keep my underpants", TextType.TEXT)
        result = split_nodes_image([node])
        self.assertEqual(result, [TextNode("google", TextType.IMAGE, "/user/documents/bin/temp"), TextNode(" is where I keep my underpants", TextType.TEXT)])

    
    
    def test_split_nodes_image_multi_nodes(self):
        node = [TextNode("google ![moogle](exam)", TextType.TEXT), TextNode("banana ![scram](ble)", TextType.TEXT)]
        result = split_nodes_image(node)
        self.assertEqual(result, [TextNode("google ", TextType.TEXT), TextNode("moogle", TextType.IMAGE, "exam"), TextNode("banana ", TextType.TEXT), TextNode("scram", TextType.IMAGE, "ble")])
    
    def test_split_image_none(self):
        node = None
        result = split_nodes_image(node)
        self.assertEqual(result, [])

    def test_split_image_noimg(self):
        node = TextNode("something witty", TextType.TEXT)
        result = split_nodes_image([node])
        self.assertEqual([node], result)
    def test_split_image_end_in_an_image(self):
        node = TextNode("end in an ![image](friends)", TextType.TEXT)
        result = split_nodes_image([node])
        self.assertEqual([TextNode("end in an ", TextType.TEXT), TextNode("image", TextType.IMAGE, "friends")],
                         result)
    
    def test_split_image_non_text(self):
        node = TextNode("somesome", TextType.BOLD)
        result = split_nodes_image([node])
        self.assertEqual([node], result)
    
    def test_split_image_empty(self):
        node = []
        result = split_nodes_image(node)
        self.assertEqual(result, [])
    
class TestSplitNodeLinks(unittest.TestCase):
    def test_split_links(self):
        node = TextNode("[moogle](exam)", TextType.TEXT)
        result = split_nodes_link([node])
        self.assertEqual([TextNode("moogle", TextType.LINK, "exam")], result)

    def test_split_links_multi(self):
        node = TextNode("a new [a](b) is upon us [c](d) here ![my](love) hera", TextType.TEXT)
        result = split_nodes_link([node])
        self.assertEqual([TextNode("a new ", TextType.TEXT),
                          TextNode("a", TextType.LINK, "b"),
                          TextNode(" is upon us ", TextType.TEXT),
                          TextNode("c", TextType.LINK, "d"),
                          TextNode(" here ![my](love) hera", TextType.TEXT)
                          ], result
                          )
    
    def test_split_with_url(self):
        node = TextNode("a new [dawn](http://google.com) is upon us", TextType.TEXT)
        result = split_nodes_link([node])
        self.assertEqual([TextNode("a new ", TextType.TEXT), 
                        TextNode("dawn", TextType.LINK, "http://google.com"),
                        TextNode(" is upon us", TextType.TEXT)],
                          result)
        
    def test_split_link_non_text(self):
        node = TextNode("somesome", TextType.BOLD)
        result = split_nodes_link([node])
        self.assertEqual([node], result)
    
    def test_split_link_empty(self):
        node = []
        result = split_nodes_link(node)
        self.assertEqual(result, [])
    
    def test_split_link_end_link(self):
        node = TextNode("some [link](here)", TextType.TEXT)
        result = split_nodes_link([node])
        self.assertEqual([TextNode("some ", TextType.TEXT), TextNode("link", TextType.LINK, "here")], result)

class TestTextToTextNode(unittest.TestCase):
    def test_text_to_TN(self):
        text = "some _text_ `here`, **bold**,"
        a = TextNode
        b = TextType
        result = text_to_textnodes(text)
        self.assertEqual(result, [a("some ", b.TEXT), 
                                  a("text", b.ITALIC),
                                  a(" ", b.TEXT),
                                  a("here", b.CODE),
                                  a(", ", b.TEXT),
                                  a("bold", b.BOLD),
                                  a(",", b.TEXT)])
    def test_text_to_TN_image_link(self):
        text = "![image](spot) is [here](now)"
        a = TextNode
        b = TextType.IMAGE
        c = TextType.LINK
        result = text_to_textnodes(text)
        self.assertEqual(result, 
                         [a("image", b, "spot"),
                          a(" is ", TextType.TEXT),
                          a("here", c, "now")])
    
    def test_text_to_TN_nest(self):
        text = "[![nest](forever)](mychild)"
        result = text_to_textnodes(text)
        self.assertEqual(result, 
                         [TextNode("![nest](forever)", TextType.LINK, "mychild")])
        
    def test_text_to_TN_link_image_nest_proper_format(self):
        text = "[link](http://google.com)![image](/src/image)[![image](/img/native)](http://dummy.com)"
        result = text_to_textnodes(text)
        self.assertEqual(result,
                         [TextNode("link", TextType.LINK, "http://google.com"),
                          TextNode("image", TextType.IMAGE, "/src/image"),
                          TextNode("![image](/img/native)", TextType.LINK, "http://dummy.com")
                          ])
    
    
    
    
    
    
    
    
