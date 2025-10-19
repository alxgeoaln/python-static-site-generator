import re

from .htmlnode import LeafNode
from .textnode import TextType, TextNode

# images
imagesRegex = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"

# regular links
linksRegex = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"

def text_node_to_html_node(text_node):
    if text_node.text_type not in TextType:
        raise ValueError(f"Text type not available {text_node.text_type}")
    
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
        node = LeafNode("a", text_node.text, {"href": text_node.url})
    if text_node.text_type == TextType.IMAGE:
        node = LeafNode("img", None, {"src": text_node.url, "alt": text_node.text})
    return node

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    
    for node in old_nodes:
        if not isinstance(node, TextNode) or node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        
        text = node.text.split(delimiter)
        
        if len(text) % 2 != 1:
            raise ValueError(f"no closing delimiter: '{delimiter}' for -> {node.text}")
        
        for i in range(len(text)):
            if text[i] == "":
                continue
            if i % 2 == 1:
                new_nodes.append(TextNode(text[i], text_type))
            else:
                new_nodes.append(TextNode(text[i], TextType.TEXT))
                
            
    return new_nodes
        
def extract_markdown_images(text):
    return re.findall(imagesRegex, text)

def extract_markdown_links(text):
    return re.findall(linksRegex, text)

def split_nodes_image(old_nodes):
    new_nodes = []
    
    text = ""
    
    for node in old_nodes:
        if not isinstance(node, TextNode) or node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        
        imgs = extract_markdown_images(node.text)
        
        if len(imgs) == 0:
            new_nodes.append(node)
            continue
        
        text = node.text
        
        for i in range(len(imgs)):
            img = imgs[i]
            splitted_text = text.split(f"![{img[0]}]({img[1]})")
            if len(splitted_text) != 2:
                raise Exception("image tag not closed")
            if splitted_text[0] != "":
                new_nodes.append(TextNode(splitted_text[0], TextType.TEXT))
            new_nodes.append(TextNode(img[0], TextType.IMAGE, img[1]))
            text = splitted_text[1]
            
            if(i == len(imgs) - 1 and text != ""):
                new_nodes.append(TextNode(text, TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    
    text = ""
    
    for node in old_nodes:
        if not isinstance(node, TextNode) or node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        
        links = extract_markdown_links(node.text)
        
        if len(links) == 0:
            new_nodes.append(node)
            continue
        
        text = node.text
        
        for i in range(len(links)):
            link = links[i]
            splitted_text = text.split(f"[{link[0]}]({link[1]})")
            if len(splitted_text) != 2:
                raise Exception("link tag not closed")
            if splitted_text[0] != "":
                new_nodes.append(TextNode(splitted_text[0], TextType.TEXT))
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            text = splitted_text[1]
        if i == len(links) - 1 and text != "":
            new_nodes.append(TextNode(text, TextType.TEXT))
        
    return new_nodes
        
def text_to_textnodes(text):
    node = TextNode(text, TextType.TEXT)
    text_bold_nodes =  split_nodes_delimiter([node], "**", TextType.BOLD)
    text_italic_nodes = split_nodes_delimiter(text_bold_nodes, "_", TextType.ITALIC)
    text_code_nodes = split_nodes_delimiter(text_italic_nodes, "`", TextType.CODE)
    text_links_nodes = split_nodes_link(text_code_nodes)
    text_imgs_nodes = split_nodes_image(text_links_nodes)
    return text_imgs_nodes
    