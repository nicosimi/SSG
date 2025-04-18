import unittest
from markdown_processing import BlockType, block_to_blocktype, markdown_to_blocks, markdown_to_html_node

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

class Test_markdown_to_html_node(unittest.TestCase):
    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
        html,
        "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
    )

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
    )

    def test_blockquote_simple(self):
        md = "> This is a quote."
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a quote.</blockquote></div>"
        )
        
    def test_blockquote_inline(self):
        md = "> This is a **bolded** _quote_."
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a <b>bolded</b> <i>quote</i>.</blockquote></div>"
        )

    def test_blockquote_inline_link(self):
        md = "> This is a quote.Visit [boot.dev](https://www.boot.dev)."
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            """<div><blockquote>This is a quote.Visit <a href="https://www.boot.dev">boot.dev</a>.</blockquote></div>"""
        )

    def test_header1(self):
        md = "# Heading 1"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            """<div><h1>Heading 1</h1></div>"""
        )

    def test_header6(self):
        md = "###### Heading 6"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            """<div><h6>Heading 6</h6></div>"""
        )

    def test_header_inline(self):
        md = "## Visit [boot.dev](https://www.boot.dev)."
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            """<div><h2>Visit <a href="https://www.boot.dev">boot.dev</a>.</h2></div>"""
        )

    def test_unordered_list(self):
        md = """
- Item 1
- Item 2
- Item 3
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            """<div><ul><li>Item 1</li><li>Item 2</li><li>Item 3</li></ul></div>"""
        )

    def test_unordered_list_inline(self):
        md = """
- **bolded**
- Item 2
- _italic_
"""
        node = markdown_to_html_node(md)
        #print(node)
        html = node.to_html()
        self.assertEqual(
            html,
            """<div><ul><li><b>bolded</b></li><li>Item 2</li><li><i>italic</i></li></ul></div>"""
        )

    def test_unordered_list_links(self):
        md = """
- This is a paragraph with a [link](https://www.google.com).
"""
        node = markdown_to_html_node(md)
        #print(node)
        html = node.to_html()
        self.assertEqual(
            html,
            """<div><ul><li>This is a paragraph with a <a href="https://www.google.com">link</a>.</li></ul></div>"""
        )

    def test_ordered_list(self):
        md = """
1. Item 1
2. Item 2
3. Item 3
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            """<div><ol><li>Item 1</li><li>Item 2</li><li>Item 3</li></ol></div>"""
        )

    def test_ordered_list_inline(self):
        md = """
1. **bolded**
2. Item 2
3. _italic_
"""
        node = markdown_to_html_node(md)
        #print(node)
        html = node.to_html()
        self.assertEqual(
            html,
            """<div><ol><li><b>bolded</b></li><li>Item 2</li><li><i>italic</i></li></ol></div>"""
        )

    def test_ordered_list_links(self):
        md = """
1. This is a paragraph with a [link](https://www.google.com).
"""
        node = markdown_to_html_node(md)
        #print(node)
        html = node.to_html()
        self.assertEqual(
            html,
            """<div><ol><li>This is a paragraph with a <a href="https://www.google.com">link</a>.</li></ol></div>"""
        )
