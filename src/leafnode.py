from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props:dict=None):
        super().__init__(tag, value, None, props)

    def __repr__(self):
        return super().__repr__()

    def to_html(self):
        if self.value == None: raise ValueError("Leaf node must have a value")
        match self.tag:
            case "p"| "h1" | "h2" | "h3" | "h4" | "h5" | "h6" | "b" | "i" | "li" | "blockquote" | "span":
                return f"<{self.tag}>{self.value}</{self.tag}>"
            case "code":
                return f"<{self.tag}>{self.value}</{self.tag}>"
            case "a":
                return f"<{self.tag} href=\"{self.props["href"]}\">{self.value}</{self.tag}>"
            case "img":
                return f"<{self.tag} src=\"{self.props["src"]}\" alt=\"{self.value}\" />"

        return self.value

            
        
