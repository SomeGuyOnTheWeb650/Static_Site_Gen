from textnode import TextNode, TextType

def main():
    result = TextNode("sample_text", TextType.LINK, "http://dummyurl.com")
    return print(result)


main()