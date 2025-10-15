from enum import Enum

from htmlnode import LeafNode

class TextType(Enum):
    TEXT = "text"
    BOLD = "**Bold**"
    ITALIC = "_Italic text_"
    CODE = "`Code text`"
    LINK = "[anchor text](url)"
    IMAGE = "![alt text](url)"
    
class TextNode():
    def __init__(self, text, text_type, url = None):
        self.text = text
        self.text_type = text_type
        self.url = url
    
    def __eq__(self, text_node):
        return self.text == text_node.text and self.text_type == text_node.text_type and self.url == text_node.url
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
    

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