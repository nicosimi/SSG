from textnode import TextNode
from textnode import TextType
from leafnode import LeafNode

def text_node_to_html_node(text_node:TextNode):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None,text_node.text)
        case TextType.BOLD_TEXT:
            return LeafNode("b",text_node.text)
        case TextType.ITALIC_TEXT:
            return LeafNode("i", text_node.text)
        case TextType.CODE_TEXT:
            return LeafNode("code",text_node.text)
        case TextType.LINK_TEXT:
            if text_node.url is None:
                raise ValueError("url can`t be null")
            props = {
                "href":text_node.url
            }
            return LeafNode("a",text_node.text,props)
        case TextType.IMAGE_TEXT:
            if text_node.src is None:
                raise ValueError("image url can`t be null")
            props = {}
            props["src"] = text_node.src
            props["alt"] = text_node.text
            return LeafNode("img", "",props)
        case _:
            raise ValueError("invalid text type")
