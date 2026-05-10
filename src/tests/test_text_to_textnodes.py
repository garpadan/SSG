import unittest
from src.text_to_textnodes import *

class TestTextNode(unittest.TestCase):
    def test_full_pipeline(self):
        """Tests a string containing every supported markdown type."""
        text = "This is **bold** with an _italic_ word and a `code block` and an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertListEqual(expected, nodes)

    def test_only_text(self):
        """Tests that a plain string returns a single TEXT node."""
        text = "Just some plain text here."
        nodes = text_to_textnodes(text)
        self.assertListEqual([TextNode("Just some plain text here.", TextType.TEXT)], nodes)

    def test_multiple_of_same_type(self):
        """Tests that the function handles multiple instances of the same delimiter."""
        text = "This is **bold** and this is **also bold**."
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and this is ", TextType.TEXT),
            TextNode("also bold", TextType.BOLD),
            TextNode(".", TextType.TEXT),
        ]
        self.assertListEqual(expected, nodes)

    def test_no_text_between_delimiters(self):
        """Tests strings that start or end with markdown symbols."""
        text = "**Bold**_Italic_![img](url)"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("Bold", TextType.BOLD),
            TextNode("Italic", TextType.ITALIC),
            TextNode("img", TextType.IMAGE, "url"),
        ]
        self.assertListEqual(expected, nodes)


if __name__ == "__main__":
    unittest.main()