import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode()
        node2 = HTMLNode()
        self.assertEqual(node,node2)
    
    def test_eq1(self):
        node = HTMLNode("p")
        node2 = HTMLNode("s")
        self.assertNotEqual(node,node2)
    
    def test_eq2(self):
        node = HTMLNode(None,"sd")
        node2 = HTMLNode(None, "qq")
        self.assertNotEqual(node,node2)
    
    def test_eq3(self):
        node = HTMLNode(None, None, "qwqe")
        node2 = HTMLNode(None, None, "WWWW")
        self.assertNotEqual(node,node2)
    
    def test_eq4(self):
        node = HTMLNode(None,None,None,"wwww")
        node2 = HTMLNode(None, None, None, "qqq")
        self.assertNotEqual(node,node2)
    
    def test_repr_full(self):
        node = HTMLNode("tag","value",["ss"],{"a":"s"})
        text = f"HTMLNode({node.tag}, {node.value}, {node.children}, {node.props})"
        self.assertEqual(node.__repr__(),text)
    
    def test_repr_null(self):
        node = HTMLNode()
        text = f"HTMLNode(None, None, None, None)"
        self.assertEqual(node.__repr__(),text)
    
    def test_props_to_html(self):
        testprops = {
            "href": "https://www.google.com",
            "target": "_blank",
        }
        node = HTMLNode(None,None,None,testprops)
        testtext = """href="https://www.google.com" target="_blank\""""
        self.assertEqual(node.props_to_html(), testtext)

    def test_props_to_html_null(self):
        testtext = ""
        node = HTMLNode(None, None, None, None)
        self.assertEqual(testtext, node.props_to_html())
    
    def test_props_to_html_empty_dict(self):
        testtext = ""
        node = HTMLNode(None,None,None,{})
        self.assertEqual(testtext,node.props_to_html())
