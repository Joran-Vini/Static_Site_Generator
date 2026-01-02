from htmlnode import LeafNode, ParentNode
from textnode import TextNode, TextType, text_node_to_html_node
from extract_markdown import markdown_to_blocks
from block import block_to_block_type, BlockType
from split_nodes import text_to_textnodes


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        block_type = block_to_block_type(block)
        html_node = block_to_html_node(block, block_type)
        children.append(html_node)
    return ParentNode('div', children)

def block_to_html_node(block, block_type):
    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)
    if block_type == BlockType.HEADING:
        return heading_to_html_node(block)
    if block_type == BlockType.CODE:
        return code_to_html_node(block)
    if block_type == BlockType.QUOTE:
        return quote_to_html_node(block)
    if block_type == BlockType.ULIST:
        return unordered_list_to_html_node(block)
    if block_type == BlockType.OLIST:
        return ordered_list_to_html_node(block)
    raise ValueError("Invalid block type")


def paragraph_to_html_node(block):
    lines = block.split("\n")
    clean_lines = [line.strip() for line in lines if line.strip() != ""]
    text = " ".join(clean_lines)
    text_node = text_to_textnodes(text)
    html_node = []
    for tn in text_node:
        html_node.append(text_node_to_html_node(tn))
    return ParentNode('p', html_node)

def heading_to_html_node(block):
    level = 0
    for ch in block:
        if ch == '#':
            level += 1
        else:
            break
        
    if level < 1 or level > 6:
        raise ValueError("Heading level must be between 1 and 6")
    text = block[level + 1:].strip()
    children = []

    for tn in text_to_textnodes(text):
        children.append(text_node_to_html_node(tn))
    
    return ParentNode(f'h{level}', children)

def code_to_html_node(block):
    if not block.startswith('```') or not block.endswith('```'):
        raise ValueError("Code block must start and end with triple backticks")
    lines = block.split('\n')
    inner_lines = lines[1:-1]
    cleaned_lines = [line.lstrip(' ') for line in inner_lines]
    text = "\n".join(cleaned_lines) + '\n'
    raw_text_node = TextNode(text, TextType.TEXT)
    child = text_node_to_html_node(raw_text_node)
    code_node = ParentNode("code", [child])
    return ParentNode("pre", [code_node])

def quote_to_html_node(block):
    lines = block.split('\n')
    cleaned_lines = []

    for line in lines:
        if line.startswith('>'):
            value = line[1:].lstrip()
            cleaned_lines.append(value)
        else:
            raise ValueError("Each line in a quote block must start with '>'")

    text = " ".join(cleaned_lines)
    children = []
    for tn in text_to_textnodes(text):
        children.append(text_node_to_html_node(tn))
    return ParentNode("blockquote", children)

def unordered_list_to_html_node(block):
    lines = block.split('\n')
    items = []
    for line in lines:
        if not line.startswith('- '):
            raise ValueError("Each line in an unordered list must start with '- '")
        text = line[2:].strip()
        children = [text_node_to_html_node(tn) for tn in text_to_textnodes(text)]
        items.append(ParentNode('li', children))

    return ParentNode('ul', items)

def ordered_list_to_html_node(block):
    lines = block.split('\n')
    items = []
    i = 1
    for line in lines:
        prefix = f"{i}. "
        if not line.startswith(prefix):
            raise ValueError("Each line in an ordered list must start with its number followed by '. '")
        text = line[len(prefix):].strip()
        children = [text_node_to_html_node(tn) for tn in text_to_textnodes(text)]
        items.append(ParentNode('li', children))
        i += 1
    return ParentNode('ol', items)