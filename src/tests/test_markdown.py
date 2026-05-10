import unittest

from src.textnode import TextNode, TextType
from src.markdown_handling import *


class TestTextNode(unittest.TestCase):
    def test_paragraphs(self):
        md = """
    This is **bolded** paragraph
    text in a p
    tag here

    This is another paragraph with _italic_ text and `code` here

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        # The content must be flush against the left margin
        md = """```
This is text that _should_ remain
the **same** even with inline stuff
```"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_paragraph(self):
            block = "This is a simple paragraph."
            node = block_to_html_node(block, BlockType.PARAG)
            html = node.to_html()
            self.assertEqual(html, "<p>This is a simple paragraph.</p>")

    def test_heading(self):
        block = "### This is a title"
        node = block_to_html_node(block, BlockType.HEAD)
        html = node.to_html()
        self.assertEqual(html, "<h3>This is a title</h3>")

    def test_code(self):
        # The input block
        block = """```
def hello():
    print('hi')
```"""
        node = block_to_html_node(block, BlockType.CODE)
        html = node.to_html()
        
        # The expected output must match the content of the block
        expected = "<pre><code>def hello():\n    print('hi')\n</code></pre>"
        self.assertEqual(html, expected)

    def test_quote(self):
        block = "> This is a quote\n> with two lines"
        node = block_to_html_node(block, BlockType.QUOTE)
        html = node.to_html()
        self.assertEqual(html, "<blockquote>This is a quote with two lines</blockquote>")

    def test_unordered_list(self):
        block = "* Item 1\n* Item 2"
        node = block_to_html_node(block, BlockType.UL)
        html = node.to_html()
        self.assertEqual(html, "<ul><li>Item 1</li><li>Item 2</li></ul>")

    def test_ordered_list(self):
        block = "1. First\n2. Second"
        node = block_to_html_node(block, BlockType.OL)
        html = node.to_html()
        self.assertEqual(html, "<ol><li>First</li><li>Second</li></ol>")

    def test_invalid_type(self):
        with self.assertRaises(ValueError):
            block_to_html_node("some text", "not_a_real_type")

if __name__ == "__main__":
    unittest.main()