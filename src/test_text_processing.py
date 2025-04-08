import unittest
from textnode import TextNode
from textnode import TextType
from text_processing import extract_markdown_images,extract_markdown_links, text_node_to_html_node, split_nodes_delimiter

class TestText_Processing(unittest.TestCase):
    def test_plain_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
    
    def test_bold_text(self):
        node = TextNode("This is a text node", TextType.BOLD_TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a text node")
    
    def test_italic_text(self):
        node = TextNode("This is a text node", TextType.ITALIC_TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is a text node")
    
    def test_code_text(self):
        node = TextNode("This is a text node", TextType.CODE_TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a text node")
    
    def test_link_text(self):
        props = {"href":"https://www.google.com"}
        url = "https://www.google.com"
        node = TextNode("This is a text node", TextType.LINK_TEXT,url)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node.props,props)
        self.assertEqual(html_node.to_html(),"<a href=\"https://www.google.com\">This is a text node</a>" )
    
    def test_image_text(self):
        props = {"src":"https://www.google.com", "alt":"This is a text node"}
        src = "https://www.google.com"
        node = TextNode("This is a text node", TextType.IMAGE_TEXT,"This is a text node",src)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props,props)

    def test_split_nodes_delimiter(self):
        test_node = TextNode("This is text with a **bolded phrase** in the middle ",TextType.TEXT)
        new_nodes = split_nodes_delimiter([test_node],"**", TextType.BOLD_TEXT)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[0].text, "This is text with a ")
        self.assertEqual(new_nodes[1].text_type, TextType.BOLD_TEXT)
        self.assertEqual(new_nodes[1].text, "bolded phrase")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[2].text, " in the middle ")

    def test_extract_images_links(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        #print(extract_markdown_images(text))
        #[("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        self.assertEqual(extract_markdown_images(text),[("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")])

    def test_extract_links_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        #print(extract_markdown_links(text))
        #[("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
        self.assertListEqual(extract_markdown_links(text),[("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")])
