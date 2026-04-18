import unittest
from markdown_blocks import *
from inline_markdown import *
from htmlnode import *
from textnode import *
from markdown_to_html import *

def markdown_to_html_node(md):
    mother = ParentNode("div", [])
    #mother is the final parent node, all blocks are her children
    # md is the document
    # we want to split the md into blocks, we have code for that
    blocks = markdown_to_blocks(md)
    # this means blocks equals a list of blocks
    # only split along double newlines, nothing special elsewise
    # operate on each block, for loop
    for block in blocks:
    # we need to determine the TYPE of block, we have a function
        bt = block_to_blocktype(block)
        # block didn't change, we just got new data, to use for formatting
        # based on bt we create a new HTMLNode, this may be parent, it may be Leaf
        # if it is leaf, it is actually got a parent for <pre> format, let's do that first
        if bt == BlockType.CODE:
            block = block[3:-3]
            b_node = ParentNode("pre", [LeafNode("code", block)])
            mother.children.append(b_node)
        # BLOCK STILL HAS NUMBER OF #'s in it
        if bt == BlockType.UNORDERED_LIST:
            mother.children.append(unordered_list_block_behavior(block))
        if bt == BlockType.ORDERED_LIST:
            mother.children.append(ordered_list_block_behavior(block))
        if bt == BlockType.HEADING:
            mother.children.append(heading_block_behavior(block))
        if bt == BlockType.QUOTE:
            mother.children.append(quote_block_behavior(block))
        if bt == BlockType.PARAGRAPH:
            mother.children.append(paragraph_block_behavior(block))
    
    return mother


def unordered_list_block_behavior(block):
    parent = ParentNode("ul", [])
    lines = block.split("\n")
    for line in lines:
        nodes = text_to_textnodes(line[2:])
        new = []
        for node in nodes:

            new.append(text_node_to_html_node(node))
        uncle = ParentNode("li", new)
        parent.children.append(uncle)
    return parent

def ordered_list_block_behavior(block):
    parent = ParentNode("ol", [])
    lines = block.split("\n")
    for line in lines:
        nodes = text_to_textnodes(line[3:])
        new = []
        for node in nodes:

            new.append(text_node_to_html_node(node))
        uncle = ParentNode("li", new)
        parent.children.append(uncle)
    return parent

def heading_block_behavior(block):
    heading_num = block[0:6].count("#")
    parent = ParentNode(f"h{heading_num}", [])
    text = block[heading_num + 1:]
    nodes = text_to_textnodes(text)
    new = []
    for node in nodes:

        new.append(text_node_to_html_node(node))
    parent.children = new
    return parent

def quote_block_behavior(block):
    parent = ParentNode("blockquote", [])
    block = block.splitlines(keepends=True)
    clean = ""
    for line in block:
        
        clean += line.strip("> ")
    block = "\n".join(block)
    
    text = clean
    nodes = text_to_textnodes(text)
    new = []
    for node in nodes:

        new.append(text_node_to_html_node(node))
    parent.children = new
    return parent

def paragraph_block_behavior(block):
    parent = ParentNode("p", [])
    nodes = text_to_textnodes(block)
    new = []
    for node in nodes:
        new.append(text_node_to_html_node(node))
    parent.children = new
    return parent