import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_with_url(self):
        node = TextNode("This is a text node", TextType.BOLD, "google.com")
        node2 = TextNode("This is a text node", TextType.BOLD, "google.com")
        self.assertEqual(node, node2)

    def test_different_url(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD, "google.com")
        self.assertNotEqual(node, node2)

    def test_different_text_type(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_different_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is another text node", TextType.TEXT)
        self.assertNotEqual(node, node2)

    def test_repr_with_url(self):
        node = TextNode("This is a text node", TextType.LINK, "https://example.com")
        expected = "TextNode(This is a text node, link, https://example.com)"
        self.assertEqual(repr(node), expected)

    def test_repr_without_url(self):
        node = TextNode("This is a text node", TextType.BOLD)
        expected = "TextNode(This is a text node, bold, None)"
        self.assertEqual(repr(node), expected)

    def test_repr_with_all_text_types(self):
        # Test repr for all text types
        test_cases = [
            (TextType.TEXT, "text"),
            (TextType.BOLD, "bold"),
            (TextType.ITALIC, "italic"),
            (TextType.CODE, "code"),
            (TextType.LINK, "link"),
            (TextType.IMAGE, "image")
        ]
        
        for text_type, expected_type_str in test_cases:
            node = TextNode("Test", text_type)
            expected = f"TextNode(Test, {expected_type_str}, None)"
            self.assertEqual(repr(node), expected)

    def test_equality_with_none_vs_empty_string_url(self):
        node1 = TextNode("Text", TextType.LINK, None)
        node2 = TextNode("Text", TextType.LINK, "")
        self.assertNotEqual(node1, node2)

    def test_equality_returns_false_not_none(self):
        node1 = TextNode("Text1", TextType.TEXT)
        node2 = TextNode("Text2", TextType.TEXT)
        result = node1.__eq__(node2)
        self.assertIs(result, False)

    def test_equality_returns_true_not_none(self):
        node1 = TextNode("Text", TextType.TEXT)
        node2 = TextNode("Text", TextType.TEXT)
        result = node1.__eq__(node2)
        self.assertIs(result, True)

    def test_init_with_empty_text(self):
        node = TextNode("", TextType.TEXT)
        self.assertEqual(node.text, "")
        self.assertEqual(node.text_type, TextType.TEXT)
        self.assertIsNone(node.url)

    def test_init_with_special_characters(self):
        special_text = "Text with special chars: @#$%^&*()[]{}|\\:;\"'<>,.?/~`"
        node = TextNode(special_text, TextType.TEXT)
        self.assertEqual(node.text, special_text)
        self.assertEqual(node.text_type, TextType.TEXT)


if __name__ == "__main__":
    unittest.main()
