class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()
    
    def props_to_html(self):
        if self.props is None:
            return ""
        
        output = ""
        for key, value in self.props.items():
            output += f' {key}="{value}"'
        return output
    
    def __repr__(self):
        return f'Tag: {self.tag}, Value: {self.value}, Children: {self.children}, Props: {self.props}'

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("Invalid HTML: LeafNode must have a value")
        if self.tag is None:
            return self.value 
        
        return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'
    
    def __repr__(self):
        return f'Tag: {self.tag}, Value: {self.value}, Props: {self.props}'
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)  

    def to_html(self):
        if self.tag is None:
            raise ValueError("Invalid HTML: ParentNode must have a tag")
        if self.children is None or len(self.children) == 0:
            raise ValueError("Invalid HTML: ParentNode must have a child")
        
        if self.props:
            parent_str = f"<{self.tag}{self.props_to_html()}>"
        else:
            parent_str = f"<{self.tag}>"

        for child in self.children:
            parent_str += child.to_html()
        parent_str += f"</{self.tag}>"

        return parent_str    



