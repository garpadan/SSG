import unittest

from src.text_to_html import *

class TestTextNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_text_node_to_html_node_image(self):
        node = TextNode("A cool image", TextType.IMAGE, "https://example.com/img.png")
        html_node = text_node_to_html_node(node)       
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props, 
            {"src": "https://example.com/img.png", "alt": "A cool image"}
    )



if __name__ == "__main__":
    unittest.main()