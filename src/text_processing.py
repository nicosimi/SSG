from textnode import TextNode
from textnode import TextType
from leafnode import LeafNode
import re ##importing regex module

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

def split_nodes_delimiter_textnode_transformer(sections_list, delimiter, text_type: TextType):
    res = []
    for i in range(len(sections_list)):
        if i%2 == 0:
            res.append(TextNode(sections_list[i], TextType.TEXT))
        else:
            match delimiter:
                case "**":
                    res.append(TextNode(sections_list[i], text_type))
                case "_":
                    res.append(TextNode(sections_list[i], text_type))
                case "`":
                    res.append(TextNode(sections_list[i], text_type))
    return res


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    if len(old_nodes) < 1: return new_nodes
    for node in old_nodes:
        text = node.get_text()
        if (text.count(delimiter) % 2 != 0): raise ValueError("delimiter is not closed")
        sections = text.split(delimiter)
        sections_nodes = split_nodes_delimiter_textnode_transformer(sections, delimiter, text_type)
        new_nodes.extend(sections_nodes)
    return new_nodes

def extract_markdown_images(text: str):
    matches = re.findall(r"!\[\w.*?\]\(\w.*?\)",text)
    res = []
    for match in matches:
        aux = match.split("]")
        aux[0] = aux[0].strip("!").strip("[")
        aux[1] = aux[1].strip("(").strip(")")
        aux_tuple = tuple(aux)
        res.append(aux_tuple)
        
    return res

def extract_markdown_links(text:str):
    matches = re.findall(r"\[\w.*?\]\(\w.*?\)", text)
    res = []
    for match in matches:
        aux = match.split("]")
        aux[0] = aux[0].strip(("["))
        aux[1] = aux[1].strip("(").strip(")")
        aux_tuple=(tuple(aux))
        res.append(aux_tuple)
    return res
