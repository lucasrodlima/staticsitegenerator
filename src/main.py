from classes import TextNode, TextType

# Main function
def main():
    node1 = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")

    print(node1)


if __name__ == "__main__":
    main()
