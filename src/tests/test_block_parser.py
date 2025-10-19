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
    
    def test_headings_and_paragraphs(self):
        md = """
            # First heading

            This is the first paragraph with **bold** text.

            ## Second heading

            This is the second paragraph with _italic_ text.
        """
        
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>First heading</h1><p>This is the first paragraph with <b>bold</b> text.</p><h2>Second heading</h2><p>This is the second paragraph with <i>italic</i> text.</p></div>",
        )
    
    def test_blockquote(self):
        md = """
            > This is a quote
            > with multiple lines
            
            This is a paragraph after the quote.

            > Another quote here
        """
            
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a quote with multiple lines</blockquote><p>This is a paragraph after the quote.</p><blockquote>Another quote here</blockquote></div>",
        )
    
    def test_markdown_to_html_full(self):
        md = """
            # This is a heading

            This is a **paragraph** with some text.

            ## This is a second heading

            > This is a quote
            > spanning multiple lines

            This is another paragraph with _italic_ and `inline code`.

            ### Smaller heading

            > Another quote here
        """
    
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>This is a heading</h1><p>This is a <b>paragraph</b> with some text.</p><h2>This is a second heading</h2><blockquote>This is a quote spanning multiple lines</blockquote><p>This is another paragraph with <i>italic</i> and <code>inline code</code>.</p><h3>Smaller heading</h3><blockquote>Another quote here</blockquote></div>",
        )
    
    def test_ordered_list(self):
        md = """
    This is a paragraph before the list.

    1. First item
    2. Second **bold** item
    3. Third item

    This is a paragraph after the list.
    """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is a paragraph before the list.</p><ol><li>First item</li><li>Second <b>bold</b> item</li><li>Third item</li></ol><p>This is a paragraph after the list.</p></div>"
        )
    
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
            

    def test_lists_with_nested_links_and_images(self):
        md = """
    # A Document with Lists and Media

    This document contains various list types with nested links and images.

    ### Unordered List
    
    *   A simple list item.
    *   A list item with [a link to a website](https://www.example.com).
    *   A final simple item.

    ### Ordered List
    
    1.  The first step is to show an image: ![alt text for image](https://www.example.com/image.png)
    2.  The second step is a plain instruction.
    3.  The third step has both: ![another image](https://www.example.com/image2.png) and [another link](https://www.example.com/page2).
    """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            '<div><h1>A Document with Lists and Media</h1><p>This document contains various list types with nested links and images.</p><h3>Unordered List</h3><ul><li>A simple list item.</li><li>A list item with <a href="https://www.example.com">a link to a website</a>.</li><li>A final simple item.</li></ul><h3>Ordered List</h3><ol><li>The first step is to show an image: <img src="https://www.example.com/image.png" alt="alt text for image"></li><li>The second step is a plain instruction.</li><li>The third step has both: <img src="https://www.example.com/image2.png" alt="another image"> and <a href="https://www.example.com/page2">another link</a>.</li></ol></div>'
        )
    
    def test_all_block_types_comprehensive(self):
        """Comprehensive test with all block types: heading, paragraph, code, quote, unordered list, ordered list"""
        md = """
# Main Heading Level 1

This is a **paragraph** with some _italic_ text and `inline code`. It also has a [link](https://www.example.com) and an image: ![alt text](https://www.example.com/image.png)

## Subheading Level 2

Here's another paragraph before a code block.

```
def hello_world():
print("This is a **code** block")
return True
```

### Heading Level 3

> This is a blockquote
> spanning multiple lines
> with **bold** and _italic_ text

This is a paragraph between blocks.

#### Heading Level 4

- First unordered list item
- Second item with **bold text**
- Third item with [a link](https://www.boot.dev)

##### Heading Level 5

1. First ordered item
2. Second ordered item with _italic_
3. Third ordered item with `code`

###### Heading Level 6

Final paragraph to wrap things up with all inline elements: **bold**, _italic_, `code`, [link](https://final.com), and ![image](https://final.com/img.png).
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        
        expected_html = (
            '<div>'
            '<h1>Main Heading Level 1</h1>'
            '<p>This is a <b>paragraph</b> with some <i>italic</i> text and <code>inline code</code>. '
            'It also has a <a href="https://www.example.com">link</a> and an image: '
            '<img src="https://www.example.com/image.png" alt="alt text"></p>'
            '<h2>Subheading Level 2</h2>'
            '<p>Here\'s another paragraph before a code block.</p>'
            '<pre><code>def hello_world():\nprint("This is a **code** block")\nreturn True\n</code></pre>'
            '<h3>Heading Level 3</h3>'
            '<blockquote>This is a blockquote spanning multiple lines with <b>bold</b> and <i>italic</i> text</blockquote>'
            '<p>This is a paragraph between blocks.</p>'
            '<h4>Heading Level 4</h4>'
            '<ul>'
            '<li>First unordered list item</li>'
            '<li>Second item with <b>bold text</b></li>'
            '<li>Third item with <a href="https://www.boot.dev">a link</a></li>'
            '</ul>'
            '<h5>Heading Level 5</h5>'
            '<ol>'
            '<li>First ordered item</li>'
            '<li>Second ordered item with <i>italic</i></li>'
            '<li>Third ordered item with <code>code</code></li>'
            '</ol>'
            '<h6>Heading Level 6</h6>'
            '<p>Final paragraph to wrap things up with all inline elements: <b>bold</b>, <i>italic</i>, '
            '<code>code</code>, <a href="https://final.com">link</a>, and '
            '<img src="https://final.com/img.png" alt="image">.</p>'
            '</div>'
        )
        
        self.assertEqual(html, expected_html)

if __name__ == "__main__":
    unittest.main()