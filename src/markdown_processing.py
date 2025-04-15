from enum import Enum
import re

from htmlnode import HTMLNode
from leafnode import LeafNode
from parentnode import ParentNode
from text_processing import text_node_to_child_node, text_to_textnodes, text_node_to_html_node
from textnode import TextNode, TextType

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "list_unordered"
    ORDERED_LIST = "list_ordered"

def markdown_to_blocks(md:str)->list[str]:
    if md is None: return []
    if len(md) < 1: return []
    sections = md.strip("\n").split("\n\n")
    sections = list(
        filter(lambda x: len(x) > 0, sections)
    )
    return sections

def is_blocktype(lines:list[str], regex:str, ordered:bool) ->bool:
    pattern = re.compile(regex)
    if ordered:
        i = 1
        for line in lines:
            if not pattern.match(line): return False
            if int(line[0]) != i: return False
            i+=1
    else:
        for line in lines:
            if not pattern.match(line): return False
    return True

def block_to_blocktype(block:str)->BlockType:
    pattern = re.compile(r"^\#{1,6}")
    if pattern.match(block):
        return BlockType.HEADING
    pattern = re.compile(r"\`{3}")
    if pattern.match(block) and pattern.match(block,(len(block)-3)):
        return BlockType.CODE
    lines = block.split(r"\n")
    if is_blocktype(lines, r"^\>", False):
        return BlockType.QUOTE
    if is_blocktype(lines, r"^\- ", False):
        return BlockType.UNORDERED_LIST
    if is_blocktype(lines, r"^\d\. ", True):
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH

def code_block_processing(block: str, children:list[HTMLNode]):
    node = TextNode(block,TextType.TEXT)
    wrapper_list = [text_node_to_html_node(node)]
    wrapper_node = ParentNode("pre", wrapper_list)
    children.append(text_node_to_html_node(wrapper_node))
    return None

def simple_block_processing(block:str, children:list[HTMLNode]):    
    text_nodes = text_to_textnodes(block)
    for node in text_nodes:
        children.append(text_node_to_child_node(node))    
    return None

def list_block_processing(block:str, children:list[HTMLNode]):
    lines = block.split("\n")
    for line in lines:
        wrapper_list = []
        pieces = text_to_textnodes(line)
        for piece in pieces:
            wrapper_list.append(text_node_to_child_node(piece))
            wrapper_node = ParentNode("li", wrapper_list)
            children.append(wrapper_node)
    return None

def block_to_parent_node(block:str, block_type:BlockType)->ParentNode:    #create html node, assign children to parent
    children = []
    tag = ""
    match block_type:
        case BlockType.CODE:
            tag = "code"
            code_block_processing(block, children)
        case BlockType.PARAGRAPH | BlockType.HEADING | BlockType.QUOTE:
            if block_type is BlockType.PARAGRAPH: tag = "p"
            if block_type is BlockType.QUOTE: tag = "blockquote"
            if block_type is BlockType.HEADING:
                hashtag = block.split(" ")[0]
                tag = "h" + str(hashtag.count("#"))
            simple_block_processing(block, children)
        case BlockType.UNORDERED_LIST | BlockType.ORDERED_LIST:
            if block_type is BlockType.UNORDERED_LIST: tag = "ul"
            else: tag = "ol"
            list_block_processing(block, children)
    return ParentNode(tag,children)

def markdown_to_html_node(doc:str)-> ParentNode:
    blocks = markdown_to_blocks(doc)
    parents = []
    for block in blocks:
        block_type = block_to_blocktype(block)
        parent_node = block_to_parent_node(block, block_type)
        parents.append(parent_node)
    return ParentNode("div",parents)
