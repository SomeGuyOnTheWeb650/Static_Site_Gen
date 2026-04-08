class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __repr__(self):
        result = f"HTMLNode: Tag: {self.tag}\nValue: {self.value}\nChildren: {self.children}\nProps: {self.props}"
        
        return result
    
    
    
    def to_html(self):
        raise NotImplementedError
        


    def props_to_html(self):
        result = ""
        if self.props is None:
            return result
        for prop in self.props:
            result += f" {prop}={self.props[prop]}"
        return result
