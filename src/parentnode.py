from htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(self, tag=None, children=None, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("Error: No tag provided for ParentNode.")
        elif self.children is None or len(self.children) == 0:
            raise ValueError("Error: No children provided for ParentNode.")
        else:
            end_string = f"<{self.tag}{self.props_to_html()}>"
            for child in self.children:
                child_string = child.to_html()
                end_string += child_string
            end_string += f"</{self.tag}>"
            return end_string

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.children}, {self.props})"
