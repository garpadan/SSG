import re
from enum import Enum
from htmlnode import HTMLNode, ParentNode
from text_to_textnodes import *
from text_to_html import *

def markdown_to_blocks(markdown):
    lines = markdown.split("\n\n")
    filtered = []

    for line in lines:
        cleaned_line = line.strip()

        if cleaned_line != "":
            filtered.append(cleaned_line)
   
    return filtered


class BlockType(Enum):
    PARAG = "paragraph"
    HEAD = "heading"
    CODE = "code"
    QUOTE = "quote"
    UL = "unordered_list"
    OL = "ordered_list"


def block_to_block_type(markdown):
    # Head block
    if re.findall(r"^#{1,6} ", markdown):
        return BlockType.HEAD
    
    # Code block
    if markdown.startswith("```") and markdown.endswith("```"):
        return BlockType.CODE

    lines = markdown.split("\n")

    # Quote block
    if markdown.startswith(">"):
        is_quote =  True
        for line in lines:
            if not line.startswith(">"):
                is_quote = False
                break
        if is_quote:
            return BlockType.QUOTE

    # Unordered List
    if markdown.startswith("- "):
        is_unordered =  True
        for line in lines:
            if not line.startswith("- "):
                is_unordered = False
                break
        if is_unordered:
            return BlockType.UL
        
    # Ordered List
    if markdown.startswith("1. "):
        is_ordered =  True
        current_index = 1
        for line in lines:
            if not line.startswith(f"{current_index}. "):
                is_ordered = False
                break
            current_index += 1
        if is_ordered:
            return BlockType.OL
        
    return BlockType.PARAG


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        block_type = block_to_block_type(block)
        html_node = block_to_html_node(block, block_type)
        children.append(html_node)
    
    return ParentNode("div", children)


def block_to_html_node(block, block_type):
    if block_type == BlockType.PARAG:
        return create_paragraph_node(block)
    if block_type == BlockType.HEAD:
        return create_heading_node(block)
    if block_type == BlockType.CODE:
        return create_code_node(block)
    if block_type == BlockType.QUOTE:
        return create_quote_node(block)
    if block_type == BlockType.UL:
        return create_ul_node(block)
    if block_type == BlockType.OL:
        return create_ol_node(block)            
    raise ValueError("Invalid block type")


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []

    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children


# Helper functions for specifc block types
def create_paragraph_node(block):
    lines = block.split("\n")
    cleaned_lines = []

    for line in lines:
        new_line = line.strip()
        cleaned_lines.append(new_line)

    paragraph = " ".join(cleaned_lines)
    children = text_to_children(paragraph)

    return ParentNode("p", children)


def create_heading_node(block):
    level = 0

    for char in block:
        if char == "#":
            level += 1
        else:
            break    
    
    text = block[level + 1:]
    children = text_to_children(text)

    return ParentNode(f"h{level}", children)


def create_code_node(block):
    # Do not strip() the whole block, or you risk losing leading 
    # indentation on the first line of code.
    lines = block.split("\n")
    
    if len(lines) < 2:
        return ParentNode("pre", [text_node_to_html_node(TextNode("", TextType.CODE))])

    # Slice out the first line (```) and the last line (```)
    content_lines = lines[1:-1]
    
    # Join the remaining lines back together
    content = "\n".join(content_lines)
    
    # Based on your 'expected' string, you need a trailing newline
    content = content + "\n"

    # Convert to the LeafNode (code tag)
    node = text_node_to_html_node(TextNode(content, TextType.CODE))
    
    # Wrap in the pre tag
    return ParentNode("pre", [node])


def create_quote_node(block):
    lines = block.split("\n")
    new_lines = []

    for line in lines:
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)

    return ParentNode("blockquote", children)


def create_ul_node(block):
    lines = block.split("\n")
    list_items = []

    for line in lines:
        text = line[2:]
        list_items.append(ParentNode("li", text_to_children(text)))

    return ParentNode("ul", list_items)
    

def create_ol_node(block):
    lines = block.split("\n")
    list_items = []

    for line in lines:
        # remove "1. "
        index = line.find(" ")
        text = line[index + 1:]
        list_items.append(ParentNode("li", text_to_children(text)))

    return ParentNode("ol", list_items)