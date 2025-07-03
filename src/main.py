from textnode import TextNode, TextType
from leafnode import LeafNode


def main():
    node1 = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    node2 = LeafNode("p", "This is a paragraph.", children=[node1])

    print(node1)
    print(node2)


if __name__ == "__main__":
    main()
