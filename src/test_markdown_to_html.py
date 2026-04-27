import unittest
from markdown_blocks import *
from inline_markdown import *
from htmlnode import *
from textnode import *
from markdown_to_html import *

class TestMarkdownToHTML(unittest.TestCase):
    def test_md_to_html_functional(self):
        md = """
This is a **bolded** paragraph
text in a p tag here

> This is a quote block _has italic text_

- This is an unordered list
- This is another item for that list
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, """<div><p>This is a <b>bolded</b> paragraph
text in a p tag here</p><blockquote>This is a quote block <i>has italic text</i></blockquote><ul><li>This is an unordered list</li><li>This is another item for that list</li></ul></div>""")
        
    def test_md_to_html_complex(self):
        md = """
This ![alt text](/src/root)
In a paragraph [with](http://google.com)

```
Code Here
```

1. List 1
2. List 2
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = """<div><p>This <img src="/src/root" alt="alt text"></img>
In a paragraph <a href="http://google.com">with</a></p><pre><code>
Code Here
</code></pre><ol><li>List 1</li><li>List 2</li></ol></div>"""
        self.assertEqual(html, expected)

    def test_md_to_html_headings(self):
        md = """
#### This is a heading"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, """<div><h4>This is a heading</h4></div>""")