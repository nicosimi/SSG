

class HTMLNode():
    def __init__(self, tag=None, value=None, children = None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def __eq__(self, other):
        return (    (self.tag == other.tag)
                and (self.value == other.value)
                and (self.children == other.children)
                and (self.props == other.props))
    
    def __repr__(self):
        return f"{self.__class__.__name__}({self.tag}, {self.value}, {self.children}, {self.props})"

    def to_html(self):
        ###Override in child classes
        raise NotImplementedError
    
    def props_to_html(self):
        res = ""
        if self.props == None:
            return res
        if len(self.props.keys()) > 0:
            texts = []
            for key in sorted(self.props.keys()):
                aux = f"{key}=\"{self.props[key]}\""
                texts.append(aux)
            res = res + " ".join(texts)
        return res
                
