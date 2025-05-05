from textnode import *
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes
    
def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if (node.text_type != TextType.TEXT):
            new_nodes.append(node)
            continue
        matches = extract_markdown_images(node.text)
        remaining_text = node.text
        for alt,url in matches:
            sections = remaining_text.split(f"![{alt}]({url})", 1)
            if (sections[0] != ""):
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            remaining_text = sections[1]
            new_nodes.append(TextNode(alt, TextType.IMAGE, url))
        # last section
        if (remaining_text != ""):
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if (node.text_type != TextType.TEXT):
            new_nodes.append(node)
            continue
        matches = extract_markdown_links(node.text)
        remaining_text = node.text
        for anchor,url in matches:
            sections = remaining_text.split(f"[{anchor}]({url})", 1)
            if (sections[0] != ""):
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            remaining_text = sections[1]
            new_nodes.append(TextNode(anchor, TextType.LINK, url))
        if (remaining_text != ""):
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    return new_nodes
            
def text_to_textnodes(text):
    split_nodes = [TextNode(text, TextType.TEXT)]
    split_nodes = split_nodes_delimiter(split_nodes, "`", TextType.CODE)
    split_nodes = split_nodes_delimiter(split_nodes, "**", TextType.BOLD)
    split_nodes = split_nodes_delimiter(split_nodes, "_", TextType.ITALIC)
    split_nodes = split_nodes_image(split_nodes)
    split_nodes = split_nodes_link(split_nodes)
    return split_nodes