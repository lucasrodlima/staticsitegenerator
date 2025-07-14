import unittest
from text_to_textnodes import text_to_textnodes
from textnode import TextNode, TextType


class TestTextToTextNodes(unittest.TestCase):
    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"

        new_nodes = text_to_textnodes(text)

        self.assertEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode(
                    "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
                ),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            new_nodes,
        )

    def test_text_to_textnodes_plain_text(self):
        text = "This is just plain text with no formatting"
        new_nodes = text_to_textnodes(text)
        self.assertEqual([TextNode(text, TextType.TEXT)], new_nodes)

    def test_text_to_textnodes_only_bold(self):
        text = "**bold text**"
        new_nodes = text_to_textnodes(text)
        self.assertEqual(
            [
                TextNode("", TextType.TEXT),
                TextNode("bold text", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_text_to_textnodes_only_italic(self):
        text = "_italic text_"
        new_nodes = text_to_textnodes(text)
        self.assertEqual(
            [
                TextNode("", TextType.TEXT),
                TextNode("italic text", TextType.ITALIC),
            ],
            new_nodes,
        )

    def test_text_to_textnodes_only_code(self):
        text = "`code text`"
        new_nodes = text_to_textnodes(text)
        self.assertEqual(
            [
                TextNode("", TextType.TEXT),
                TextNode("code text", TextType.CODE),
            ],
            new_nodes,
        )

    def test_text_to_textnodes_only_image(self):
        text = "![alt text](https://example.com/image.png)"
        new_nodes = text_to_textnodes(text)
        self.assertEqual(
            [
                TextNode("", TextType.TEXT),
                TextNode("alt text", TextType.IMAGE, "https://example.com/image.png"),
            ],
            new_nodes,
        )

    def test_text_to_textnodes_only_link(self):
        text = "[link text](https://example.com)"
        new_nodes = text_to_textnodes(text)
        self.assertEqual(
            [
                TextNode("", TextType.TEXT),
                TextNode("link text", TextType.LINK, "https://example.com"),
            ],
            new_nodes,
        )

    def test_text_to_textnodes_multiple_same_type(self):
        text = "Text with **bold1** and **bold2** words"
        new_nodes = text_to_textnodes(text)
        self.assertEqual(
            [
                TextNode("Text with ", TextType.TEXT),
                TextNode("bold1", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("bold2", TextType.BOLD),
                TextNode(" words", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_text_to_textnodes_complex_combination(self):
        text = "Start **bold** _italic_ `code` ![img](url.png) [link](url.com) end"
        new_nodes = text_to_textnodes(text)
        self.assertEqual(
            [
                TextNode("Start ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode(" ", TextType.TEXT),
                TextNode("img", TextType.IMAGE, "url.png"),
                TextNode(" ", TextType.TEXT),
                TextNode("link", TextType.LINK, "url.com"),
                TextNode(" end", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_text_to_textnodes_empty_string(self):
        text = ""
        new_nodes = text_to_textnodes(text)
        self.assertEqual([TextNode("", TextType.TEXT)], new_nodes)

    def test_text_to_textnodes_image_and_link_mixed(self):
        text = "Check ![image](img.png) and [link](site.com) together"
        new_nodes = text_to_textnodes(text)
        self.assertEqual(
            [
                TextNode("Check ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "img.png"),
                TextNode(" and ", TextType.TEXT),
                TextNode("link", TextType.LINK, "site.com"),
                TextNode(" together", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_text_to_textnodes_adjacent_formatting(self):
        text = "**bold**_italic_"
        new_nodes = text_to_textnodes(text)
        self.assertEqual(
            [
                TextNode("", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode("", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
            new_nodes,
        )

    def test_text_to_textnodes_empty_formatting(self):
        text = "Text with **** empty bold and __ empty italic and `` empty code"
        new_nodes = text_to_textnodes(text)
        self.assertEqual(
            [
                TextNode("Text with ", TextType.TEXT),
                TextNode("", TextType.BOLD),
                TextNode(" empty bold and ", TextType.TEXT),
                TextNode("", TextType.ITALIC),
                TextNode(" empty italic and ", TextType.TEXT),
                TextNode("", TextType.CODE),
                TextNode(" empty code", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_text_to_textnodes_special_characters(self):
        text = "Text with **bold @#$%** and _italic &*()_ formatting"
        new_nodes = text_to_textnodes(text)
        self.assertEqual(
            [
                TextNode("Text with ", TextType.TEXT),
                TextNode("bold @#$%", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic &*()", TextType.ITALIC),
                TextNode(" formatting", TextType.TEXT),
            ],
            new_nodes,
        )


if __name__ == "__main__":
    unittest.main()
