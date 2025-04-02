from htmlnode import HTMLNode

class Leafnode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        super().__init__(tag, value, props)

    def __repr__(self):
        return super().__repr__()

    def to_html(self):
        if self.value == None: raise ValueError("Leaf node must have a value")
        match self.tag:
            case "p"| "h1" | "h2" | "h3" | "h4" | "h5" | "h6" | "b" | "i" | "li" | "blockquote" | "code":
                return f"<{self.tag}>{self.value}</{self.tag}"
            case "a":
                key = self.props.keys()
                return f"<{self.tag} {key[0]}=\"{self.props[key[0]]}\">{self.value}</{self.tag}>"
            case "img":
                keys = sorted(self.props.keys())
                return f"<{self.tag} {keys[0]}=\"{self.props[keys[0]]}\" {keys[1]}=\"{self.props[keys[1]]}\" />"

        return self.value

            
        
