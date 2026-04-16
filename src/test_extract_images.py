import unittest
from extract_markdown import *

class TestTextNode(unittest.TestCase):
    def test_extract_markdown_image(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and a second ![image2](https://i.imgur.com/zjjcJKZ111.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png"),("image2", "https://i.imgur.com/zjjcJKZ111.png")], matches)   

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], matches)

    def test_extract_markdown_links_excludes_images(self):
        text = "This is an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://boot.dev)"
        matches = extract_markdown_links(text)
        
        self.assertEqual([("link", "https://boot.dev")], matches)

    def test_extract_only_image(self):
        text = "![only an image](https://i.imgur.com/zjjcJKZ.png)"
        matches = extract_markdown_links(text)
        
        self.assertEqual([], matches)

if __name__ == "__main__":
    unittest.main()