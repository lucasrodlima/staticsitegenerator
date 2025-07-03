import unittest

from textnode import TextNode, TextType
from leafnode import LeafNode
from text_node_to_html import text_node_to_html

class TestTextNodeToHTML(unittest.TestCase):
    def test_text_node_to_html(self):
        text_node = TextNode("Hello, world!", TextType.TEXT)
        html_node = text_node_to_html(text_node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.value, "Hello, world!")
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.props, None)

    def test_bold_text_node_to_html(self):
        text_node = TextNode("Bold text", TextType.BOLD)
        html_node = text_node_to_html(text_node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.value, "Bold text")
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.props, None)

    def test_italic_text_node_to_html(self):
        text_node = TextNode("Italic text", TextType.ITALIC)
        html_node = text_node_to_html(text_node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.value, "Italic text")
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.props, None)

    def test_code_text_node_to_html(self):
        text_node = TextNode("Code text", TextType.CODE)
        html_node = text_node_to_html(text_node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.value, "Code text")
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.props, None)

    def test_link_text_node_to_html(self):
        text_node = TextNode("Link text", TextType.LINK, url="https://example.com")
        html_node = text_node_to_html(text_node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.value, "Link text")
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.props, {"href": "https://example.com"})

    def test_image_text_node_to_html(self):
        text_node = TextNode("Image alt text", TextType.IMAGE, url="https://example.com/image.jpg")
        html_node = text_node_to_html(text_node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.props, {"src": "https://example.com/image.jpg", "alt": "Image alt text"})
