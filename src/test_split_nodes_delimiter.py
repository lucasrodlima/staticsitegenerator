import unittest

from split_nodes import split_nodes_delimiter
from textnode import TextNode, TextType


class SplitNodesDelimiterTest(unittest.TestCase):
    def test_split_code(self):
        node = TextNode("This is a text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is a text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
        )

    def test_split_bold(self):
        node = TextNode("This is a text with a **bold** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is a text with a ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ],
        )

    def test_split_italic(self):
        node = TextNode("This is a text with a _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is a text with a ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ],
        )

    def test_split_multiple_delimiters(self):
        node = TextNode("This is a text with a `code block`, **bold**, and _italic_ word", TextType.TEXT)
        code_splitted = split_nodes_delimiter([node], "`", TextType.CODE)
        bold_splitted = split_nodes_delimiter(code_splitted, "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(bold_splitted, "_", TextType.ITALIC)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is a text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(", ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(", and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ],
        )

    def test_split_no_delimiter_present(self):
        node = TextNode("This text has no delimiters", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [node])

    def test_split_non_text_node_unchanged(self):
        node = TextNode("This is bold text", TextType.BOLD)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [node])

    def test_split_multiple_code_blocks(self):
        node = TextNode("First `code1` then `code2` and `code3` end", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [
                TextNode("First ", TextType.TEXT),
                TextNode("code1", TextType.CODE),
                TextNode(" then ", TextType.TEXT),
                TextNode("code2", TextType.CODE),
                TextNode(" and ", TextType.TEXT),
                TextNode("code3", TextType.CODE),
                TextNode(" end", TextType.TEXT),
            ],
        )

    def test_split_delimiter_at_start(self):
        node = TextNode("`code` at the beginning", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [
                TextNode("", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode(" at the beginning", TextType.TEXT),
            ],
        )

    def test_split_delimiter_at_end(self):
        node = TextNode("Text ending with `code`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [
                TextNode("Text ending with ", TextType.TEXT),
                TextNode("code", TextType.CODE),
            ],
        )

    def test_split_empty_delimiter_content(self):
        node = TextNode("Empty code `` block", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [
                TextNode("Empty code ", TextType.TEXT),
                TextNode("", TextType.CODE),
                TextNode(" block", TextType.TEXT),
            ],
        )

    def test_split_mixed_node_types(self):
        nodes = [
            TextNode("Normal text with `code`", TextType.TEXT),
            TextNode("Already bold", TextType.BOLD),
            TextNode("More text with `another code`", TextType.TEXT)
        ]
        new_nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
        expected = [
            TextNode("Normal text with ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode("Already bold", TextType.BOLD),
            TextNode("More text with ", TextType.TEXT),
            TextNode("another code", TextType.CODE),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_invalid_delimiter_for_code(self):
        node = TextNode("Text with **bold**", TextType.TEXT)
        with self.assertRaises(ValueError) as context:
            split_nodes_delimiter([node], "**", TextType.CODE)
        self.assertEqual(str(context.exception), "Delimiter for code must be '`'")

    def test_split_invalid_delimiter_for_bold(self):
        node = TextNode("Text with `code`", TextType.TEXT)
        with self.assertRaises(ValueError) as context:
            split_nodes_delimiter([node], "`", TextType.BOLD)
        self.assertEqual(str(context.exception), "Delimiter for bold must be '**'")

    def test_split_invalid_delimiter_for_italic(self):
        node = TextNode("Text with **bold**", TextType.TEXT)
        with self.assertRaises(ValueError) as context:
            split_nodes_delimiter([node], "**", TextType.ITALIC)
        self.assertEqual(str(context.exception), "Delimiter for italic must be '_'")

    def test_split_nested_delimiters(self):
        node = TextNode("Text with **bold `code` inside**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [
                TextNode("Text with ", TextType.TEXT),
                TextNode("bold `code` inside", TextType.BOLD),
            ],
        )

    def test_split_consecutive_delimiters(self):
        node = TextNode("Text **bold1****bold2** more text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [
                TextNode("Text ", TextType.TEXT),
                TextNode("bold1", TextType.BOLD),
                TextNode("", TextType.TEXT),
                TextNode("bold2", TextType.BOLD),
                TextNode(" more text", TextType.TEXT),
            ],
        )

    def test_split_modifies_original_list(self):
        original_nodes = [TextNode("Text with `code`", TextType.TEXT)]
        original_copy = original_nodes.copy()
        split_nodes_delimiter(original_nodes, "`", TextType.CODE)
        # Original should remain unchanged due to .copy() in the function
        self.assertEqual(original_nodes, original_copy)


if __name__ == "__main__":
    unittest.main()
