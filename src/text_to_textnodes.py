from split_nodes import split_nodes_delimiter, split_nodes_image, split_nodes_link
from textnode import TextNode, TextType


def text_to_textnodes(text):
    initial_node = TextNode(text, TextType.TEXT)

    code_separated = split_nodes_delimiter([initial_node], "`", TextType.CODE)

    bold_separated = split_nodes_delimiter(code_separated, "**", TextType.BOLD)

    italic_separated = split_nodes_delimiter(bold_separated, "_", TextType.ITALIC)

    image_separated = split_nodes_image(italic_separated)

    link_separated = split_nodes_link(image_separated)

    return link_separated
