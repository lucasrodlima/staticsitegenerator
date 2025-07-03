class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("Subclasses should implement this method")

    def props_to_html(self):
        end_string = str()
        for k, v in self.props.items():
            end_string += f' {k}="{v}"' if len(end_string) != 0 else f'{k}="{v}"'

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
