from .htmlnode import LeafNode
from .textnode import TextType

def text_node_to_html_node(text_node):
    if text_node.text_type not in TextType:
        raise ValueError("Text type not available")
    
    node = None
    
    if text_node.text_type == TextType.TEXT:
        node = LeafNode(None, text_node.text)
    if text_node.text_type == TextType.BOLD:
        node = LeafNode("b", text_node.text)
    if text_node.text_type == TextType.ITALIC:
        node = LeafNode("i", text_node.text)
    if text_node.text_type == TextType.CODE:
        node = LeafNode("code", text_node.text)
    if text_node.text_type == TextType.LINK:
        node = LeafNode("a", text_node.text, {"href", text_node.url})
    if text_node.text_type == TextType.IMAGE:
        node = LeafNode("img", None, {"src": text_node.url, "alt": text_node.text_node.text})
        
    return node