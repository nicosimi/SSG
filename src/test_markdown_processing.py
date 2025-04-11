import unittest
from markdown_processing import markdown_to_blocks

class Test_markdown_to_blocks(unittest.TestCase):
    def test_markdown_to_blocks_1(self):
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
    
    def test_markdown_to_blocks_2(self):
        md = """
# This is a heading

This is a paragraph of text. It has some **bold** and _italic_ words inside of it.

- This is the first list item in a list block
- This is a list item
- This is another list item
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# This is a heading",
                "This is a paragraph of text. It has some **bold** and _italic_ words inside of it.",
                "- This is the first list item in a list block\n- This is a list item\n- This is another list item",
            ],
        )

    def test_markdown_to_blocks_empty_md(self):
        md = """"""
        blocks = markdown_to_blocks(md)
        self.assertListEqual([], blocks)
    
    def test_markdown_to_blocks_null_md(self):
        md = None
        blocks = markdown_to_blocks(md)
        self.assertListEqual([], blocks)

    def test_markdown_to_blocks_single_block(self):
        md = """
This is a paragraph of text.
It has some **bold** and _italic_ words inside of it."""
        blocks = markdown_to_blocks(md)
        self.assertListEqual([
            "This is a paragraph of text.\nIt has some **bold** and _italic_ words inside of it."
        ], blocks)

    def test_markdown_to_blocks_empty_blocks(self):
        md = """


This is a paragraph of text.



This is a paragraph of text.



"""
        blocks = markdown_to_blocks(md)
        self.assertListEqual([
            "This is a paragraph of text.",
            "This is a paragraph of text."], blocks)
