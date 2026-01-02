from textnode import TextNode, TextType
from extract_markdown import extract_markdown_images, extract_markdown_links

def text_to_textnodes(text):
    textNode = TextNode(text, TextType.TEXT)
    textNode = split_nodes_delimiter([textNode], '**', TextType.BOLD)
    textNode = split_nodes_delimiter(textNode, '*', TextType.ITALIC)
    textNode = split_nodes_delimiter(textNode, "_", TextType.ITALIC)
    textNode = split_nodes_delimiter(textNode, '`', TextType.CODE)
    textNode = split_nodes_image(textNode)
    textNode = split_nodes_link(textNode)
    return textNode


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        parts = node.text.split(delimiter)

        if len(parts) % 2 == 0:
            raise Exception("Invalid markdown, missing closing delimiter")
        
        for i, part in enumerate(parts):
            if part == '':
                continue

            if i % 2 == 0:
                new_nodes.append(TextNode(part, TextType.TEXT))
            else:
                new_nodes.append(TextNode(part, text_type))
        
    return new_nodes    

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        original_text = node.text
        parts = extract_markdown_images(node.text)

        if len(parts) == 0:
            new_nodes.append(node)
            continue
        
        for alt, url in parts:
            sections = original_text.split(f"![{alt}]({url})", 1)
            if sections[0]:
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(alt, TextType.IMAGE, url))
            original_text = sections[1]
        if original_text:
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        original_text = node.text
        parts = extract_markdown_links(node.text)

        if len(parts) == 0:
            new_nodes.append(node)
            continue
        
        for alt, url in parts:
            sections = original_text.split(f"[{alt}]({url})", 1)
            if sections[0]:
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(alt, TextType.LINK, url))
            original_text = sections[1]
        if original_text:
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes
