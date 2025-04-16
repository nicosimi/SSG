import unittest
from textnode import TextNode
from textnode import TextType
from text_processing import split_nodes_image, extract_markdown_images, extract_markdown_links, split_nodes_link, text_node_to_html_node, split_nodes_delimiter
from text_processing import text_to_textnodes

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
        props = {"src":"https://www.google.com"}
        src = "https://www.google.com"
        node = TextNode("This is a text node", TextType.IMAGE_TEXT,src)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node.props,props)


    def test_text_to_textnode(self):
        test_text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(test_text)
        #print(nodes)
        self.assertListEqual( [
        TextNode("This is ", TextType.TEXT),
        TextNode("text", TextType.BOLD_TEXT),
        TextNode(" with an ", TextType.TEXT),
        TextNode("italic", TextType.ITALIC_TEXT),
        TextNode(" word and a ", TextType.TEXT),
        TextNode("code block", TextType.CODE_TEXT),
        TextNode(" and an ", TextType.TEXT),
        TextNode("obi wan image", TextType.IMAGE_TEXT, "https://i.imgur.com/fJRm4Vk.jpeg"),
        TextNode(" and a ", TextType.TEXT),
        TextNode("link", TextType.LINK_TEXT, "https://boot.dev"),
        ],nodes)
    
    def test_text_to_textnode_reverse_order(self):
        test_text = "[link](https://boot.dev)This is ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) with an `code block` word and a _italic_ and an  and a **text**"
        nodes = text_to_textnodes(test_text)
        #print(nodes)
        self.assertListEqual( [
        TextNode("link", TextType.LINK_TEXT, "https://boot.dev"),
        TextNode("This is ", TextType.TEXT),
        TextNode("obi wan image", TextType.IMAGE_TEXT, "https://i.imgur.com/fJRm4Vk.jpeg"),
        TextNode(" with an ", TextType.TEXT),
        TextNode("code block", TextType.CODE_TEXT),
        TextNode(" word and a ", TextType.TEXT),
        TextNode("italic", TextType.ITALIC_TEXT),
        TextNode(" and an  and a ", TextType.TEXT),
        TextNode("text", TextType.BOLD_TEXT),
        ],nodes)

    def test_text_to_textnode_empty_text(self):
        test_text = "This a text for testing"
        nodes = text_to_textnodes(test_text)
        self.assertListEqual([
            TextNode("This a text for testing", TextType.TEXT),
        ], nodes)

    def test_text_to_textnode_empty_text(self):
        test_text = ""
        nodes = text_to_textnodes(test_text)
        self.assertListEqual([], nodes)
    
    def test_text_to_textnode_null(self):
        test_text = None
        nodes = text_to_textnodes(test_text)
        self.assertListEqual([], nodes)

class Test_split_functions(unittest.TestCase):
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

    def test_split_images(self):
        node = TextNode(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
           TextType.TEXT,
        )   
        new_nodes = split_nodes_image([node])
        #print(new_nodes)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE_TEXT, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE_TEXT, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_images_adjacent_images(self):
        node = TextNode(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)![second image](https://i.imgur.com/3elNhQu.png)",
        TextType.TEXT)
        new_nodes = split_nodes_image([node])

        test_list = [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE_TEXT, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode("second image", TextType.IMAGE_TEXT, "https://i.imgur.com/3elNhQu.png")
        ]
        self.assertListEqual(test_list, new_nodes)

    def test_split_links(self):
        node = TextNode(
        "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
        TextType.TEXT,
        )   
        new_nodes = split_nodes_link([node])
        self.assertListEqual([
        TextNode("This is text with a link ", TextType.TEXT),
        TextNode("to boot dev", TextType.LINK_TEXT, "https://www.boot.dev"),
        TextNode(" and ", TextType.TEXT),
        TextNode(
        "to youtube", TextType.LINK_TEXT, "https://www.youtube.com/@bootdotdev"
            ),
            ],
            new_nodes
        )
    
    def test_split_links_adjacent_links(self):
        node = TextNode(
        "This is text with a link [to boot dev](https://www.boot.dev)[to youtube](https://www.youtube.com/@bootdotdev)",
        TextType.TEXT,
        )   
        new_nodes = split_nodes_link([node])
        self.assertListEqual([
        TextNode("This is text with a link ", TextType.TEXT),
        TextNode("to boot dev", TextType.LINK_TEXT, "https://www.boot.dev"),
        TextNode("to youtube", TextType.LINK_TEXT, "https://www.youtube.com/@bootdotdev")
        ],new_nodes)

    def test_split_links_plain_text(self):
        node = TextNode(
        "This is text",
        TextType.TEXT,
        )   
        new_nodes = split_nodes_link([node])
        self.assertListEqual([
        TextNode("This is text", TextType.TEXT),
        ],new_nodes)
    
    def test_split_links_empty_text(self):
        node = TextNode(
        "",
        TextType.TEXT,
        )   
        new_nodes = split_nodes_link([node])
        self.assertListEqual([
        ],new_nodes)

    def test_split_links_null_list(self):
        new_nodes = split_nodes_link(None)
        self.assertListEqual([
        ],new_nodes)

    def test_split_links_list_null_nodes(self):
        new_nodes = split_nodes_link([None])
        self.assertListEqual( []
        , new_nodes)
