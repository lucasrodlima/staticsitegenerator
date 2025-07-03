import unittest

from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "This is a paragraph")
        self.assertEqual(node.to_html(), "<p>This is a paragraph</p>")

    def test_no_value_leaf(self):
        node = LeafNode("i")
        with self.assertRaises(ValueError) as e:
            node.to_html()
        self.assertEqual(str(e.exception),
                         "Error: No value provided for LeafNode.")

    def test_leaf_to_html_i(self):
        node = LeafNode("i", "This is italic text")
        self.assertEqual(node.to_html(), "<i>This is italic text</i>")

    def test_leaf_with_children(self):
        node = LeafNode("i", "This is italic text")
        with self.assertRaises(TypeError) as e:
            LeafNode("i", "This is italic text", children=[node])
        self.assertEqual(
            str(e.exception),
            "LeafNode.__init__() got an unexpected keyword argument 'children'",
        )

    def test_leaf_with_props(self):
        node = LeafNode("a", "Click me", {
                        "href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(
            node.to_html(), '<a href="https://www.google.com" target="_blank">Click me</a>')

    def test_leaf_with_single_prop(self):
        node = LeafNode("p", "Styled paragraph", {"class": "highlight"})
        self.assertEqual(
            node.to_html(), '<p class="highlight">Styled paragraph</p>')

    def test_leaf_no_tag_returns_value(self):
        node = LeafNode(None, "Just plain text")
        self.assertEqual(node.to_html(), "Just plain text")

    def test_leaf_no_tag_with_props_returns_value(self):
        # Props should be ignored when there's no tag
        node = LeafNode(None, "Plain text", {"class": "ignored"})
        self.assertEqual(node.to_html(), "Plain text")

    def test_leaf_empty_value_raises_error(self):
        node = LeafNode("p", "")
        # Empty string is still a value, so this should work
        self.assertEqual(node.to_html(), "<p></p>")

    def test_leaf_none_value_raises_error(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError) as e:
            node.to_html()
        self.assertEqual(str(e.exception),
                         "Error: No value provided for LeafNode.")

    def test_leaf_repr(self):
        node = LeafNode("p", "This is a paragraph", {"class": "text"})
        expected = "LeafNode(p, This is a paragraph, {'class': 'text'})"
        self.assertEqual(repr(node), expected)

    def test_leaf_repr_no_props(self):
        node = LeafNode("p", "This is a paragraph")
        expected = "LeafNode(p, This is a paragraph, None)"
        self.assertEqual(repr(node), expected)

    def test_leaf_repr_no_tag(self):
        node = LeafNode(None, "Just text")
        expected = "LeafNode(None, Just text, None)"
        self.assertEqual(repr(node), expected)

    def test_leaf_equality(self):
        node1 = LeafNode("p", "Same text", {"class": "same"})
        node2 = LeafNode("p", "Same text", {"class": "same"})
        self.assertEqual(node1, node2)

    def test_leaf_inequality_different_tag(self):
        node1 = LeafNode("p", "Same text")
        node2 = LeafNode("div", "Same text")
        self.assertNotEqual(node1, node2)

    def test_leaf_inequality_different_value(self):
        node1 = LeafNode("p", "Text 1")
        node2 = LeafNode("p", "Text 2")
        self.assertNotEqual(node1, node2)

    def test_leaf_inequality_different_props(self):
        node1 = LeafNode("p", "Same text", {"class": "one"})
        node2 = LeafNode("p", "Same text", {"class": "two"})
        self.assertNotEqual(node1, node2)

    def test_leaf_with_multiple_props(self):
        node = LeafNode(
            "img", "", {"src": "image.jpg", "alt": "Test image", "width": "100"})
        expected = '<img src="image.jpg" alt="Test image" width="100"></img>'
        self.assertEqual(node.to_html(), expected)

    def test_leaf_with_special_characters_in_value(self):
        node = LeafNode("p", "Text with <special> & characters")
        # Note: This doesn't escape HTML entities, which might be a design choice
        self.assertEqual(
            node.to_html(), "<p>Text with <special> & characters</p>")

    def test_leaf_with_numbers_in_value(self):
        node = LeafNode("span", "123")
        self.assertEqual(node.to_html(), "<span>123</span>")

    def test_leaf_with_boolean_string_value(self):
        node = LeafNode("span", "True")
        self.assertEqual(node.to_html(), "<span>True</span>")


if __name__ == "__main__":
    unittest.main()
