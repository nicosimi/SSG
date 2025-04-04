from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props = None):
        super().__init__(tag, None, children, props)

    def __repr__(self):
        return super().__repr__()
    
    def to_html(self):
        if self.tag == None: raise ValueError("Tag is required")
        if self.children == None: raise ValueError("Children is null")
        res = f"<{self.tag}>"
        for node in self.children:
            aux = node.to_html()
            res += aux
        res += f"</{self.tag}>"
        return res
