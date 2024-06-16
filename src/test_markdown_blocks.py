import unittest
from markdown_blocks import markdown_to_blocks


class TestMarkdownBlocks(unittest.TestCase):
    def test_markdown_to_splits(self):
        text = """This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items"""
        self.assertEqual(
            [
                "This is **bolded** paragraph",
                """This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line""",
                """* This is a list
* with items""",
            ],
            markdown_to_blocks(text),
        )

    def test_markdown_to_splits_with_leading_whitespaces(self):
        text = """     This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

        * This is a list
* with items"""
        self.assertEqual(
            [
                "This is **bolded** paragraph",
                """This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line""",
                """* This is a list
* with items""",
            ],
            markdown_to_blocks(text),
        )

    def test_markdown_to_splits_with_empty_blocks(self):
        text = """This is **bolded** paragraph








This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items"""

        self.assertEqual(
            [
                "This is **bolded** paragraph",
                """This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line""",
                """* This is a list
* with items""",
            ],
            markdown_to_blocks(text),
        )


if __name__ == "__main__":
    unittest.main()
