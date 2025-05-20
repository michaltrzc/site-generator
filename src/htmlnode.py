from textnode import TextNode, TextType

class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value 
        self.children = children
        self.props = props

    def to_html(self):
        if self.children is None:
            if self.value is None:
                return f"<{self.tag}></{self.tag}>"
            else:
                return f"<{self.tag}>{self.value}</{self.tag}>"
        else:
            children_html = ""
            for child in self.children:
                children_html += child.to_html()
        
            if self.props is not None:
                props_html = ""
                for prop_key, prop_value in self.props.items():
                    props_html += f' {prop_key}="{prop_value}"'
                return f"<{self.tag}{props_html}>{children_html}</{self.tag}>"
            else:
                return f"<{self.tag}>{children_html}</{self.tag}>"
    
    def props_to_html(self):
        if not self.props:
            return ""
        props_str = ""
        for key, value in self.props.items():
            props_str += f' {key}="{value}"'
        return props_str

    def __repr__(self):
        print (f"HTMLNode ({self.tag}, {self.value},{self.children},{self.props})")

class LeafNode (HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value == None:
            raise ValueError("LeafNode must have a value")
        if self.tag == None:
            return str(self.value)
        else:
            return (f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>")
        
class ParentNode (HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("ParentNode must have a tag")
        if self.children is None:
            raise ValueError("ParentNode must have children")
    
    # Start with the opening tag (handle props if needed)
        html = f"<{self.tag}"
        if self.props:
            props_str = ""
            for key, value in self.props.items():
                props_str += f' {key}="{value}"'
            html += props_str

        html += ">"
    
    # Recursively call to_html() on each child
        for child in self.children:
            html += child.to_html()
    
    # Add the closing tag
        html += f"</{self.tag}>"
    
        return html
    
def text_node_to_html_node(text_node):
    if text_node.text_type not in (TextType.TEXT, TextType.BOLD, TextType.IMAGE, TextType.CODE, TextType.LINK, TextType.ITALIC):
        raise Exception ("Type not in TextType enum")
    elif text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text, None)
    elif text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text, None)
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text, None)
    elif text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text, None)
    elif text_node.text_type == TextType.LINK:
        return LeafNode("a", text_node.text, {"href": text_node.url})
    elif text_node.text_type == TextType.IMAGE:
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
