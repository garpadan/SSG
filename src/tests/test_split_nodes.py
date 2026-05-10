import unittest
from src.split_nodes import *

class TestTextNode(unittest.TestCase):
    # test delimiter

    def test_split_bold(self):
        node = TextNode("This is **bold** text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[1].text, "bold")
        self.assertEqual(new_nodes[1].text_type, TextType.BOLD)

    def test_split_italic(self):
        node = TextNode("This is *italic* text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[1].text, "italic")
        self.assertEqual(new_nodes[1].text_type, TextType.ITALIC)

    def test_split_code(self):
        node = TextNode("Use `pip install` to start", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[1].text, "pip install")
        self.assertEqual(new_nodes[1].text_type, TextType.CODE)

    def test_split_multiple(self):
        node = TextNode("This **is** a **test**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        # Expected: ["This ", "is", " a ", "test"]
        self.assertEqual(len(new_nodes), 4)
        self.assertEqual(new_nodes[1].text, "is")
        self.assertEqual(new_nodes[3].text, "test")

    def test_split_start_and_end(self):
        node = TextNode("**Bold** at start and **end**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        # Even if bold is at the start, index 0 might be an empty string
        # Depending on your logic, you might want to filter those out.
        self.assertEqual(new_nodes[0].text, "Bold")
        self.assertEqual(new_nodes[-1].text, "end")

    def test_invalid_markdown(self):
        node = TextNode("This is **invalid bold", TextType.TEXT)
        # This should catch the missing closing **
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "**", TextType.BOLD)

    # test split

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with an [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_images_at_edges(self):
        node = TextNode(
            "![first](https://url1.com)between![second](https://url2.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("first", TextType.IMAGE, "https://url1.com"),
                TextNode("between", TextType.TEXT),
                TextNode("second", TextType.IMAGE, "https://url2.com"),
            ],
            new_nodes,
        )    


if __name__ == "__main__":
    unittest.main()