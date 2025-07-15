import re
import os
import shutil
from classes import TextNode, TextType, LeafNode, BlockType, ParentNode


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


def block_to_blocktype(block):
    if block.startswith("# ") and "\n" not in block:
        return BlockType.HEADING
    elif block.startswith("## ") and "\n" not in block:
        return BlockType.HEADING
    elif block.startswith("### ") and "\n" not in block:
        return BlockType.HEADING
    elif block.startswith("#### ") and "\n" not in block:
        return BlockType.HEADING
    elif block.startswith("##### ") and "\n" not in block:
        return BlockType.HEADING
    elif block.startswith("###### ") and "\n" not in block:
        return BlockType.HEADING

    elif block.startswith("```") and block.endswith("```"):
        return BlockType.CODE

    elif block.startswith("> "):
        lines = block.split("\n")
        if all(map(lambda x: x.startswith("> "), lines)):
            return BlockType.QUOTE
    
    elif block.startswith("- "):
        lines = block.split("\n")
        if all(map(lambda x: x.startswith("- "), lines)):
            return BlockType.UNORDERED_LIST

    elif block[0] == "1" and block[1] == ".":
        lines = block.split("\n")
        if all(map(lambda x: x[0].isdigit() and x[1] == ".", lines)):
            nums = []
            for line in lines:
                nums.append(int(line.split(".")[0]))
            if nums == list(range(1, len(nums) + 1)):
                return BlockType.ORDERED_LIST

    else:
        return BlockType.PARAGRAPH


def text_to_children(text):
    text_nodes = text_to_textnodes(text)

    html_nodes = []
    for node in text_nodes:
        html_nodes.append(text_node_to_html(node))

    return html_nodes


def markdown_to_html_node(markdown):
    final_nodes = []

    blocks = markdown_to_blocks(markdown)

    for block in blocks:
        block_type = block_to_blocktype(block)

        match block_type:
            case BlockType.PARAGRAPH:
                lines = block.split("\n")
                text = " ".join(line.strip() for line in lines)

                children_nodes = text_to_children(text)               

                final_nodes.append( ParentNode(tag="p", children=children_nodes) )

            case BlockType.HEADING:
                text = block.lstrip("#").strip()

                children_nodes = text_to_children(text)

                header_level = f"h{ block.count("#") }"

                final_nodes.append( ParentNode(tag=f"{ header_level }", children=children_nodes) )

            case BlockType.CODE:
                text_node = TextNode(block.strip("`\n "), TextType.CODE)

                html_node = text_node_to_html(text_node) 

                if "\n" not in html_node.value:
                    final_nodes.append(html_node)
                else:
                    html_node.value += "\n"
                    final_nodes.append( ParentNode(tag="pre", children=[html_node]) )

            case BlockType.QUOTE:
                text = block.lstrip("> ").strip()
                children_nodes = text_to_children(text)

                final_nodes.append( ParentNode(tag="blockquote", children=children_nodes ) )

            case BlockType.UNORDERED_LIST:
                items = block.split("\n")

                list_items = []

                for item in items:
                    children_nodes = text_to_children(item.strip("- "))

                    list_items.append( ParentNode(tag="li", children=children_nodes ) )

                final_nodes.append( ParentNode(tag="ul", children=list_items) )

            case BlockType.ORDERED_LIST:
                items = block.split("\n")

                list_items = []

                for item in items:
                    children_nodes = text_to_children(item.strip("1234567890. "))

                    list_items.append( ParentNode(tag="li", children=children_nodes) )

                final_nodes.append( ParentNode(tag="ol", children=list_items ))
                
    master_html = ParentNode( tag="div", children=final_nodes )

    return master_html
    

def copy_directory_contents(src, dest):
    if os.path.exists(dest):
        shutil.rmtree(dest)
    os.mkdir(dest)

    for item in os.listdir(src):
        if os.path.isfile(os.path.join(src, item)):
            shutil.copy2(os.path.join(src, item), dest)
            print(f"Copied file: {os.path.join(src, item)} to {dest}")
        elif os.path.isdir(os.path.join(src, item)):
            os.makedirs(os.path.join(dest, item))
            copy_directory_contents(os.path.join(src, item), os.path.join(dest, item))


def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()
    raise Exception("No title found in markdown")


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using template {template_path}")

    with open(from_path, 'r') as f:
        markdown_content = f.read()

    with open(template_path, 'r') as f:
        template_content = f.read()

    html_node = markdown_to_html_node(markdown_content)
    html_string = html_node.to_html()

    title = extract_title(markdown_content)

    template_content = template_content.replace("{{ Title }}", title)
    template_content = template_content.replace("{{ Content }}", html_string)

    dest_dir = os.path.dirname(dest_path)
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    with open(dest_path, 'w') as f:
        f.write(template_content)