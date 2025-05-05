class HTMLNode:

    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError("child class should override this method")
    
    def props_to_html(self):
        html = ""
        if (self.props is None):
            return html
        for key in self.props:
            html += f" {key}=\"{self.props[key]}\""
        return html
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"


class LeafNode(HTMLNode):

    def __init__(self, tag, value, props = None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if (self.value is None):
            raise ValueError("All leaf nodes must have a value")
        if (self.tag is None):
            return self.value
        
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):

    def __init__(self, tag, children, props = None):
        super().__init__(tag, None, children, props)
    
    def to_html(self):
        if (self.tag is None):
            raise ValueError("Parent node must have a tag")
        if (self.children is None):
            raise ValueError("Parent node must have children")
        
        html = ""
        for child in self.children:
            html += child.to_html()
        return f"<{self.tag}{self.props_to_html()}>{html}</{self.tag}>"

    
