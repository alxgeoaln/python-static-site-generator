import re

from .blocknode import BlockType, BlockNode
from .htmlnode import ParentNode
from .text_parsers import text_to_textnodes, split_nodes_delimiter,text_node_to_html_node
from .textnode import TextNode, TextType

# heading
headingRegex = r"^(#+)"

def markdown_to_blocks(markdown):
    lines = markdown.split('\n')
    stripped_lines = [line.strip() for line in lines]
    normalized_markdown = '\n'.join(stripped_lines)
    blocks = normalized_markdown.split('\n\n')
    result = [block.strip() for block in blocks if block.strip()]
    
    return result

def block_to_block_type(block):
    lines = block.split("\n")
    
    heading = block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### "))
    code_blocks = block.startswith("```") and block.endswith("```")
    quote_block = block.startswith(">")
    unordered_list = block.startswith("-") or block.startswith("*")
    
    if heading:
        return BlockType.HEADING
    elif code_blocks:
        return BlockType.CODE
    elif quote_block:
        return BlockType.QUOTE
    elif unordered_list:
        i = 1
        for line in lines:
            if not line.startswith("*") and not line.startswith("-"):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST
    elif block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH

    
def block_node_to_html_node(block_node):
    print("block_node_to_html_node", block_node)
    if block_node.block_type not in BlockType:
        raise ValueError(f"Block type is not available {block_node.block_type}")
    
    children = []
    
    if block_node.block_type != BlockType.ORDERED_LIST and block_node.block_type != BlockType.UNORDERED_LIST:
        for child in block_node.children:
            children.append(text_node_to_html_node(child))
    else:
        for block_children in block_node.children:
            li_children = []
            for child in block_children:
                li_children.append(text_node_to_html_node(child))
            children.append(ParentNode("li", li_children))
        tag = "ol"
        if block_node.block_type != BlockType.ORDERED_LIST:
            tag = "ul"
        return ParentNode(tag, children)
            
            
        
    if block_node.block_type == BlockType.PARAGRAPH:
        return ParentNode("p", children)
    
    if block_node.block_type == BlockType.HEADING:
        return ParentNode(f"h{block_node.extension}", children)
    
    if block_node.block_type == BlockType.CODE:
        return ParentNode("pre", children)
    
    if block_node.block_type == BlockType.QUOTE:
        return ParentNode("blockquote", children)
    
def split_nodes_delimiter_blocks(markdown, block_type):
    if block_type == BlockType.PARAGRAPH:
        markdown = markdown.replace("\n", " ")  # Replace newlines with spaces
        text_nodes = text_to_textnodes(markdown)
        return BlockNode(text_nodes, BlockType.PARAGRAPH)
    
    if block_type == BlockType.HEADING:
        pounds = re.match(headingRegex, markdown)
        text = markdown.split(pounds.group(1))[1]
        text_nodes = text_to_textnodes(text.replace(" ", "", 1))
        return BlockNode(text_nodes, BlockType.HEADING, len(pounds.group(1)))
    
    if block_type == BlockType.CODE:
        markdown = markdown.replace("\n", "", 1)
        text_node = TextNode(markdown, TextType.TEXT)
        text_nodes = split_nodes_delimiter([text_node], "`", TextType.CODE)
        return BlockNode(text_nodes, BlockType.CODE)
    
    if block_type == BlockType.QUOTE:
        splitted_markdown = markdown.split(">")[1:]
        markdown = "".join(splitted_markdown).replace("\n", "").replace(" ", "", 1)
        text_nodes = text_to_textnodes(markdown)
        return BlockNode(text_nodes, BlockType.QUOTE)
    
    if block_type == BlockType.ORDERED_LIST:
        items = markdown.split
        pattern = r'^\d+\. '
        items = re.split(pattern, markdown, flags=re.MULTILINE)

        # The first split is usually empty, remove it
        items = [item.strip() for item in items if item.strip()]
        text_nodes = []
        for item in items:
            text_nodes.append(text_to_textnodes(item))
        return BlockNode(text_nodes, BlockType.ORDERED_LIST)
    
    if block_type == BlockType.UNORDERED_LIST:
        items = markdown.split("\n")
        
        items = [item.strip() for item in items if item.strip()]
        text_nodes = []
        for item in items:
            clean = re.sub(r"^[-*]\s*", "", item, count=1)
            text_nodes.append(text_to_textnodes(clean))
            
        return BlockNode(text_nodes, BlockType.UNORDERED_LIST)
            

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        if len(block) == 0:
            continue
        
        block_type = block_to_block_type(block)
        print("BLOCKKKK", block, block_type)
        block_node = split_nodes_delimiter_blocks(block, block_type)
        
        node = block_node_to_html_node(block_node)
        children.append(node)
        
    return ParentNode("div", children)
        
