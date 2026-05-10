import unittest
from src.extract_title import extract_title

class TestExtractTitle(unittest.TestCase):
    def test_basic_h1(self):
        # Standard case
        self.assertEqual(extract_title("# Hello"), "Hello")

    def test_h1_with_whitespace(self):
        # Testing stripping of extra spaces
        self.assertEqual(extract_title("#   Hello World   "), "Hello World")

    def test_h1_among_other_blocks(self):
        # Testing finding the H1 when other content exists
        md = """
## Subtitle
Some paragraph text.
# The Main Title
More text here.
"""
        self.assertEqual(extract_title(md), "The Main Title")

    def test_no_h1_raises_exception(self):
        # Testing that it raises an exception if no H1 is present
        md = "## This is only an H2"
        with self.assertRaises(Exception) as cm:
            extract_title(md)
        self.assertEqual(str(cm.exception), "The markdown file has no title.")

    def test_false_h1(self):
        # Ensure it doesn't get confused by H2 or headers with no space
        # (Though Markdown usually requires a space after #, it's good to be strict)
        md = "## Title\n### Subtitle\n#TitleWithNoSpace"
        with self.assertRaises(Exception):
            extract_title(md)

    def test_empty_h1(self):
        # Testing a header with no content
        self.assertEqual(extract_title("# "), "")

if __name__ == "__main__":
    unittest.main()