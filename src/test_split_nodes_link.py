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

    def test_link_at_beginning(self):
        node = TextNode("[link](https://example.com) at the beginning", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://example.com"),
                TextNode(" at the beginning", TextType.TEXT),
            ],
        )

    def test_link_at_end(self):
        node = TextNode("Text ending with [link](https://example.com)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("Text ending with ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://example.com"),
            ],
        )

    def test_only_link(self):
        node = TextNode("[link](https://example.com)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://example.com"),
            ],
        )

    def test_consecutive_links(self):
        node = TextNode("[link1](url1.com)[link2](url2.com)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("", TextType.TEXT),
                TextNode("link1", TextType.LINK, "url1.com"),
                TextNode("", TextType.TEXT),
                TextNode("link2", TextType.LINK, "url2.com"),
            ],
        )

    def test_non_text_node_unchanged(self):
        node = TextNode("Already bold text", TextType.BOLD)
        new_nodes = split_nodes_link([node])
        self.assertEqual(new_nodes, [node])

    def test_mixed_node_types(self):
        nodes = [
            TextNode("Text with [link](url.com)", TextType.TEXT),
            TextNode("Bold text", TextType.BOLD),
            TextNode("More text", TextType.TEXT)
        ]
        new_nodes = split_nodes_link(nodes)
        expected = [
            TextNode("Text with ", TextType.TEXT),
            TextNode("link", TextType.LINK, "url.com"),
            TextNode("Bold text", TextType.BOLD),
            TextNode("More text", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_link_with_special_characters_in_text(self):
        node = TextNode("[Link: @#$%^&*()!](https://example.com)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("", TextType.TEXT),
                TextNode("Link: @#$%^&*()!", TextType.LINK, "https://example.com"),
            ],
        )

    def test_modifies_original_list(self):
        original_nodes = [TextNode("Text with [link](url.com)", TextType.TEXT)]
        original_copy = original_nodes.copy()
        split_nodes_link(original_nodes)
        # Original should remain unchanged due to .copy() in the function
        self.assertEqual(original_nodes, original_copy)

    def test_link_with_complex_url(self):
        node = TextNode("[link](https://example.com/path/page.html?query=value&other=param#fragment)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://example.com/path/page.html?query=value&other=param#fragment"),
            ],
        )

    def test_link_with_empty_text_but_valid_url(self):
        node = TextNode("Check this [](https://example.com) out", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("Check this ", TextType.TEXT),
                TextNode("", TextType.LINK, "https://example.com"),
                TextNode(" out", TextType.TEXT),
            ],
        )

    def test_link_with_text_but_empty_url(self):
        node = TextNode("Check this [link text]() out", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("Check this ", TextType.TEXT),
                TextNode("link text", TextType.LINK, ""),
                TextNode(" out", TextType.TEXT),
            ],
        )

if __name__ == "__main__":
    unittest.main()