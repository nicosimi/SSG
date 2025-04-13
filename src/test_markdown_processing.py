import unittest
from markdown_processing import BlockType, block_to_blocktype, markdown_to_blocks

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

class Test_block_to_blocktype(unittest.TestCase):
    def test_paragraph(self):
        text = "this is text"
        self.assertEqual(block_to_blocktype(text), BlockType.PARAGRAPH)

    def test_code(self):
        text = "```this is code```"
        self.assertEqual(block_to_blocktype(text), BlockType.CODE)
    
    def test_heading(self):
        text = "##this is heading"
        self.assertEqual(block_to_blocktype(text), BlockType.HEADING)

    def test_quote(self):
        text = ">this is quote"
        self.assertEqual(block_to_blocktype(text), BlockType.QUOTE)

    def test_quote_multiline(self):
        text= """>this is quote
        >this is also quote"""
        self.assertEqual(block_to_blocktype(text), BlockType.QUOTE)
    
    def test_unordered_list(self):
        text = "- this is unordered list"
        self.assertEqual(block_to_blocktype(text), BlockType.UNORDERED_LIST)

    def test_unordered_list_multiline(self):
        text = """- this is unordered list
        - this is also unordered list"""
        self.assertEqual(block_to_blocktype(text), BlockType.UNORDERED_LIST)
    
    def test_ordered_list(self):
        text = "1. this is ordered list"
        self.assertEqual(block_to_blocktype(text), BlockType.ORDERED_LIST)
    
    def test_ordered_list_multiline(self):
        text = """1. this is ordered list
        2. this is also ordered list"""
        self.assertEqual(block_to_blocktype(text), BlockType.ORDERED_LIST)
