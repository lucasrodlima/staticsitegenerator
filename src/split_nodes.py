from textnode import TextNode, TextType
from regex_functions import extract_markdown_images, extract_markdown_links


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)

        match text_type:
            case TextType.CODE:
                if delimiter != "`":
                    raise ValueError("Delimiter for code must be '`'")

                split_text = node.text.split(delimiter)

                new_nodes.extend(
                    [
                        TextNode(split_text[0], TextType.TEXT),
                        TextNode(split_text[1], TextType.CODE),
                        TextNode(split_text[2], TextType.TEXT),
                    ]
                )

            case TextType.BOLD:
                if delimiter != "**":
                    raise ValueError("Delimiter for bold must be '**'")

                split_text = node.text.split(delimiter)

                new_nodes.extend(
                    [
                        TextNode(split_text[0], TextType.TEXT),
                        TextNode(split_text[1], TextType.BOLD),
                        TextNode(split_text[2], TextType.TEXT),
                    ]
                )

            case TextType.ITALIC:
                if delimiter != "_":
                    raise ValueError("Delimiter for italic must be '_'")

                split_text = node.text.split(delimiter)

                new_nodes.extend(
                    [
                        TextNode(split_text[0], TextType.TEXT),
                        TextNode(split_text[1], TextType.ITALIC),
                        TextNode(split_text[2], TextType.TEXT),
                    ]
                )

    return new_nodes


def split_nodes_image(old_nodes):
    old_nodes = old_nodes.copy()
    new_nodes = [] # [node]

    for node in old_nodes: # text, TextType
        images = extract_markdown_images(node.text)

        if len(images) == 0:
            new_nodes.append(node)
            continue

        for image in images:
            image_text = f"![{image[0]}]({image[1]})"

            new_nodes.append(TextNode(node.text.split(image_text, 1)[0], TextType.TEXT))

            new_nodes.append(TextNode(image[0], TextType.IMAGE, url=image[1]))

            node.text = node.text.split(image_text, 1)[1]

            if image == images[-1]:
                new_nodes.append(TextNode(node.text, TextType.TEXT))

    return new_nodes


