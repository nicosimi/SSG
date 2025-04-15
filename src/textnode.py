from enum import Enum

class TextType(Enum):
    TEXT = "normal"
    BOLD_TEXT   = "bold"
    ITALIC_TEXT = "italic"
    CODE_TEXT   = "code"
    LINK_TEXT   = "link"
    IMAGE_TEXT  = "image"


class TextNode():
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = TextType(text_type)
        self.url = url
    
    def __eq__(self, other):
        return ( (self.text == other.text) and
                 (self.text_type == other.text_type) and
                 (self.url == other.url))

    def __repr__(self):
        cls = self.__class__.__name__
        return f"{cls}({self.text}, {self.text_type.value}, {self.url})"

    def get_text(self):
        return self.text

    def get_text_type(self):
        return self.text_type
    
    def get_url(self):
        return self.url
