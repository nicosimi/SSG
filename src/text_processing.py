from textnode import TextNode
from textnode import TextType
from leafnode import LeafNode
import re ##importing regex module

def text_node_to_html_node(text_node:TextNode):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None,text_node.get_text())
        case TextType.BOLD_TEXT:
            return LeafNode("b",text_node.get_text())
        case TextType.ITALIC_TEXT:
            return LeafNode("i", text_node.get_text())
        case TextType.CODE_TEXT:
            return LeafNode("code",text_node.get_text())
        case TextType.LINK_TEXT:
            url = text_node.get_url()
            if url is None:
                raise ValueError("url can`t be null")
            props = {
                "href":url
            }
            return LeafNode("a",text_node.get_text() ,props)
        case TextType.IMAGE_TEXT:
            url = text_node.get_url()
            if url is None:
                raise ValueError("image url can`t be null")
            props = {"src":url}
            return LeafNode("img", text_node.get_text() ,props)
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


def split_nodes_delimiter(old_nodes:list[TextNode], delimiter, text_type:TextType):
    new_nodes = []
    if len(old_nodes) < 1: return new_nodes
    for node in old_nodes:
        if node.get_text() is None: continue
        if node.get_text_type() is not TextType.TEXT:
            new_nodes.append(node)
            continue
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

def split_nodes_image(nodes: list[TextNode]):
    res = []
    if nodes is None: return res
    if len(nodes) < 1: return res
    for text_node in nodes:
        if text_node is None: continue
        if text_node.get_text_type() is not TextType.TEXT:
            res.append(text_node)
            continue
        text = text_node.get_text()
        image_links = extract_markdown_images(text)
        for aux_link_tuple in image_links:
            text_sections = text.split(f"![{aux_link_tuple[0]}]({aux_link_tuple[1]})",1)
            if len(text_sections[0])>0: res.append(TextNode(text_sections[0],TextType.TEXT))
            res.append(TextNode(aux_link_tuple[0],TextType.IMAGE_TEXT,aux_link_tuple[1]))
            text = text_sections[1]
        if len(text) > 0: res.append(TextNode(text, TextType.TEXT))
    return res

def split_nodes_link(nodes: list[TextNode]):
    res = []
    if nodes is None: return res
    if len(nodes) < 1: return res
    for text_node in nodes:
        if text_node is None: continue
        if text_node.get_text_type() is not TextType.TEXT:
            res.append(text_node)
            continue 
        text = text_node.get_text()
        image_links = extract_markdown_links(text)
        for aux_link_tuple in image_links:
            text_sections = text.split(f"[{aux_link_tuple[0]}]({aux_link_tuple[1]})",1)
            if len(text_sections[0]) > 0: res.append(TextNode(text_sections[0],TextType.TEXT))
            res.append(TextNode(aux_link_tuple[0],TextType.LINK_TEXT,aux_link_tuple[1]))
            text = text_sections[1]
        if len(text) > 0: res.append(TextNode(text, TextType.TEXT))
    return res

def text_to_textnodes(text: str)->list[TextNode]:
    base_node = TextNode(text,TextType.TEXT)
    text_node_list = split_nodes_delimiter([base_node],"**", TextType.BOLD_TEXT)
    text_node_list = split_nodes_delimiter(text_node_list,"_", TextType.ITALIC_TEXT)
    text_node_list = split_nodes_delimiter(text_node_list,"`", TextType.CODE_TEXT)
    text_node_list = split_nodes_image(text_node_list)
    text_node_list = split_nodes_link(text_node_list)
    return text_node_list

def text_node_to_child_node(node: TextNode)->LeafNode:
    text = node.get_text()
    match node.get_text_type():
        case TextType.LINK_TEXT:
            tag = "a"
            props = {"href":node.get_url()}
        case TextType.IMAGE_TEXT:
            tag = "img"
            props = {"src":node.get_url()}
        case TextType.CODE_TEXT:
            tag = "code"
            props = None
        case TextType.BOLD_TEXT:
            tag = "b"
            props = None
        case TextType.ITALIC_TEXT:
            tag = "i"
            props = None
        case TextType.TEXT:
            tag = None
            props = None
    return LeafNode(tag, text, props)
