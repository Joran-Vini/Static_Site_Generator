from enum import Enum


class BlockType(Enum):
    PARAGRAPH = 'paragraph'
    HEADING = 'heading'
    CODE = 'code'
    QUOTE = 'quote'
    ULIST = 'unordered_list'
    OLIST = 'ordered_list'

def block_to_block_type(block):
    if block.startswith('#'):
        return BlockType.HEADING 
    if block.startswith('```') and block.endswith('```'):
        return BlockType.CODE
    if block.startswith('>'):
        return BlockType.QUOTE
    if block.startswith('- '):
        return BlockType.ULIST
    lines = block.split("\n")
    if all(line.lstrip().startswith("1.") or line.lstrip()[0].isdigit() and line.lstrip()[1:3] == ". "
       for line in lines):
        return BlockType.OLIST
    return BlockType.PARAGRAPH
