import unittest
from functions import text_node_to_html_node, split_nodes_delimiter,extract_markdown_images, extract_markdown_links
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

    def test_split_nodes_delimiter(self):
        old_nodes = [TextNode("this is plain text, no mods needed has a url, shouldn't do anything", TextType.TEXT, "https:dummy.com"),
                    TextNode("this is a node, with a 'code block' word", TextType.TEXT),
                    TextNode("this is a node, it has a **bold section of text** blagh", TextType.TEXT),
                    TextNode("this is a node, it has an _italic section of text_ blagh", TextType.TEXT)
                    ]
        delimiter_text_type = [("", TextType.TEXT), ("'", TextType.CODE), ("**", TextType.BOLD), ("_", TextType.ITALIC)]
        result = []
        result.extend(split_nodes_delimiter(old_nodes, delimiter_text_type[0][0], delimiter_text_type[0][1]))
        self.assertEqual("this is plain text, no mods needed has a url, shouldn't do anything", result[0].text)
        
    def test_split_nodes_code(self):
        old_nodes = [TextNode("this is a node, with a 'code block' word", TextType.TEXT)]
        result = split_nodes_delimiter(old_nodes, "'", TextType.CODE)
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
        old_nodes = [TextNode("this is a node, with a 'code block'", TextType.TEXT)]
        result = split_nodes_delimiter(old_nodes, "'", TextType.CODE)
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