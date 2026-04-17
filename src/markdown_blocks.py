from enum import Enum


def markdown_to_blocks(markdown):
    if not isinstance(markdown, str):
        raise TypeError("markdown_to_blocks takes a str input")
    list_of_blocks = markdown.split("\n\n")
    # need to adjust for trailing lines, AND early lines
    clean_list = []
    for block in list_of_blocks:
        block = block.strip()
        if block != "":
            clean_list.append(block)

    return clean_list

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_blocktype(block_of_markdown):
    if not isinstance(block_of_markdown, str):
        raise TypeError("block_to_blocktype takes 'str' input")
    
    block = block_of_markdown
    if block[0] == "#":
        header = block
        header = header.strip("#")
        if header[0] != " ":
            raise Exception("header format incorrect")
        
        if len(header) < len(block) - 6:
        # Important, this determines that the number of #'s are not > 6 otherwise raises Error
            raise Exception("Too many #'s")
        return BlockType.HEADING
    
    
    if "```\n" in block[0: 4] and "```" in block[-3:]:
        
        return BlockType.CODE
    
    if block[0] == ">":
        quote_lines = block.splitlines()
        for line in quote_lines:
            if line[0] != ">":
                raise Exception("Invalid Quote Format")
        return BlockType.QUOTE
    
    if block[0:2] == "- ":
        ul_lines = block.splitlines()
        for line in ul_lines:
            if line[0:2] != "- ":
                raise Exception("Invalid UL Format")
        return BlockType.UNORDERED_LIST
    
    if block[0:3] == str(1)+". ":
        ol_lines = block.splitlines()
        for index, line in enumerate(ol_lines):
            if line[0:3] != str(index + 1)+". ":
                # I was a moron, index starts at 0, ordered lists start at 1
                raise Exception("Invalid OL Format")
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH