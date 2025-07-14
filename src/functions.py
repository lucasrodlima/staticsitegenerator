import re
from classes import TextNode, TextType, LeafNode


# Text node to HTML conversion
def text_node_to_html(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(value=text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise Exception("TextNode type not supported: " +
                            str(text_node.text_type))


# Regex functions
def extract_markdown_images(text):
    return re.findall(r"\!\[(.*?)\]\((.*?)\)", text)
    

def extract_markdown_links(text):
    return re.findall(r"(?<!\!)\[(.*?)\]\((.*?)\)", text)


# Split nodes functions
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    old_nodes = old_nodes.copy()
    new_nodes = []

    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
            continue

        match text_type:
            case TextType.CODE:
                if delimiter != "`":
                    raise ValueError("Delimiter for code must be '`'")

                if delimiter not in node.text:
                    new_nodes.append(node)
                    continue

                while delimiter in node.text:

                    split_text = node.text.split(delimiter, 2)

                    node.text = split_text[2]

                    new_nodes.extend(
                        [
                            TextNode(split_text[0], TextType.TEXT),
                            TextNode(split_text[1], TextType.CODE),
                        ]
                    )

                    if node.text and delimiter not in node.text:
                        new_nodes.append(TextNode(node.text, TextType.TEXT))

            case TextType.BOLD:
                if delimiter != "**":
                    raise ValueError("Delimiter for bold must be '**'")

                if delimiter not in node.text:
                    new_nodes.append(node)
                    continue

                while delimiter in node.text:
                    split_text = node.text.split(delimiter, 2)

                    node.text = split_text[2]

                    new_nodes.extend(
                        [
                            TextNode(split_text[0], TextType.TEXT),
                            TextNode(split_text[1], TextType.BOLD),
                        ]
                    )

                    if node.text and delimiter not in node.text:
                        new_nodes.append(TextNode(node.text, TextType.TEXT))
                

            case TextType.ITALIC:
                if delimiter != "_":
                    raise ValueError("Delimiter for italic must be '_'")

                if delimiter not in node.text:
                    new_nodes.append(node)
                    continue

                while delimiter in node.text:
                    split_text = node.text.split(delimiter, 2)

                    node.text = split_text[2]

                    new_nodes.extend(
                        [
                            TextNode(split_text[0], TextType.TEXT),
                            TextNode(split_text[1], TextType.ITALIC),
                        ]
                    )

                    if node.text and delimiter not in node.text:
                        new_nodes.append(TextNode(node.text, TextType.TEXT))

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

            if image == images[-1] and node.text:
                new_nodes.append(TextNode(node.text, TextType.TEXT))

    return new_nodes


def split_nodes_link(old_nodes):
    old_nodes = old_nodes.copy()
    new_nodes = []  # [node]

    for node in old_nodes:  # text, TextType
        links = extract_markdown_links(node.text)

        if len(links) == 0:
            new_nodes.append(node)
            continue

        for link in links:
            link_text = f"[{link[0]}]({link[1]})"

            new_nodes.append(TextNode(node.text.split(link_text, 1)[0], TextType.TEXT))

            new_nodes.append(TextNode(link[0], TextType.LINK, url=link[1]))

            node.text = node.text.split(link_text, 1)[1]

            if link == links[-1] and node.text:
                new_nodes.append(TextNode(node.text, TextType.TEXT))

    return new_nodes


# Text to text nodes conversion
def text_to_textnodes(text):
    initial_node = TextNode(text, TextType.TEXT)

    code_separated = split_nodes_delimiter([initial_node], "`", TextType.CODE)

    bold_separated = split_nodes_delimiter(code_separated, "**", TextType.BOLD)

    italic_separated = split_nodes_delimiter(bold_separated, "_", TextType.ITALIC)

    image_separated = split_nodes_image(italic_separated)

    link_separated = split_nodes_link(image_separated)

    return link_separated


# Markdown to blocks function
def markdown_to_blocks(markdown):
    blocks = list(
        filter(lambda x: x != "", map(lambda x: x.strip(), markdown.split("\n\n")))
    )

    return blocks

