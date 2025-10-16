import unittest

from src.htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_node(self):
        node = HTMLNode("p", "abc", None, None)
        self.assertEqual(node.tag, "p")
        
    def test_to_html(self):
        node = HTMLNode("p", "abc", None, {
            "href": "https://www.google.com",
            "target": "_blank",
        })
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')
        
    def test_to_html_with_id(self):
        node = HTMLNode("p", "abc", None, {
            "id": "test",
        })
        self.assertEqual(node.props_to_html(), ' id="test"')
        
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
        
    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')
        
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")
    
    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
    )
        
    def test_to_html_with_grandchildren_a(self):
        grandchild_node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        child_node = ParentNode("span", [grandchild_node], {"id": "spanId", "class": "niceClass"})
        parent_node = ParentNode("div", [child_node], {"id": "someId"})
        self.assertEqual(
            parent_node.to_html(),
            '<div id="someId"><span id="spanId" class="niceClass"><a href="https://www.google.com">Click me!</a></span></div>',
    )