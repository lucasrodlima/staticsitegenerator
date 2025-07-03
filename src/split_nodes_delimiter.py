from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)

        match text_type:
            case TextType.CODE:
                split_text = node.text.split(delimiter)

                new_nodes.extend([
                    TextNode(split_text[0], TextType.TEXT),
                    TextNode(split_text[1], TextType.CODE),
                    TextNode(split_text[2], TextType.TEXT),
                ])

            case TextType.BOLD:
                split_text = node.text.split(delimiter)

                new_nodes.extend([
                    TextNode(split_text[0], TextType.TEXT),
                    TextNode(split_text[1], TextType.BOLD),
                    TextNode(split_text[2], TextType.TEXT),
                ])

            case TextType.ITALIC:
                split_text = node.text.split(delimiter)

                new_nodes.extend([
                    TextNode(split_text[0], TextType.TEXT),
                    TextNode(split_text[1], TextType.ITALIC),
                    TextNode(split_text[2], TextType.TEXT),
                ])
        
    return new_nodes
