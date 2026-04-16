from textnode import TextNode, TextType
from functions import extract_markdown_images, extract_markdown_links
import re
def split_nodes_image_alt(old_nodes):
    # take list of old nodes
    # take the text of each node, split along image format
    # create a list of plain strings first, then determine stuff
    # create a new list of TextNodes, with TEXT and IMAGE values
    # how to split along image format?
    # regex? fstring? multiple splits?
    if old_nodes is None or len(old_nodes) == 0:
        return []
    new_nodes = []
    
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
            continue
        not_images = re.split(r"!\[[^\].*?]+\]\([^\).*?]+\)", node.text)
        images = extract_markdown_images(node.text)
        
        for i in range(len(not_images)):
            if not_images[i] != "":

                new_nodes.append(TextNode(not_images[i], TextType.TEXT))        
            if i < len(images):
                new_nodes.append(TextNode(images[i][0], TextType.IMAGE, images[i][1]))

            

    return new_nodes

def split_nodes_link_alt(old_nodes):
    # don't mess with nested links yet, just get it working
    if old_nodes is None or len(old_nodes) == 0:
        return []
    new_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
            continue
        not_links = re.split(r"(?<!!)\[[^\[\]]*\][^\)*?]*\)", node.text)
        links = extract_markdown_links(node.text)
        for i in range(len(not_links)):
            if not_links[i] != "":
                new_nodes.append(TextNode(not_links[i], TextType.TEXT))
            if i < len(links):
                new_nodes.append(TextNode(links[i][0], TextType.LINK, links[i][1]))

    return new_nodes

def extract_markdown_links_alt(text):
    if text is None:
        return None
    if not isinstance(text, str):
        raise TypeError("input is not a valid string")    
    complex_result = []
    result = re.findall(r"\[!\[(.*?)\]\((.*?)\)\]\((.*?)\)", text)
    
    if result != []:
        
        for item in result:
            complex_result.append((f"![{item[0]}]({item[1]})", item[2]))
            
    result = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\[\]\(\)]*)\)", text)
    result = complex_result + result
    return result

