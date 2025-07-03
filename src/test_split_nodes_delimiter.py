import unittest

from split_nodes_delimiter import split_nodes_delimiter
from textnode import TextNode,TextType


class SplitNodesDelimiterTest(unittest.TestCase):

    def test_split_code(self):
        node = TextNode("This is a text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [TextNode("This is a text with a ", TextType.TEXT), TextNode("code block", TextType.CODE), TextNode(" word", TextType.TEXT)])

    def test_split_bold(self):
        node = TextNode("This is a text with a **bold** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [TextNode("This is a text with a ", TextType.TEXT), TextNode("bold", TextType.BOLD), TextNode(" word", TextType.TEXT)])

    def test_split_italic(self):
        node = TextNode("This is a text with a *italic* word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        self.assertEqual(new_nodes, [TextNode("This is a text with a ", TextType.TEXT), TextNode("italic", TextType.ITALIC), TextNode(" word", TextType.TEXT)])


if __name__ == "__main__":
    unittest.main()
