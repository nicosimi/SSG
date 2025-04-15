import unittest

from leafnode import LeafNode

class TestLeafnode(unittest.TestCase):
    def test_creation(self):
        node = LeafNode()
        self.assertIsInstance(node,LeafNode)

    def test_creation_children_none(self):
        node = LeafNode()
        self.assertEqual(node.children, None)

    def test_repr(self):
        node = LeafNode("a","sss", {"src":"url/of/image.jpg"})
        self.assertEqual(node.__repr__(), "LeafNode(a, sss, None, {\'src\': \'url/of/image.jpg\'})")

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_blockquote(self):
        node = LeafNode("blockquote", "Hello, world!")
        self.assertEqual(node.to_html(), "<blockquote>Hello, world!</blockquote>") 

    def test_leaf_to_html_img(self):
        node = LeafNode("img", "Description of image",{"src":"url/of/image.jpg"})
        self.assertEqual(node.to_html(), "<img src=\"url/of/image.jpg\" alt=\"Description of image\" />")

    def test_leaf_to_html_a(self):
        node = LeafNode("a","Hello, world!",{"href":"https://www.google.com"})
        self.assertEqual(node.to_html(),"<a href=\"https://www.google.com\">Hello, world!</a>")

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None,"Hello, world!",None)
        self.assertEqual(node.to_html(), "Hello, world!")
    
    def test_leaf_to_html_empty_node(self):
        node = LeafNode()
        self.assertRaises(ValueError,node.to_html)
