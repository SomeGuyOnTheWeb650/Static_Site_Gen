class HTMLNode():
    def __init__(self,
                 tag: str | None = None,
                 value: str | None = None, 
                 children: list["HTMLNode"] | None = None, 
                 props: dict[str, str] | None = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __repr__(self):
        result = f"""
        HTMLNode
        --------
        Tag: {self.tag}
        Value: {self.value}
        Children: {self.children}
        Props: {self.props}
        """
        
        return result
    
    
    
    def to_html(self):
        raise NotImplementedError("This hasn't been implemented")
        


    def props_to_html(self):
        result = ""
        if self.props is None:
            return result
        for prop in self.props:
            result += f' {prop}="{self.props[prop]}"'
        return result

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("LeafNode has no value")
        if self.tag is None:
            return self.value
        t = self.tag
        
        result = f"<{t}{self.props_to_html()}>{self.value}</{t}>"
        
        return result

    def __repr__(self):
        return f"""
        LeafNode
        ------------------
        Tag: {self.tag}
        Value: {self.value}
        Props: {self.props}
        """
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("ParentNode, node has no tag")
        if self.children is None:
            raise ValueError("ParentNode, node has no children")
        result = f"<{self.tag}{self.props_to_html()}>"
        for child in self.children:
            result += child.to_html()
        result += f"</{self.tag}>"

        return result