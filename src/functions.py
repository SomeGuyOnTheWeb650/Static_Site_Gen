from textnode import TextNode, TextType
from htmlnode import HTMLNode, ParentNode, LeafNode
import re
#pretend to pass in a text_node, it has attr of text, texttype and optional url
def text_node_to_html_node(text_node):
    match text_node.text_type:

        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
    raise Exception("TextType doesn't exist")


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    # we want to take the text of each old node, check for delimiters, and split along those limiters
    # make a list of new nodes, with the text type changed, we are passing in the text type that we are checking for
    if delimiter == "":
        return old_nodes
    
    new_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
            continue
        text = node.text
        split_text = text.split(delimiter)
        
        
        if len(split_text) % 2 == 0:
           
            raise SyntaxError("Syntax error, no closing delimiter") 
        for index, text in enumerate(split_text):
            if text == "":
                continue     
            if index % 2 == 0:
                new_nodes.append(TextNode(text, TextType.TEXT, node.url))
                continue
            new_nodes.append(TextNode(text, text_type, node.url))
    return new_nodes


def extract_markdown_images(text):
    if text is None:
        return None
    if not isinstance(text, str):
        raise TypeError("input is not a valid string")    
    result = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    
    return result

def extract_markdown_links(text):
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


def split_nodes_image(old_nodes):
    new_nodes = []
    if old_nodes is None or len(old_nodes) == 0:
        return new_nodes
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue 
        original_text = node.text
        images = extract_markdown_images(node.text)
        for image in images:
            sections = original_text.split(f"![{image[0]}]({image[1]})", 1)
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    if old_nodes is None or len(old_nodes) == 0:
        return new_nodes
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue 
        original_text = node.text
        links = extract_markdown_links(node.text)
        for link in links:
            sections = original_text.split(f"[{link[0]}]({link[1]})", 1)
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
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
