class HTMLNode():
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        result = ""
        
        if self.props == None:
            return result
        
        for key, value in self.props.items():
            result += f' {key}="{value}"'
        
        return result
    
    def __repr__(self):
        return f"HTMLNode ({self.tag}) ({self.value}) ({self.children}) ({self.props})"
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)
        self.tag = tag
        self.value = value
        self.props = props
    
    def to_html(self):
        if len(self.value) == 0:
            raise ValueError("All leaf nodes must have a value.")
        if not self.tag or len(self.tag) == 0:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
            
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
        self.tag = tag
        self.children = children
        self.props = props
        
    def to_html(self):
        if len(self.tag) == 0:
            raise ValueError("Tag is required")
        if len(self.children) == 0:
            raise ValueError("Children is required")
        
        children_tags = ""
                
        for child in self.children:
            children_tags += f"{child.to_html()}"
            
        print("children_tagschildren_tags", children_tags)
        
        
        return f"<{self.tag}{self.props_to_html()}>{children_tags}</{self.tag}>"