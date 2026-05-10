import unittest

from src.htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        print("Props Test:")
        props_test = {
            "href": "https://www.google.com",
            "target": "_blank",
        }

        node = HTMLNode("a", "Google", None, props_test)
        expected_output = ' href="https://www.google.com" target="_blank"'

        self.assertEqual(node.props_to_html(), expected_output)
    
    def test_propts_to_html_empty(self):
        node = HTMLNode("p", "No props here")
        self.assertEqual(node.props_to_html(), "")
    
    def test_children(self):
        child_node = HTMLNode("span", "child")
        parent_node = HTMLNode("div", None, [child_node])

        self.assertEqual(len(parent_node.children), 1)
        self.assertEqual(parent_node.children[0].tag, "span")

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_2(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_leaf_to_html_2(self):
        node = LeafNode(None, "This has no tag.")
        self.assertEqual(node.to_html(), "This has no tag.")
    
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
    def test_to_html_multiple_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        expected = "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        self.assertEqual(node.to_html(), expected)

    def test_to_html_no_children(self):
        node = ParentNode("div", [])
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_with_props(self):
        node = ParentNode(
            "div",
            [LeafNode("span", "child")],
            {"class": "container", "id": "main"}
        )
        expected = '<div class="container" id="main"><span>child</span></div>'
        self.assertEqual(node.to_html(), expected)




if __name__ == "__main__":
    unittest.main()