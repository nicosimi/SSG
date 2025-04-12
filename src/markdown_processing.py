from enum import Enum
import re

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
    pattern = re.Pattern(regex)
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
    pattern = re.Pattern("^\#{1,6}")
    if pattern.match(block):
        return BlockType.HEADING
    pattern = re.Pattern("\`{3}")
    if pattern.match(block) and pattern.match(block,(len(block)-3)):
        return BlockType.CODE
    lines = block.split("\n")
    if is_blocktype(lines, "^\>", False):
        return BlockType.QUOTE
    if is_blocktype(lines, "^\- ", False):
        return BlockType.UNORDERED_LIST
    if is_blocktype(lines, "^\d\. ", True):
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH
    