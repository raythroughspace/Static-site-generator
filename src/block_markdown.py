from enum import Enum
from inline_markdown import *
from textnode import *
from htmlnode import *
import re


class BlockType(Enum):
    PARAGRAPH = "Paragraph"
    HEADING = "Heading"
    CODE = "Code"
    QUOTE = "Quote"
    ULIST = "Unordered_list"
    OLIST = "Ordered_list"

def markdown_to_blocks(markdown):
    lst = markdown.split("\n\n")
    for i in range(len(lst)):
        lst[i] = lst[i].strip()
    return [block for block in lst if block != ""]

def block_to_block_type(block):
    if re.match(r"#(#?){5} \w*", block):
        return BlockType.HEADING
    if re.match(r"```(\n|.)*```", block):
        return BlockType.CODE
    if re.match(r"(>.*\n)+", block):
        return BlockType.QUOTE
    if re.match(r"(- .*)+", block):
        return BlockType.ULIST
    
    lines = block.split("\n")
    is_ordered_list = True
    for i in range(len(lines)):
        if (not lines[i].startswith(f"{i+1}. ")):
            is_ordered_list = False
    if (is_ordered_list):
        return BlockType.OLIST
    return BlockType.PARAGRAPH

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    html_nodes = []
    for block in blocks:
        match block_to_block_type(block):
            case BlockType.HEADING:
                html_nodes.append(heading_to_html(block))
            case BlockType.CODE:
                html_nodes.append(code_to_html(block))
            case BlockType.QUOTE:
                html_nodes.append(quote_to_html(block))
            case BlockType.ULIST:
                html_nodes.append(ulist_to_html(block))
            case BlockType.OLIST:
                html_nodes.append(olist_to_html(block))
            case BlockType.PARAGRAPH:
                html_nodes.append(paragraph_to_html(block))
    return ParentNode("div", html_nodes)

def text_to_children(text):
    return list(map(text_node_to_html_node, text_to_textnodes(text)))

def heading_to_html(block):
    nhashtags = len(re.findall(r"(#+)", block)[0])
    return ParentNode(f"h{nhashtags}", text_to_children(block.strip("#").strip()))

def quote_to_html(block):
    lines = block.split("\n")
    new_lines = [line.strip(">").strip() for line in lines]
    return ParentNode("blockquote", text_to_children(" ".join(new_lines)))

def ulist_to_html(block):
    lines = block.split("\n")
    children = [ParentNode("li", text_to_children(line[2:])) for line in lines]
    return ParentNode("ul", children)

def olist_to_html(block):
    lines = block.split("\n")
    children = [ParentNode("li", text_to_children(line[3:])) for line in lines]
    return ParentNode("ol", children)

def code_to_html(block):
    text = block[4:-3]
    raw_text_node = TextNode(text, TextType.TEXT)
    child = text_node_to_html_node(raw_text_node)
    code = ParentNode("code", [child])
    return ParentNode("pre", [code])

def paragraph_to_html(block):
    lines = block.split("\n")
    children = text_to_children(" ".join(lines))
    return ParentNode("p", children)