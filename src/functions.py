from textnode import TextNode, TextType
from htmlnode import HTMLNode, ParentNode, LeafNode

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
