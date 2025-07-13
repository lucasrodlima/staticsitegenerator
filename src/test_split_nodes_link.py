import unittest

from split_nodes import split_nodes_link
from textnode import TextNode, TextType

class TestSplitNodesLink(unittest.TestCase):
    def test_split_nodes_link(self):
        node = TextNode("This is a text with a [link](https://example.com) word", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is a text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://example.com"),
                TextNode(" word", TextType.TEXT),
            ],
        )

    def test_split_multiple_links(self):
        node = TextNode("This is a text with a [link1](https://example.com/1) and [link2](https://example.com/2) word", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is a text with a ", TextType.TEXT),
                TextNode("link1", TextType.LINK, "https://example.com/1"),
                TextNode(" and ", TextType.TEXT),
                TextNode("link2", TextType.LINK, "https://example.com/2"),
                TextNode(" word", TextType.TEXT),
            ],
        )

    def test_no_links(self):
        node = TextNode("This is a text without links", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertEqual(new_nodes, [node])

    def test_with_image_and_link(self):
        node = TextNode("This is a text with an ![image](https://example.com/image.png) and a [link](https://example.com) word", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is a text with an ![image](https://example.com/image.png) and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://example.com"),
                TextNode(" word", TextType.TEXT),
            ],
        )

    def test_multiple_texts_with_links(self):
        node1 = TextNode("This is a text with a [link1](https://example.com/1)", TextType.TEXT)
        node2 = TextNode("And this is another text with a [link2](https://example.com/2)", TextType.TEXT)
        new_nodes = split_nodes_link([node1, node2])
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is a text with a ", TextType.TEXT),
                TextNode("link1", TextType.LINK, "https://example.com/1"),
                TextNode("And this is another text with a ", TextType.TEXT),
                TextNode("link2", TextType.LINK, "https://example.com/2"),
            ],
        )

    def test_link_with_no_text(self):
        node = TextNode("This is a text with a []()", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is a text with a ", TextType.TEXT),
                TextNode("", TextType.LINK, url=""),
            ],
        )

if __name__ == "__main__":
    unittest.main()