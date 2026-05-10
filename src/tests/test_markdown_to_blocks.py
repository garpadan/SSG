import unittest

from src.markdown_handling import *


class TestTextNode(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_newlines(self):
        md = """
    This is block 1.


        
    This is block 2 after many newlines.
    """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is block 1.",
                "This is block 2 after many newlines.",
            ],
        )

    def test_markdown_to_blocks_single(self):
        md = "Just one single block of text."
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "Just one single block of text.",
            ],
        )   

# --------- BLOCK TESTS -----------

    def test_headings(self):
        self.assertEqual(block_to_block_type("# Heading 1"), BlockType.HEAD)
        self.assertEqual(block_to_block_type("### Heading 3"), BlockType.HEAD)
        self.assertEqual(block_to_block_type("###### Heading 6"), BlockType.HEAD)
        # Fail cases
        self.assertEqual(block_to_block_type("####### Heading 7"), BlockType.PARAG)
        self.assertEqual(block_to_block_type("#Heading No Space"), BlockType.PARAG)

    def test_code_block(self):
        code = "```\nprint('hello')\n```"
        self.assertEqual(block_to_block_type(code), BlockType.CODE)
        # Fail case: missing end backticks
        self.assertEqual(block_to_block_type("```\nno closing"), BlockType.PARAG)

    def test_quote_block(self):
        quote = "> This is a quote\n> still quoting"
        self.assertEqual(block_to_block_type(quote), BlockType.QUOTE)
        # Single line quote
        self.assertEqual(block_to_block_type("> Only one line"), BlockType.QUOTE)
        # Fail case: one line missing the symbol
        bad_quote = "> Line 1\nLine 2 missing symbol"
        self.assertEqual(block_to_block_type(bad_quote), BlockType.PARAG)

    def test_unordered_list(self):
        ul = "- Item 1\n- Item 2\n- Item 3"
        self.assertEqual(block_to_block_type(ul), BlockType.UL)
        # Fail case: missing space after dash
        self.assertEqual(block_to_block_type("-Item1"), BlockType.PARAG)
        # Fail case: mixed content
        mixed = "- Item 1\nSome random text\n- Item 2"
        self.assertEqual(block_to_block_type(mixed), BlockType.PARAG)

    def test_ordered_list(self):
        ol = "1. First\n2. Second\n3. Third"
        self.assertEqual(block_to_block_type(ol), BlockType.OL)
        # Fail case: doesn't start at 1
        self.assertEqual(block_to_block_type("2. Start at two"), BlockType.PARAG)
        # Fail case: broken sequence
        broken_seq = "1. First\n3. Third"
        self.assertEqual(block_to_block_type(broken_seq), BlockType.PARAG)
        # Fail case: missing space after dot
        self.assertEqual(block_to_block_type("1.First"), BlockType.PARAG)

    def test_paragraph(self):
        text = "This is just a normal paragraph of text."
        self.assertEqual(block_to_block_type(text), BlockType.PARAG)
        # Almost a heading but not quite
        self.assertEqual(block_to_block_type(" # Leading space makes it a paragraph"), BlockType.PARAG)



if __name__ == "__main__":
    unittest.main()