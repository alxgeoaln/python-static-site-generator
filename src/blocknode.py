from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph",
    HEADING = "heading",
    CODE = "code",
    QUOTE = "quote",
    UNORDERED_LIST = "unordered_list",
    ORDERED_LIST = "order_list"

class BlockNode():
    def __init__(self, children, block_type, extension = None):
        self.children = children
        self.block_type = block_type
        self.extension = extension
        
    def __eq__(self, block_node):
        return self.text == block_node.text and self.block_type == block_node.block_type and self.extension == block_node.extension
    
    def __repr__(self):
        return f"Block type:{self.block_type} -- Block children: {self.children}"

       