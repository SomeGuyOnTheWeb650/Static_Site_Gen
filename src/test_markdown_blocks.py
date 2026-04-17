import unittest
from markdown_blocks import markdown_to_blocks, block_to_blocktype, BlockType


class TestMarkdownToBlocks(unittest.TestCase):
    def setUp(self):
        self.markdown = "#an initial line header\n\nblock #2\n\n- block #3\n- still block #3\n\n"
        self.md = """
This is a **bolded paragraph**


This is a paragraph with an extra line break with some _italics mixed in_
This is the same paragraph but with some `code mixed in`

- This is a list item
- Another list item

* This is a list item as well
* This is a another list item

"""

    def test_md_to_block_functional(self):
        result = markdown_to_blocks(self.markdown)
        self.assertEqual(result,
                         ["#an initial line header",
                         "block #2",
                         "- block #3\n- still block #3"])
        
    def test_md_to_block_multiline_string(self):
        result = markdown_to_blocks(self.md)
        expected = ["This is a **bolded paragraph**", 
                    "This is a paragraph with an extra line break with some _italics mixed in_\n"
                    "This is the same paragraph but with some `code mixed in`",
                    "- This is a list item\n- Another list item",
                    "* This is a list item as well\n* This is a another list item"]
        self.assertEqual(result, expected)

    def test_md_to_block_wrong_input(self):
        with self.assertRaises(TypeError, msg="markdown_to_blocks takes a str input"):
            markdown_to_blocks(5)
        

    def test_block_to_blockType(self):
        block = "### Header"
        result = block_to_blocktype(block)
        self.assertEqual(result, BlockType.HEADING)    
    
    def test_block_to_blockType_FAIL(self):
        with self.assertRaises(Exception, msg="Too many #'s"):

            result = block_to_blocktype("######## Heading")
    def test_block_to_blockType_WrongFormat(self):
        with self.assertRaises(Exception, msg="header format incorrect"):
            block_to_blocktype("####Header")
    
    def test_block_to_blockType_code(self):
        text = """```
CODE
```"""
        result = block_to_blocktype(text)
        self.assertEqual(result, BlockType.CODE)
    
    def test_block_to_blockTYPE_quote(self):
        text = "> quote stuff\n> quote more stuff"
        result = block_to_blocktype(text)
        self.assertEqual(result, BlockType.QUOTE)
    
    def test_block_to_blockTYPE_quote_fail(self):
        text = "> quote stuff\n> quote more stuff\n<wrong format"
        with self.assertRaises(Exception, msg="Invalid Quote Format"):
            result = block_to_blocktype(text)
        
    def test_block_to_blockTYPE_uo(self):
        text = "- List\n- List2"
        result = block_to_blocktype(text)
        self.assertEqual(result, BlockType.UNORDERED_LIST)

    def test_block_to_blockTYPE_Fail(self):
        text = "- List\n-List2"
        with self.assertRaises(Exception, msg="Invalid UL Format"):
            block_to_blocktype(text)
    
    def test_block_to_blockTYPE_OL(self):
        text = "1. item 1\n2. item 2\n3. item 3"
        result = block_to_blocktype(text)
        self.assertEqual(result, BlockType.ORDERED_LIST)

    def test_block_to_blockTYPE_OL_Fail(self):
        text = "1. item 1\n4. item 2\n3. item 3"
        with self.assertRaises(Exception, msg="Invalid OL Format"):
            block_to_blocktype(text)
    
    def test_block_to_blockType_NORMAL(self):
        text = """
Greetings Everyone!
How are you today?
Are we ready to rock!?
"""
        result = block_to_blocktype(text)
        self.assertEqual(result, BlockType.PARAGRAPH)    
