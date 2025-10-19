import unittest
from src.block_parser import markdown_to_blocks, block_to_block_type, BlockType, markdown_to_html_node

class TestBlockParser(unittest.TestCase):
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
        
    def test_block_to_block_types(self):
        block = "# heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
        block = "```\ncode\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
        block = "> quote\n> more quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
        block = "- list\n- items"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)
        block = "1. list\n2. items"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)
        block = "paragraph"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    # def test_paragraphs(self):
    #     md = """
    # This is **bolded** paragraph
    # text in a p
    # tag here

    # This is another paragraph with _italic_ text and `code` here

    # """

    #     node = markdown_to_html_node(md)
    #     print("NODEINTESTTT->>>", node)
    #     html = node.to_html()
    #     self.assertEqual(
    #         html,
    #         "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
    #     )

    # def test_codeblock(self):
    #     md = """
    #         ```
    #         This is text that _should_ remain
    #         the **same** even with inline stuff
    #         ```
    #         """

    #     node = markdown_to_html_node(md)
    #     html = node.to_html()
    #     self.assertEqual(
    #         html,
    #         "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
    #     )
    
    # def test_headings_and_paragraphs(self):
    #     md = """
    #         # First heading

    #         This is the first paragraph with **bold** text.

    #         ## Second heading

    #         This is the second paragraph with _italic_ text.
    #     """
        
    #     node = markdown_to_html_node(md)
    #     html = node.to_html()
    #     self.assertEqual(
    #         html,
    #         "<div><h1>First heading</h1><p>This is the first paragraph with <b>bold</b> text.</p><h2>Second heading</h2><p>This is the second paragraph with <i>italic</i> text.</p></div>",
    #     )
    
    # def test_blockquote(self):
    #     md = """
    #         > This is a quote
    #         > with multiple lines
            
    #         This is a paragraph after the quote.

    #         > Another quote here
    #     """
            
    #     node = markdown_to_html_node(md)
    #     html = node.to_html()
    #     self.assertEqual(
    #         html,
    #         "<div><blockquote>This is a quote with multiple lines</blockquote><p>This is a paragraph after the quote.</p><blockquote>Another quote here</blockquote></div>",
    #     )
    
    # def test_markdown_to_html_full(self):
    #     md = """
    #         # This is a heading

    #         This is a **paragraph** with some text.

    #         ## This is a second heading

    #         > This is a quote
    #         > spanning multiple lines

    #         This is another paragraph with _italic_ and `inline code`.

    #         ### Smaller heading

    #         > Another quote here
    #     """
    
    #     node = markdown_to_html_node(md)
    #     html = node.to_html()
    #     self.assertEqual(
    #         html,
    #         "<div><h1>This is a heading</h1><p>This is a <b>paragraph</b> with some text.</p><h2>This is a second heading</h2><blockquote>This is a quote spanning multiple lines</blockquote><p>This is another paragraph with <i>italic</i> and <code>inline code</code>.</p><h3>Smaller heading</h3><blockquote>Another quote here</blockquote></div>",
    #     )
    
    # def test_ordered_list(self):
    #     md = """
    # This is a paragraph before the list.

    # 1. First item
    # 2. Second **bold** item
    # 3. Third item

    # This is a paragraph after the list.
    # """
    #     node = markdown_to_html_node(md)
    #     html = node.to_html()
    #     self.assertEqual(
    #         html,
    #         "<div><p>This is a paragraph before the list.</p><ol><li>First item</li><li>Second <b>bold</b> item</li><li>Third item</li></ol><p>This is a paragraph after the list.</p></div>"
    #     )
    
    def test_unordered_list(self):
        md = """
    This is a paragraph before the unordered list.

    - Item one
    * _Item two_ in italics
    - Item three

    This paragraph comes after the list.
    """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is a paragraph before the unordered list.</p><ul><li>Item one</li><li><i>Item two</i> in italics</li><li>Item three</li></ul><p>This paragraph comes after the list.</p></div>"
        )
        
    # In your test class, which inherits from unittest.TestCase

    def test_full_document_with_mixed_lists(self):
        md = """
    # Main Document Title

    Here is a short paragraph to introduce the lists.

    *   First item in the unordered list
    *   Second item, also unordered
    -   Third item using a hyphen

    And now, for the main points in order:

    1.  This is the very first step.
    2.  The second step is **extremely important**.
    3.  Finally, the third step concludes the process.
    """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Main Document Title</h1><p>Here is a short paragraph to introduce the lists.</p><ul><li>First item in the unordered list</li><li>Second item, also unordered</li><li>Third item using a hyphen</li></ul><p>And now, for the main points in order:</p><ol><li>This is the very first step.</li><li>The second step is <b>extremely important</b>.</li><li>Finally, the third step concludes the process.</li></ol></div>"
        )
            
if __name__ == "__main__":
    unittest.main()