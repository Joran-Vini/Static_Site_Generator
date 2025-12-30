from enum import Enum


class BlockType(Enum):
    PARAGRAPH = 'paragraph'
    HEADING = 'heading'
    CODE = 'code'
    QUOTE = 'quote'
    UNORDERED_LIST = 'unordered_list'
    ORDERED_LIST = 'ordered_list'

def block_to_block_type(block):
    if block.startswith('# '):
        return BlockType.HEADING 
    if block.startswith('```') and block.endswith('```'):
        return BlockType.CODE
    if block.startswith('>'):
        return BlockType.QUOTE
    if block.startswith('- '):
        return BlockType.UNORDERED_LIST
    if block[0:2].isdigit() and block[2:4] == '. ':
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH
